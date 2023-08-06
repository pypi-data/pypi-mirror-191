import logging
import re
from csv import DictReader
from io import StringIO

import requests
from crossref.restful import Etiquette, Works
from django.db.models import QuerySet

from lxml import etree as ET
import xmltodict
from rich.progress import track


def show_preservation(container_title: str, issn: str, volume: str,
                      no: str | None, doi: str,
                      archive: str = None) -> (dict | None, str):
    """
    Determine whether an item is preserved
    :param container_title: the journal/container name
    :param issn: the ISSN
    :param volume: the volume
    :param no: the number
    :param doi: the DOI
    :param archive: the archive to query (or None for all archives)
    :return: a dictionary of preservations and a doi
    """
    from preservationdatabase import constants

    if archive is None:
        preservation_systems = [*constants.archives.values()]
    else:
        preservation_systems = [constants.archives[archive]]

    preservations = {}

    for system in preservation_systems:
        preserved, done = system.preservation(container_title, issn, volume, no)
        preservations[system.name()] = preserved, done

    return preservations, doi


def unpack_range(s):
    """ Converts a range of numbers to a full set"""
    r = []
    for i in s.split(','):
        if '-' not in i:
            r.append(int(i))
        else:
            l, h = map(int, i.split('-'))
            r += range(l, h + 1)
    return r


def show_preservation_for_doi(doi: str,
                              archive: str = None) -> (dict | None, str):
    """
    Determine whether a DOI is preserved with resolution via the REST API
    :param doi: the DOI to look up
    :param archive: the archive to query (or None for all archives)
    :return:
    """
    # TODO: caching
    # TODO: tests
    # TODO: type hints
    # TODO: externalize settings

    my_etiquette = Etiquette('Preservation Status', '0.01',
                             'https://eve.gd', 'meve@crossref.org')

    works = Works(etiquette=my_etiquette)
    doi = works.doi(doi)

    container_title = doi['container-title']
    issn = doi['ISSN']
    volume = doi['volume']
    no = doi['issue']

    return show_preservation(container_title, issn, volume, no, doi, archive)


def normalize_doi(doi: str) -> str:
    """
    Normalize a DOI
    :param doi: the DOI to normalize
    :return: a DOI without the prefix
    """

    # extract the DOI from the input
    # note that this is not as rigorous as it could be, but writing a single
    # expression that captures everything is hard.
    # See: https://www.crossref.org/blog/dois-and-matching-regular-expressions/
    pattern = r'(10.\d{4,9}/[-._;()/:A-Z0-9]+)'

    result = re.search(pattern, doi, re.IGNORECASE)

    return result.group(0) if result else None


def generic_lockss_import(url: str, model,
                          skip_first_line: bool = False,
                          local: bool = False) -> None:
    """
    The generic import function for LOCKSS-like models
    :param url: the URL to download
    :param model: the model class to use
    :param local: whether to use a local file
    :param skip_first_line: whether to skip the first line of the file
    :return: None
    """
    from preservationdatabase.models import Publisher

    # get CSV data
    csv_file = download_remote(local, model, url)

    # clear out
    clear_out(model)

    with StringIO(csv_file) as input_file:
        # skip the top line in the CSV which is something like
        # #Keepers CLOCKSS serials 2022-12-19
        if skip_first_line:
            next(input_file)

        csv_reader = DictReader(input_file)

        for row in csv_reader:
            publisher, created = \
                Publisher.objects.get_or_create(name=row['Publisher'])

            if model.name() == 'CLOCKSS' or model.name() == 'LOCKSS'\
                    or model.name() == 'Cariniana':
                # create the item
                model.create_preservation(
                    issn=row['ISSN'], eissn=row['eISSN'], title=row['Title'],
                    preserved_volumes=row['Preserved Volumes'],
                    preserved_years=row['Preserved Years'],
                    in_progress_volumes=row['In Progress Volumes'],
                    in_progress_years=row['In Progress Years'],
                    publisher=publisher, model=model
                )
            elif model.name() == 'PKP PLN':
                model.create_preservation(
                    issn=row['ISSN'], title=row['Title'],
                    preserved_volumes=row['Vol'],
                    preserved_no=row['No'],
                    publisher=publisher, model=model
                )

            logging.info(f'Added {row["Title"]} to {model.name()} data')


def clear_out(model):
    logging.info(f'Clearing previous {model.name()} data')
    model.objects.all().delete()


def download_remote(local, model, url, bucket="", s3client=None, decode=True):
    if s3client:
        if decode:
            return s3client.get_object(Bucket=bucket, Key=url)[
                'Body'].read().decode('utf-8')
        else:
            return s3client.get_object(Bucket=bucket, Key=url)[
                'Body'].read()

    if not local:
        logging.info(f'Downloading: {model.name()} data')
        csv_file = requests.get(url).text
    else:
        logging.info(f'Using local file for {model.name()} data')

        if decode:
            with open(url, 'r') as f:
                csv_file = f.read()
        else:
            with open(url, 'rb') as f:
                csv_file = f.read()

    return csv_file


