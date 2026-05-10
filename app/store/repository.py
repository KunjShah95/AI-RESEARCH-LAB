"""PostgreSQL repository for papers and citations"""

from uuid import UUID
from typing import Optional
import json
from app.database import Database, db
from app.models.paper import Paper, PaperCreate, Author
from app.models.citation import Citation, CitationCreate


class PaperRepository:
    """Repository for paper CRUD operations"""

    def __init__(self, database: Database = None):
        self.db = database if database else db

    def save_paper(self, paper: PaperCreate) -> Paper:
        """Save a paper to the database"""
        query = """
            INSERT INTO papers (source, external_id, title, authors, abstract, year, doi, open_access, metadata)
            VALUES (%(source)s, %(external_id)s, %(title)s, %(authors)s, %(abstract)s, %(year)s, %(doi)s, %(open_access)s, %(metadata)s)
            ON CONFLICT (source, external_id) DO UPDATE SET
                title = EXCLUDED.title,
                abstract = EXCLUDED.abstract
            RETURNING id, created_at
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(
                query,
                {
                    "source": paper.source,
                    "external_id": paper.external_id,
                    "title": paper.title,
                    "authors": json.dumps([a.model_dump() for a in paper.authors]),
                    "abstract": paper.abstract,
                    "year": paper.year,
                    "doi": paper.doi,
                    "open_access": paper.open_access,
                    "metadata": json.dumps(paper.metadata),
                },
            )
            result = cursor.fetchone()

        paper_dict = paper.model_dump()
        paper_dict["id"] = result["id"]
        paper_dict["created_at"] = result["created_at"]

        paper_dict["authors"] = [Author(**a) for a in json.loads(paper_dict["authors"])]

        return Paper(**paper_dict)

    def get_paper(self, paper_id: UUID) -> Optional[Paper]:
        """Get paper by ID"""
        query = "SELECT * FROM papers WHERE id = %s"
        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(paper_id),))
            result = cursor.fetchone()

        if result is None:
            return None

        return self._row_to_paper(result)

    def search_papers(
        self,
        query: str,
        source: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit: int = 20,
    ) -> list[Paper]:
        """Search papers in database"""
        conditions = []
        params = {"limit": limit}

        if query:
            conditions.append("(title ILIKE %(query)s OR abstract ILIKE %(query)s)")
            params["query"] = f"%{query}%"

        if source:
            conditions.append("source = %(source)s")
            params["source"] = source

        if year_from:
            conditions.append("year >= %(year_from)s")
            params["year_from"] = year_from

        if year_to:
            conditions.append("year <= %(year_to)s")
            params["year_to"] = year_to

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"SELECT * FROM papers WHERE {where_clause} ORDER BY created_at DESC LIMIT %(limit)s"

        with self.db.get_cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()

        return [self._row_to_paper(row) for row in results]

    def _row_to_paper(self, row) -> Paper:
        """Convert database row to Paper model"""
        return Paper(
            id=row["id"],
            source=row["source"],
            external_id=row["external_id"],
            title=row["title"],
            authors=[Author(**a) for a in row["authors"]],
            abstract=row["abstract"],
            year=row["year"],
            doi=row["doi"],
            open_access=row["open_access"],
            metadata=row.get("metadata", {}),
            created_at=row["created_at"],
        )


class CitationRepository:
    """Repository for citation operations"""

    def __init__(self, database: Database = None):
        self.db = database if database else db

    def save_citation(self, citation: CitationCreate) -> Citation:
        """Save a citation"""
        query = """
            INSERT INTO citations (paper_id, snippet, page_ref, claim_id, position_start, position_end)
            VALUES (%(paper_id)s, %(snippet)s, %(page_ref)s, %(claim_id)s, %(position_start)s, %(position_end)s)
            RETURNING id, created_at
        """

        with self.db.get_cursor() as cursor:
            cursor.execute(
                query,
                {
                    "paper_id": citation.paper_id,
                    "snippet": citation.snippet,
                    "page_ref": citation.page_ref,
                    "claim_id": citation.claim_id,
                    "position_start": citation.position_start,
                    "position_end": citation.position_end,
                },
            )
            result = cursor.fetchone()

        citation_dict = citation.model_dump()
        citation_dict["id"] = result["id"]
        citation_dict["created_at"] = result["created_at"]

        return Citation(**citation_dict)

    def get_citations_for_paper(self, paper_id: UUID) -> list[Citation]:
        """Get all citations for a paper"""
        query = "SELECT * FROM citations WHERE paper_id = %s ORDER BY created_at"

        with self.db.get_cursor() as cursor:
            cursor.execute(query, (str(paper_id),))
            results = cursor.fetchall()

        return [
            Citation(
                id=row["id"],
                paper_id=row["paper_id"],
                snippet=row["snippet"],
                page_ref=row["page_ref"],
                claim_id=row["claim_id"],
                position_start=row["position_start"],
                position_end=row["position_end"],
                created_at=row["created_at"],
            )
            for row in results
        ]
