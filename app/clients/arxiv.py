"""arXiv client - uses real arXiv API"""

import requests
from typing import Optional
from app.clients.base import PaperSourceClient
from app.models.paper import PaperSearchResult, Paper, Author


API_URL = "http://export.arxiv.org/api/query"


class ArxivClient(PaperSourceClient):
    """arXiv API client"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "ai-research-lab/0.1"})

    def get_source_name(self) -> str:
        return "arxiv"

    def search(
        self,
        query: str,
        max_results: int = 10,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
    ) -> PaperSearchResult:
        search_query = f"all:{query}"
        if year_from:
            search_query += f" AND submittedDate:[{year_from}0101 TO *]"
        if year_to:
            search_query = f"submittedDate:[* TO {year_to}1231] AND ({search_query})"

        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending",
        }

        try:
            response = self.session.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            return self._parse_atom_response(response.text)
        except Exception:
            return PaperSearchResult(papers=[], total=0, query=query)

    def get_paper(self, paper_id: str) -> dict:
        """Get paper by arXiv ID"""
        params = {"id_list": paper_id, "max_results": 1}
        try:
            response = self.session.get(API_URL, params=params, timeout=10)
            response.raise_for_status()
            result = self._parse_atom_response(response.text)
            if result.papers:
                return result.papers[0].model_dump()
        except Exception:
            pass
        return None

    def _parse_atom_response(self, xml_text: str) -> PaperSearchResult:
        """Parse Atom XML response from arXiv"""
        import xml.etree.ElementTree as ET

        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            return PaperSearchResult(papers=[], total=0, query="")

        papers = []

        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title_elem = entry.find(".//{http://www.w3.org/2005/Atom}title")
            summary_elem = entry.find(".//{http://www.w3.org/2005/Atom}summary")

            title = (
                title_elem.text.strip()
                if title_elem is not None and title_elem.text
                else ""
            )
            summary = (
                summary_elem.text.strip()
                if summary_elem is not None and summary_elem.text
                else ""
            )

            authors = []
            for author in entry.findall(".//{http://www.w3.org/2005/Atom}author"):
                name_elem = author.find("{http://www.w3.org/2005/Atom}name")
                if name_elem is not None and name_elem.text:
                    authors.append(Author(name=name_elem.text))

            published_elem = entry.find(".//{http://www.w3.org/2005/Atom}published")
            year = (
                int(published_elem.text[:4])
                if published_elem is not None and published_elem.text
                else None
            )

            id_elem = entry.find(".//{http://www.w3.org/2005/Atom}id")
            arxiv_id = ""
            if id_elem is not None and id_elem.text:
                arxiv_id = id_elem.text.split("/")[-1]

            doi_elem = entry.find(".//{http://arxiv.org/schemas/atom}doi")
            doi = doi_elem.text if doi_elem is not None else None

            categories = [
                cat.get("term", "")
                for cat in entry.findall(".//{http://www.w3.org/2005/Atom}category")
            ]

            papers.append(
                Paper(
                    source="arxiv",
                    external_id=arxiv_id,
                    title=title,
                    authors=authors,
                    abstract=summary,
                    year=year,
                    doi=doi,
                    open_access=True,
                    categories=categories,
                )
            )

        return PaperSearchResult(papers=papers, total=len(papers), query="search")
