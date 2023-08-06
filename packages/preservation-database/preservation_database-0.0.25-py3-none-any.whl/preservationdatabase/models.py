import csv
import logging
import re
import sys
import tempfile
from io import StringIO
from pathlib import Path

from django.db import models, transaction

from preservationdatabase import utils


class Publisher(models.Model):
    class Meta:
        db_table = "preservationData_publisher"
        app_label = "preservationdatabase"

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class LockssPreservation(models.Model):
    class Meta:
        db_table = "preservationData_locksspreservation"

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_years = models.TextField()
    in_progress_volumes = models.TextField()
    in_progress_years = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  default=None)

    @staticmethod
    def name() -> str:
        return "LOCKSS"

    @staticmethod
    def preservation(container_title: str, issn: str, volume: str, no=None):
        """
        Determine whether a DOI is preserved in LOCKSS
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A LockssPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        return utils.preservation_status(LockssPreservation, container_title,
                                         issn, volume, no=no)

    @staticmethod
    def create_preservation(issn, eissn, title, preserved_volumes,
                            preserved_years, in_progress_volumes,
                            in_progress_years, publisher, model) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param eissn: the eISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param preserved_years: the preserved years
        :param in_progress_volumes: the in-progress volumes
        :param in_progress_years: the in-progress years
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn, eissn=eissn, title=title,
            preserved_volumes=preserved_volumes,
            preserved_years=preserved_years,
            in_progress_volumes=in_progress_volumes,
            in_progress_years=in_progress_years,
            publisher=publisher
        )

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(url, LockssPreservation, local=local,
                                    skip_first_line=True)


class CarinianaPreservation(models.Model):
    class Meta:
        db_table = "preservationData_carinianapreservation"

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_years = models.TextField()
    in_progress_volumes = models.TextField()
    in_progress_years = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  default=None)

    @staticmethod
    def name() -> str:
        return "Cariniana"

    @staticmethod
    def preservation(container_title: str, issn: str, volume: str, no=None):
        """
        Determine whether a DOI is preserved in Cariniana
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A Cariniana item (or None) and a bool indicating
        whether the item is fully preserved
        """
        return utils.preservation_status(CarinianaPreservation, container_title,
                                         issn, volume, no=no)

    @staticmethod
    def create_preservation(issn, eissn, title, preserved_volumes,
                            preserved_years, in_progress_volumes,
                            in_progress_years, publisher, model) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param eissn: the eISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param preserved_years: the preserved years
        :param in_progress_volumes: the in-progress volumes
        :param in_progress_years: the in-progress years
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn, eissn=eissn, title=title,
            preserved_volumes=preserved_volumes,
            preserved_years=preserved_years,
            in_progress_volumes=in_progress_volumes,
            in_progress_years=in_progress_years,
            publisher=publisher
        )

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(url, CarinianaPreservation, local=local,
                                    skip_first_line=True)


class ClockssPreservation(models.Model):
    class Meta:
        db_table = "preservationData_clocksspreservation"

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_years = models.TextField()
    in_progress_volumes = models.TextField()
    in_progress_years = models.TextField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  default=None)

    @staticmethod
    def name() -> str:
        return "CLOCKSS"

    @staticmethod
    def preservation(container_title: str, issn: str, volume: str, no=None):
        """
        Determine whether a DOI is preserved in CLOCKSS
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A ClockssPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        return utils.preservation_status(ClockssPreservation, container_title,
                                         issn, volume, no=no)

    @staticmethod
    def create_preservation(issn, eissn, title, preserved_volumes,
                            preserved_years, in_progress_volumes,
                            in_progress_years, publisher, model) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param eissn: the eISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param preserved_years: the preserved years
        :param in_progress_volumes: the in-progress volumes
        :param in_progress_years: the in-progress years
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn, eissn=eissn, title=title,
            preserved_volumes=preserved_volumes,
            preserved_years=preserved_years,
            in_progress_volumes=in_progress_volumes,
            in_progress_years=in_progress_years,
            publisher=publisher
        )

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(url, ClockssPreservation, local=local,
                                    skip_first_line=True)


