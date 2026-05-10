"""Export engine for various file formats"""

import csv
import io
from typing import Optional
from app.models.paper import Paper


class ExportEngine:
    """Engine for exporting papers and summaries to various formats"""

    def export_to_csv(self, papers: list[Paper]) -> str:
        """Export papers to CSV format"""
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            ["Title", "Authors", "Year", "Source", "DOI", "Citations", "Open Access"]
        )

        for paper in papers:
            writer.writerow(
                [
                    paper.title,
                    "; ".join(a.name for a in paper.authors),
                    paper.year or "",
                    paper.source,
                    paper.doi or "",
                    paper.citations_count,
                    "Yes" if paper.open_access else "No",
                ]
            )

        return output.getvalue()

    def export_to_bibtex(self, papers: list[Paper]) -> str:
        """Export papers to BibTeX format"""
        entries = []

        for paper in papers:
            first_author = (
                paper.authors[0].name.split()[-1] if paper.authors else "Unknown"
            )
            key = (
                f"{first_author}{paper.year}"
                if paper.year
                else f"unknown{paper.external_id}"
            )

            authors_str = " and ".join(a.name for a in paper.authors)

            entry = f"""@article{{{key},
  title = {{{paper.title}}},
  author = {{{authors_str}}},
  year = {{{paper.year or "n.d."}}},
  doi = {{{paper.doi or ""}}},
  abstract = {{{paper.abstract or ""}}},
}}"""
            entries.append(entry)

        return "\n\n".join(entries)

    def export_to_ris(self, papers: list[Paper]) -> str:
        """Export papers to RIS format"""
        entries = []

        for paper in papers:
            entry = "TY  - JOUR\n"
            entry += f"TI  - {paper.title}\n"
            for author in paper.authors:
                entry += f"AU  - {author.name}\n"
            if paper.year:
                entry += f"PY  - {paper.year}\n"
            if paper.doi:
                entry += f"DO  - {paper.doi}\n"
            if paper.abstract:
                entry += f"AB  - {paper.abstract}\n"
            entry += "ER  - \n"
            entries.append(entry)

        return "\n".join(entries)

    def export_to_markdown(
        self, papers: list[Paper], summary: Optional[str] = None
    ) -> str:
        """Export papers to Markdown format"""
        md = "# Research Papers\n\n"

        if summary:
            md += f"## Summary\n{summary}\n\n"

        md += "## Papers\n\n"

        for i, paper in enumerate(papers, 1):
            md += f"### {i}. {paper.title}\n\n"
            md += f"**Authors:** {', '.join(a.name for a in paper.authors)}\n\n"
            md += f"**Year:** {paper.year} | **Source:** {paper.source}\n\n"
            if paper.doi:
                md += f"**DOI:** {paper.doi}\n\n"
            if paper.abstract:
                md += f"**Abstract:** {paper.abstract[:200]}...\n\n"
            md += "---\n\n"

        return md