def preservation_status(model, container_title, issn, volume,
                        no=None) -> (dict | None, str):
    """
    Determine whether a DOI is preserved in model
    :param model: the model class to use
    :param container_title: the container title
    :param issn: the ISSN
    :param volume: the volume
    :param no: the issue number
    :return: A model item (or None) and a bool indicating whether the item is
    fully preserved
    """
    preserved_item = get_preserved_item_record(model, container_title, issn)

    if not preserved_item or len(preserved_item) == 0:
        return None, False

    for pi in preserved_item:
        vols = [x.strip() for x in pi.preserved_volumes.split(';')]
        vols_in_prog = [x.strip() for x in pi.in_progress_volumes.split(';')]

        volume = str(volume)

        if volume in vols:
            return preserved_item, True
        elif volume in vols_in_prog:
            return preserved_item, False

    return None, False


def get_preserved_item_record(model, container_title, issn) -> QuerySet | None:
    """
    Retrieves preservation records from the model
    :param model: the preservation model to use
    :param container_title: the name of the container
    :param issn: a list of ISSNs
    :return: a queryset of preservation model records or None
    """
    fields = [f.name for f in model._meta.get_fields()]

    # test ISSN
    try:
        if issn and 'issn' in fields:
            preserved_item = model.objects.filter(issn=issn[0])
            if not preserved_item or len(preserved_item) == 0:
                raise model.DoesNotExist
        else:
            raise model.DoesNotExist
    except model.DoesNotExist:
        # test EISSN
        try:
            if issn and 'eissn' in fields:
                preserved_item = model.objects.filter(eissn=issn[0])
                if not preserved_item or len(preserved_item) == 0:
                    raise model.DoesNotExist
            else:
                raise model.DoesNotExist
        except model.DoesNotExist:
            # test container title
            try:
                if container_title and 'container_title' in fields:
                    preserved_item = model.objects.filter(title=container_title)
                    if not preserved_item or len(preserved_item) == 0:
                        raise model.DoesNotExist
                else:
                    raise model.DoesNotExist
            except model.DoesNotExist:
                return None

    return preserved_item


def process_onix(xml_file, elements, callback):
    """
    A faster method for processing ONIX XML than using DOM methods
    """
    root = ET.XML(xml_file)

    outputs = []

    for holdings_record in root.findall(".//{http://www.editeur.org/onix/serials/SOH}HoldingsRecord"):

        resource_versions = holdings_record.findall(".//{http://www.editeur.org/onix/serials/SOH}ResourceVersion")
        for resource_version in resource_versions:

            resource_version_identifiers = resource_version.findall(".//{http://www.editeur.org/onix/serials/SOH}ResourceVersionIdentifier")
            for resource_version_identifier in resource_version_identifiers:

                resource_type = resource_version_identifier.find(".//{http://www.editeur.org/onix/serials/SOH}ResourceVersionIDType")

                # determine if ISSN
                if int(resource_type.text) == 7:
                    # extract unhyphenated ISSN, title, and publisher
                    issn = resource_version_identifier.find(".//{http://www.editeur.org/onix/serials/SOH}IDValue").text
                    title = resource_version.find(".//{http://www.editeur.org/onix/serials/SOH}TitleText").text
                    publisher = resource_version.find(".//{http://www.editeur.org/onix/serials/SOH}PublisherName").text

                    volume = None
                    issue = None

                    # extract volume and issue
                    coverages = resource_version.findall(".//{http://www.editeur.org/onix/serials/SOH}Coverage")

                    for coverage in coverages:
                        level_one = coverage.find(".//{http://www.editeur.org/onix/serials/SOH}Level1")
                        level_two = coverage.find(".//{http://www.editeur.org/onix/serials/SOH}Level2")

                        levels = [level_one, level_two]

                        for level in levels:
                            unit = level.find(".//{http://www.editeur.org/onix/serials/SOH}Unit").text
                            number = level.find(".//{http://www.editeur.org/onix/serials/SOH}Number").text

                            if unit == 'Volume':
                                volume = number
                            elif unit == 'Issue':
                                issue = number
                            else:
                                print('Unrecognised unit: {}'.format(unit))

                    # preservation and verification status
                    try:
                        status = resource_version.find(".//{http://www.editeur.org/onix/serials/SOH}PreservationStatusCode").text
                        verification = resource_version.find(".//{http://www.editeur.org/onix/serials/SOH}VerificationStatus").text

                        output = {'issn': normalize_issn(issn), 'title': title,
                                  'publisher': publisher, 'volume': volume,
                                  'issue': issue, 'status': status,
                                  'verification': verification}

                        outputs.append(output)

                        if callback:
                            callback(output)

                    except AttributeError:
                        # if we get here, there is no preservation or
                        # verification status
                        # print("ERROR on {}".format(issn))
                        pass

    return outputs


def normalize_issn(issn) -> str:
    """
    Normalizes an ISSN
    :param issn: the ISSN
    :return: the normalized ISSN
    """
    return f'{issn[0:4]}-{issn[4:8]}' if '-' not in issn else issn
