# pylint: disable=R0801
"""Test for the package"""
from s23openalex import Works


REF_BIBTEX = """@article{Kitchin2015,
    author = John R. Kitchin,
    year = 2015,
    title = Examples of Effective Data Sharing in Scientific Publishing,
    journal = ACS Catalysis,
    volume = 5,
    number = 6,
    pages = 3894-3899,
    doi = https://doi.org/10.1021/acscatal.5b00538
}"""


def test_bibtex():
    """test for bibtex"""
    work = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert REF_BIBTEX == work.get_bibtex()