class PKPPreservation(models.Model):
    class Meta:
        db_table = "preservationData_pkppreservation"

    title = models.TextField()
    issn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_no = models.TextField(blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  default=None)

    @staticmethod
    def name() -> str:
        return "PKP PLN"

    @staticmethod
    def preservation(container_title, issn, volume, no):
        """
        Determine whether a DOI is preserved in the PKP private LOCKSS network
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A PKPPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(PKPPreservation,
                                                         container_title, issn)

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        if no is not None and no != '' and no != '0':
            preserved_item.filter(preserved_no=no)

            if len(preserved_item) == 0:
                return None, False

        return preserved_item, True

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        utils.generic_lockss_import(url, PKPPreservation, local=local,
                                    skip_first_line=True)

    @staticmethod
    def create_preservation(issn, title, preserved_volumes, preserved_no,
                            publisher, model) -> None:
        """
        Create a preservation item of this model
        :param issn: the ISSN
        :param title: the title
        :param preserved_volumes: the preserved volumes
        :param publisher: the publisher object
        :param model: the model on which to operate
        :return: None
        """
        model.objects.create(
            issn=issn, title=title, preserved_volumes=preserved_volumes,
            preserved_no=preserved_no, publisher=publisher
        )


class HathiPreservation(models.Model):
    class Meta:
        db_table = "preservationData_hathipreservation"

    title = models.TextField()
    issn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()

    @staticmethod
    def name() -> str:
        return "HathiTrust"

    @staticmethod
    def preservation(container_title, issn, volume, no=None):
        """
        Determine whether a DOI is preserved in HathiTrust
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A HathiPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(HathiPreservation,
                                                         container_title, issn)

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        if preserved_item:
            volume = str(volume)

            for pi in preserved_item:
                vols = [x.strip() for x in
                        pi.preserved_volumes.split(';')]

                if volume in vols:
                    return pi, True
                else:
                    return None, False
        else:
            return None, False

    @staticmethod
    @transaction.atomic
    def import_data(url, bucket="", s3client=None):
        # download the data file from S3 bucket
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'downloaded.file'

            hathi_data = utils.download_remote(False, HathiPreservation,
                                               url, bucket=bucket,
                                               s3client=s3client,
                                               decode=False, file=True,
                                               filename=str(path))

            # clear out existing data
            utils.clear_out(HathiPreservation)

            csv.field_size_limit(sys.maxsize)

            with open(str(path), 'r') as input_file:
                csv_reader = csv.reader(input_file, delimiter='\t')

                volume_matcher = r'v\.\s?(\d+(?:\-?\d+)?)'
                no_matcher = r'no\.\s?(\d+(?:\-?\d+)?)'
                year_matcher = r'\d{4}'

                for row in csv_reader:
                    try:
                        vols = row[4]
                        issn = row[9]
                        title = row[11]
                        publishing_info = row[12]
                        date = row[16]
                        bf = row[19]
                        unknown_format = False

                        # check if it's an ISSN
                        logging.info('ISSN: {}'.format(issn))

                        # if it's a serial, try to parse the vols
                        if bf == 'SE' and issn and vols:
                            matches = re.findall(volume_matcher, vols)

                            if matches:
                                for match in matches:
                                    vols = utils.unpack_range(match)
                            else:
                                matches = re.findall(no_matcher, vols)

                                if matches:
                                    for match in matches:
                                        vols = utils.unpack_range(match)
                                else:

                                    matches = re.findall(year_matcher, vols)

                                    if matches:
                                        for match in matches:
                                            vols = match
                                    else:
                                        unknown_format = True

                            if not unknown_format:
                                if title.endswith('.'):
                                    title = title[:-1]

                                HathiPreservation.objects.create(
                                    issn=issn,
                                    title=title,
                                    preserved_volumes=vols
                                )

                                logging.info(f'Added {title} to '
                                             f'{HathiPreservation.name()} data')
                    except IndexError:
                        pass


