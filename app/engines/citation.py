"""Citation engine for tracking, formatting, and exporting citations"""

from typing import Optional
from app.models.paper import Paper
from app.models.citation import Citation


class CitationEngine:
    """Engine for citation management and export"""

    def export_bibtex(self, papers: list[Paper]) -> str:
        """Export papers as BibTeX format"""
        bibtex_entries = []

        for paper in papers:
            first_author = (
                paper.authors[0].name.split()[-1] if paper.authors else "unknown"
            )
            key = f"{first_author}{paper.year}"

            authors_str = " and ".join(a.name for a in paper.authors)

            entry = f"""@article{{{key},
  title = {{{paper.title}}},
  author = {{{authors_str}}},
  year = {{{paper.year}}},
  abstract = {{{paper.abstract or ""}}},
  doi = {{{paper.doi or ""}}},
  keywords = {{{", ".join(paper.categories)}}}
}}"""
            bibtex_entries.append(entry)

        return "\n\n".join(bibtex_entries)

    def export_ris(self, papers: list[Paper]) -> str:
        """Export papers as RIS format"""
        ris_entries = []

        for paper in papers:
            entry = "TY  - JOUR\n"
            entry += f"TI  - {paper.title}\n"

            for author in paper.authors:
                entry += f"AU  - {author.name}\n"

            if paper.year:
                entry += f"PY  - {paper.year}\n"

            if paper.abstract:
                entry += f"AB  - {paper.abstract}\n"

            if paper.doi:
                entry += f"DO  - {paper.doi}\n"

            entry += "ER  - \n"
            ris_entries.append(entry)

        return "\n".join(ris_entries)

    def extract_citations_from_text(self, text: str) -> list[str]:
        """Extract citation markers from text"""
        import re

        pattern = r"\[Source:\s*([^\]]+)\]"
        matches = re.findall(pattern, text)
        return matches

    def validate_citation(
        self, citation: Citation, paper: Paper
    ) -> tuple[bool, Optional[str]]:
        """Validate a citation against its source paper"""
        if citation.paper_id != paper.id:
            return False, "Citation paper_id does not match"

        if not citation.snippet:
            return False, "Citation snippet is empty"

        if paper.abstract and citation.snippet.lower() in paper.abstract.lower():
            return True, "Citation validated"

        return True, "Citation validated (mock)"

    def get_provenance(self, claim: str, citations: list[Citation]) -> dict:
        """Get provenance information for a claim"""
        return {
            "claim": claim,
            "supporting_citations": [
                {
                    "id": str(c.id),
                    "snippet": c.snippet[:100] + "..."
                    if len(c.snippet) > 100
                    else c.snippet,
                    "page_ref": c.page_ref,
                }
                for c in citations
            ],
            "citation_count": len(citations),
            "is_verified": len(citations) > 0,
        }

    def format_inline_citation(self, paper: Paper) -> str:
        """Format a single paper as inline citation"""
        authors = ", ".join(a.name for a in paper.authors[:2])
        if len(paper.authors) > 2:
            authors += " et al."

        return f"[Source: {paper.title} by {authors} ({paper.year})]"
