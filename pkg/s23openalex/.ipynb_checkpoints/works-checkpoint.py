# pylint: disable=R0801
"""Work with https://api.openalex.org/works."""

import time
import base64
import requests
import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure
from IPython.display import HTML


class Works:
    """works class for return ris/bibtex"""

    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    def __str__(self):
        return "str"

    def __repr__(self):
        _authors = [au["author"]["display_name"] for au in self.data["authorships"]]
        if len(_authors) == 0:
            authors = "None"
        elif len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and" + _authors[-1]

        title = self.data["title"]

        journal = self.data["host_venue"]["display_name"]
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        works_id = self.data["id"]
        repr_string = f'{authors}, {title}, {journal}, {volume}{issue}{pages}, ({year}), \
            {self.data["doi"]}. cited by: {citedby}. {works_id}'
        return repr_string

    def create_plot(self, markdown):
        """Create a plot for _repr_markdown function"""
        # Citation counts by year
        years = [e["year"] for e in self.data["counts_by_year"]]
        counts = [e["cited_by_count"] for e in self.data["counts_by_year"]]
        fig, axis = plt.subplots()
        axis.bar(years, counts)
        axis.set_xlabel("year")
        axis.set_ylabel("citation count")
        data = print_figure(fig, "png")  # save figure in string
        plt.close(fig)

        b64 = base64.b64encode(data).decode("utf8")
        citefig = f"![img](data:image/png;base64,{b64})"

        markdown += "<br>" + citefig
        return markdown

    def _repr_markdown_(self):
        _authors = [
            f'[{au["author"]["display_name"]}]({au["author"]["id"]})'
            for au in self.data["authorships"]
        ]
        if len(_authors) == 1:
            authors = _authors[0]
        else:
            authors = ", ".join(_authors[0:-1]) + " and " + _authors[-1]

        title = self.data["title"]

        journal = f"[{self.data['host_venue']['display_name']}]({self.data['host_venue']['id']})"
        volume = self.data["biblio"]["volume"]

        issue = self.data["biblio"]["issue"]
        if issue is None:
            issue = ", "
        else:
            issue = ", " + issue

        pages = "-".join(
            [
                self.data["biblio"].get("first_page", "") or "",
                self.data["biblio"].get("last_page", "") or "",
            ]
        )
        year = self.data["publication_year"]
        citedby = self.data["cited_by_count"]

        works_id = self.data["id"]

        markdown = f'{authors}, *{title}*, **{journal}**, {volume}{issue}, {pages}, ({year}), \
            {self.data["doi"]}. cited by: {citedby}. [Open Alex]({works_id})'

        return self.create_plot(markdown)

    @property
    def ris(self):
        """Return ris for the work"""
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        return ris

    def ris_html(self):
        """Return ris in html form for the work"""
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64, {ris64} \
            " download="ris">Download RIS</a>'

        return HTML(uri)

    def bibtex(self):
        """Print out bibtex for the work"""
        fields = []
        if self.data["type"] == "journal-article":
            author_list = []
            for author in self.data["authorships"]:
                author_lastname = author["author"]["display_name"].split()[-1]
                publication_year = self.data["publication_year"]
                author_list += [f"{author_lastname}{publication_year},"]
            fields += ["@article{" + " ".join(author_list)]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'    author = {author["author"]["display_name"]},']

        fields += [f'    year = {self.data["publication_year"]},']
        fields += [f'    title = {self.data["title"]},']
        fields += [f'    journal = {self.data["host_venue"]["display_name"]},']
        fields += [f'    volume = {self.data["biblio"]["volume"]},']

        if self.data["biblio"]["issue"]:
            fields += [f'    number = {self.data["biblio"]["issue"]},']

        fields += [
            f'    pages = {self.data["biblio"]["first_page"]}-{self.data["biblio"]["last_page"]},'
        ]
        fields += [f'    doi = {self.data["doi"]}']
        fields += ["}"]

        bibtex = "\n".join(fields)
        print(bibtex)
        return bibtex

    def related_works(self):
        """Return related works for the instance"""
        rworks = []
        for related_works_url in self.data["related_works"]:
            related_works = Works(related_works_url)
            rworks += [related_works]
            time.sleep(0.101)
        return rworks

    def references(self):
        """Return referenced works for the instance"""
        refers = []
        for rf_url in self.data["referenced_works"]:
            refer = Works(rf_url)
            refers += [refer]
            time.sleep(0.101)
        return refers

    def citing_works(self):
        """Return citing works for the instance"""
        cite_data = requests.get(self.data["cited_by_api_url"]).json()
        cites = []
        for cite in cite_data["results"]:
            url = cite["id"]
            cite_work = Works(url)
            cites += [cite_work]
            time.sleep(0.101)
        return cites
