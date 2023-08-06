import inspect
import logging
import os.path
import sys
import tracemalloc

import boto3
import click
from rich.console import Console
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]",
    handlers=[RichHandler(console=Console(stderr=True))]
)
log = logging.getLogger("rich")

sys.path.append(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django

django.setup()

from preservationdatabase.models import CarinianaPreservation, \
    ClockssPreservation, HathiPreservation, LockssPreservation, \
    OculScholarsPortalPreservation, PKPPreservation, PorticoPreservation
from django.db import transaction
import utils


@click.group()
def cli():
    pass


@click.command()
@click.option('--url',
              default='https://api.portico.org/kbart/Portico_Holding_KBart.txt',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_portico(url, local):
    """Download and import data from Portico"""
    PorticoPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='https://reports.clockss.org/keepers/keepers-CLOCKSS-report.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_clockss(url, local):
    """Download and import data from CLOCKSS"""
    ClockssPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='https://reports.lockss.org/keepers/keepers-LOCKSS-report.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_lockss(url, local):
    """Download and import data from LOCKSS"""
    LockssPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='https://pkp.sfu.ca/files/pkppn/onix.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_pkp(url, local):
    """Download and import data from PKP's private LOCKSS network"""
    PKPPreservation.import_data(url, local=local)


@click.command()
@click.option('--url',
              default='http://reports-lockss.ibict.br/keepers/pln/ibictpln/keepers-IBICTPLN-report.csv',
              help='The URL to fetch')
@click.option('--local', is_flag=True, default=False)
@transaction.atomic()
def import_cariniana(url, local):
    """Download and import data from Cariniana"""
    CarinianaPreservation.import_data(url, local=local)


@click.command()
@click.option('--file',
              default='hathi_full_20230101.txt',
              help='The filename of the Hathitrust full dump to use')
@click.option('--bucket',
              default='preservation.research.crossref.org',
              help='The s3 bucket from which to retrieve the data')
@transaction.atomic()
def import_hathi(file, bucket):
    """Import data from Hathi (requires local file download or S3)"""
    s3client = boto3.client('s3')
    HathiPreservation.import_data(
        file, bucket=bucket, s3client=s3client)


@click.command()
@click.option('--file',
              default='scholars_portal_keepers_20230202.xml',
              help='The filename of the OCUL full dump to use')
@click.option('--bucket',
              default='preservation.research.crossref.org',
              help='The s3 bucket from which to retrieve the data')
@transaction.atomic()
def import_ocul(file, bucket):
    """Import data from Ocul (requires local file download or S3)"""

    s3client = boto3.client('s3')
    OculScholarsPortalPreservation.import_data(file, bucket=bucket,
                                               s3client=s3client)

    return


@click.command()
def import_all():
    """Download and import all data (excluding HathiTrust)"""

    import_clockss(
        url='https://reports.clockss.org/keepers/keepers-CLOCKSS-report.csv'
    )

    import_portico(
        url='https://api.portico.org/kbart/Portico_Holding_KBart.txt'
    )

    import_lockss(
        url='https://reports.lockss.org/keepers/keepers-LOCKSS-report.csv'
    )

    import_cariniana(
        url='http://reports-lockss.ibict.br/keepers/pln/ibictpln/keepers-IBICTPLN-report.csv'
    )


@click.command()
@click.option('--doi',
              help='The DOI to lookup for preservation status')
def show_preservation(doi):
    """
    Determine whether a DOI is preserved
    """
    doi = utils.normalize_doi(doi)
    preservation_statuses, doi = utils.show_preservation_for_doi(doi)

    for key, value in preservation_statuses.items():
        preserved, done = value

        if preserved:
            if done:
                log.info(f'[green]Preserved:[/] in {key}',
                         extra={'markup': True})
            else:
                log.info(f'[yellow]Preserved (in progress):[/] '
                         f'in {key}',
                         extra={'markup': True})
        else:
            log.info(f'[red]Not preserved:[/] in {key}',
                     extra={'markup': True})


if __name__ == '__main__':
    cli.add_command(import_all)
    cli.add_command(import_cariniana)
    cli.add_command(import_clockss)
    cli.add_command(import_hathi)
    cli.add_command(import_lockss)
    cli.add_command(import_ocul)
    cli.add_command(import_pkp)
    cli.add_command(import_portico)
    cli.add_command(show_preservation)
    cli()
