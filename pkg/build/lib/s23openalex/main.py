# pylint: disable=E0401, R0801
"""main routine"""
import click
from .works import Works


@click.command()
@click.option("--bibtex", is_flag=True, help="Get the BibTeX citation")
@click.option("--ris", is_flag=True, help="Get the RIS citation")
@click.argument("doi", nargs=1)
def main(doi, bibtex, ris):
    """main routine"""
    if doi is str:
        work = Works(doi)
    else:
        work = Works(str(doi))

    if bibtex:
        work.bibtex()
    elif ris:
        work.ris()
