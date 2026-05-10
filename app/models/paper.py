"""Paper data models"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class Author(BaseModel):
    name: str
    orcid: Optional[str] = None
    affiliation: Optional[str] = None


class PaperBase(BaseModel):
    source: str = Field(..., description="Source: arxiv, semantic_scholar, pubmed")
    external_id: str = Field(..., description="Source-specific ID")
    title: str
    authors: list[Author] = Field(default_factory=list)
    abstract: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    open_access: bool = False
    venue: Optional[str] = None
    categories: list[str] = Field(default_factory=list)
    citations_count: int = 0
    metadata: dict = Field(default_factory=dict)


class Paper(PaperBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class PaperCreate(PaperBase):
    pass


class PaperSearchResult(BaseModel):
    papers: list[Paper]
    total: int
    query: str
    source: Optional[str] = None