class PorticoPreservation(models.Model):
    class Meta:
        db_table = "preservationData_porticopreservation"

    title = models.TextField()
    issn = models.CharField(max_length=20)
    eissn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()

    # this indicates whether the title is preserved or queued
    preserved = models.BooleanField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  default=None)

    @staticmethod
    def name():
        return 'Portico'

    @staticmethod
    def preservation(container_title, issn, volume, no=None):
        """
        Determine whether a DOI is preserved in Portico
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A PorticoPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(PorticoPreservation,
                                                         container_title, issn)

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        # Portico gives volume formats as follows:
        # 2013/2014 - v. 2 (1-2)
        volume_regex = r'v\.\s(\d+)'

        for pi in preserved_item:
            matches = re.findall(volume_regex, pi.preserved_volumes)

            volume = str(volume)

            if volume in matches:
                return pi, pi.preserved

        return None, False

    @staticmethod
    @transaction.atomic
    def import_data(url: str = None, local: bool = False) -> None:
        """
        Import data into the system
        :param url: the URL of the data file
        :param local: whether the data file is local
        :return: None
        """
        # get CSV data
        csv_file = utils.download_remote(local, PorticoPreservation, url)

        # clear out
        utils.clear_out(PorticoPreservation)

        # increase the CSV field size to accommodate large entries
        csv.field_size_limit(sys.maxsize)

        with StringIO(csv_file) as input_file:
            csv_reader = csv.DictReader(input_file, delimiter='\t',
                                        quoting=csv.QUOTE_NONE)

            for row in csv_reader:
                publisher, created = \
                    Publisher.objects.get_or_create(name=row['publisher_name'])

                PorticoPreservation.objects.create(
                    issn=row['print_identifier'],
                    eissn=row['online_identifier'],
                    title=row['publication_title'],
                    preserved_volumes=row['holding_list'],
                    preserved=(row['notes'] == 'Preserved'),
                    publisher=publisher
                )

                logging.info(f'Added {row["publication_title"]} to '
                             f'{PorticoPreservation.name()} data')


class OculScholarsPortalPreservation(models.Model):
    class Meta:
        db_table = "preservationData_oculpreservation"

    title = models.TextField()

    """
    ONIX field codes to identify an ISSN:
    ResourceVersionIDType = 7
    IDValue = unhyphenated ISSN
    
    e.g.
    <oph:ResourceVersion>
        <oph:ResourceVersionIdentifier>
        <oph:ResourceVersionIDType>07</oph:ResourceVersionIDType>
        <oph:IDValue> 27697541</oph:IDValue>
    </oph:ResourceVersionIdentifier>
    """
    issn = models.CharField(max_length=20)
    preserved_volumes = models.TextField()
    preserved_no = models.TextField()

    # this indicates whether the title is preserved or queued
    """
    ONIX field codes for the <oph:PreservationStatus><oph:PreservationStatusCode> tags:
    00	Unknown	The preservation status is genuinely unknown, and should be updated as soon as information is available	5		
    01	Will not be preserved	Preservation agency has decided against preservation of the issues and e-content in the <Coverage> statement	5		
    02	Undecided	Preservation agency is considering preservation of the issues and e-content in the <Coverage> statement. No decision has yet been made. This status should be updated as soon as information is available	5		
    03	Committed	Preservation agency is committed to preserving the issues and e-content in the <Coverage> statement. No active steps have yet been taken	5		
    04	In progress	Preservation agency is in the process of preserving the issues and e-content in the <Coverage> statement	5		
    05	Preserved	Preservation agency has preserved the issues and e-content in the <Coverage> statement	5
    """
    preserved = models.IntegerField()

    """
    ONIX field codes for the <oph:VerificationStatus> tag:
    00	Unknown	It is genuinely unknown whether the preservation agency has checked the preserved holdings in the <Coverage> statement. This status should be updated when information is available		
    01	Unverified	Preservation agency has not checked the preserved holdings in the <Coverage> statement, and it is not known whether all issues or e-content items are preserved
    02	Verification in progress	Preservation agency is in the process of checking the preserved holdings in the <Coverage> statement, and nothing can be said about completeness at this stage		
    03	Verified and incomplete	Preservation agency has checked the preserved holdings in the <Coverage> statement, and some issues or e-content items intended to be preserved are not complete		
    04	Verified and complete	Preservation agency has checked the preserved holdings in the <Coverage> statement, and all issues or e-content items intended to be preserved are complete
    """
    verified = models.IntegerField()

    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE,
                                  default=None)

    @staticmethod
    def name():
        return 'OCUL Scholars Portal'

    @staticmethod
    def preservation(container_title, issn, volume, no=None):
        """
        Determine whether a DOI is preserved in Portico
        :param container_title: the container title
        :param issn: the ISSN
        :param volume: the volume
        :param no: the issue number
        :return: A PorticoPreservation item (or None) and a bool indicating
        whether the item is fully preserved
        """
        preserved_item = utils.get_preserved_item_record(PorticoPreservation,
                                                         container_title, issn)

        if not preserved_item or len(preserved_item) == 0:
            return None, False

        # Portico gives volume formats as follows:
        # 2013/2014 - v. 2 (1-2)
        volume_regex = r'v\.\s(\d+)'

        for pi in preserved_item:
            matches = re.findall(volume_regex, pi.preserved_volumes)

            volume = str(volume)

            if volume in matches:
                return pi, pi.preserved

        return None, False

    @staticmethod
    def import_data(url, bucket="", s3client=None):
        # download the data file from S3 bucket
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'downloaded.file'

            xml_file = utils.download_remote(False,
                                             OculScholarsPortalPreservation,
                                             url, bucket=bucket,
                                             s3client=s3client,
                                             decode=False, file=True,
                                             filename=str(path))

            # local file for testing
            # xml_file = '/home/martin/scholars_portal_keepers_20230202.xml'

            # clear out
            utils.clear_out(OculScholarsPortalPreservation)

            fields = ['oph:ResourceVersionIDType', 'oph:IDValue',
                      'oph:FixedCoverage', 'oph:PreservationStatusCode',
                      'oph:VerificationStatus']

            xml_parsed = utils.process_onix(
                xml_file, fields,
                callback=OculScholarsPortalPreservation.create_preservation)

    @staticmethod
    def create_preservation(output) -> None:
        """
        Create a preservation item of this model
        :param output: a dictionary from an ONIX import
        :return: None
        """

        if 'status' not in output or output['status'] is None:
            status = 0
        else:
            status = output['status']

        if 'verified' not in output or output['verified'] is None:
            verified = 0
        else:
            verified = output['verified']

        if 'publisher' not in output or output['publisher'] is None:
            publisher = 'Default'
        else:
            publisher = output['publisher']

        if 'title' not in output or output['title'] is None:
            title = 'Unknown title'
        else:
            title = output['title']

        publisher, created = \
            Publisher.objects.get_or_create(name=publisher)

        volumes = output['volumes']
        issues = output['issues']

        for volume, issue in zip(volumes, issues):

            volume = volume if volume is not None else ''
            issue = issue if issue is not None else ''

            OculScholarsPortalPreservation.objects.create(
                issn=output['issn'], title=title,
                preserved_volumes=volume, preserved_no=issue,
                preserved=status, verified=verified,
                publisher=publisher
            )

        logging.info(f'Added {title} to '
                     f'{OculScholarsPortalPreservation.name()} data')
