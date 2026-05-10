"""Citation Formatter - multiple citation style support"""

from typing import List
from enum import Enum
from app.models.paper import Paper


class CitationStyle(str, Enum):
    APA = "apa"
    MLA = "mla"
    CHICAGO = "chicago"
    HARVARD = "harvard"
    IEEE = "ieee"
    VANCOUVER = "vancouver"
    TURABIAN = "turabian"


class CitationFormatter:
    """Format citations in multiple academic styles"""

    def format_single(self, paper: Paper, style: CitationStyle) -> str:
        """Format a single paper citation"""
        formatters = {
            CitationStyle.APA: self._format_apa,
            CitationStyle.MLA: self._format_mla,
            CitationStyle.CHICAGO: self._format_chicago,
            CitationStyle.HARVARD: self._format_harvard,
            CitationStyle.IEEE: self._format_ieee,
            CitationStyle.VANCOUVER: self._format_vancouver,
            CitationStyle.TURABIAN: self._format_turabian,
        }
        return formatters[style](paper)

    def format_multiple(self, papers: List[Paper], style: CitationStyle) -> List[str]:
        """Format multiple paper citations"""
        return [self.format_single(p, style) for p in papers]

    def _format_apa(self, paper: Paper) -> str:
        authors = self._format_authors_apa(paper.authors)
        year = f"({paper.year})" if paper.year else "(n.d.)"
        title = paper.title

        citation = f"{authors} {year}. {title}."

        if paper.doi:
            citation += f" https://doi.org/{paper.doi}"

        return citation

    def _format_mla(self, paper: Paper) -> str:
        authors = self._format_authors_mla(paper.authors)
        title = f'"{paper.title}."'
        source = paper.source.title()
        year = str(paper.year) if paper.year else "n.d."

        return f"{authors}. {title} {source}, {year}."

    def _format_chicago(self, paper: Paper) -> str:
        authors = self._format_authors_chicago(paper.authors)
        title = f'"{paper.title}."'
        source = paper.source.title()
        year = str(paper.year) if paper.year else "n.d."

        return f"{authors}. {title} {source} ({year})."

    def _format_harvard(self, paper: Paper) -> str:
        authors = self._format_authors_harvard(paper.authors)
        year = paper.year if paper.year else "n.d."
        title = paper.title
        source = paper.source.title()

        return f'{authors} ({year}) "{title}." {source}.'

    def _format_ieee(self, paper: Paper) -> str:
        authors = self._format_authors_ieee(paper.authors)
        title = f'"{paper.title},"'
        source = paper.source.title()
        year = paper.year if paper.year else "n.d."

        return f"{authors}, {title} {source}, {year}."

    def _format_vancouver(self, paper: Paper) -> str:
        authors = self._format_authors_vancouver(paper.authors)
        title = paper.title + "."
        source = paper.source.title()
        year = paper.year if paper.year else "n.d."

        return f"{authors}. {title} {source}. {year}."

    def _format_turabian(self, paper: Paper) -> str:
        authors = self._format_authors_turabian(paper.authors)
        title = f'"{paper.title}."'
        source = paper.source.title()
        year = str(paper.year) if paper.year else "n.d."

        return f"{authors}. {title} {source} ({year})."

    def _format_authors_apa(self, authors) -> str:
        if not authors:
            return "Unknown Author"
        if len(authors) == 1:
            return authors[0].name
        if len(authors) == 2:
            return f"{authors[0].name} & {authors[1].name}"
        return f"{authors[0].name} et al."

    def _format_authors_mla(self, authors) -> str:
        if not authors:
            return "Unknown Author"
        if len(authors) == 1:
            return authors[0].name
        if len(authors) == 2:
            return f"{authors[0].name}, and {authors[1].name}"
        return f"{authors[0].name}, et al."

    def _format_authors_chicago(self, authors) -> str:
        if not authors:
            return "Unknown Author"
        if len(authors) == 1:
            return authors[0].name
        if len(authors) == 2:
            return f"{authors[0].name} and {authors[1].name}"
        return f"{authors[0].name} et al."

    def _format_authors_harvard(self, authors) -> str:
        if not authors:
            return "Unknown Author"
        if len(authors) == 1:
            return authors[0].name.split()[-1]
        if len(authors) == 2:
            return f"{authors[0].name.split()[-1]} and {authors[1].name.split()[-1]}"
        return f"{authors[0].name.split()[-1]} et al."

    def _format_authors_ieee(self, authors) -> str:
        if not authors:
            return "Unknown Author"
        names = []
        for a in authors[:3]:
            parts = a.name.split()
            if len(parts) > 1:
                names.append(f"{parts[0][0]}. {parts[-1]}")
            else:
                names.append(a.name)
        if len(authors) > 3:
            return ", ".join(names) + ", et al."
        return ", ".join(names)

    def _format_authors_vancouver(self, authors) -> str:
        if not authors:
            return "Unknown Author"
        names = []
        for a in authors[:6]:
            parts = a.name.split()
            if len(parts) > 1:
                names.append(f"{parts[0][0]}. {parts[-1]}")
            else:
                names.append(a.name)
        if len(authors) > 6:
            return ", ".join(names) + ", et al."
        return ", ".join(names)

    def _format_authors_turabian(self, authors) -> str:
        return self._format_authors_chicago(authors)
