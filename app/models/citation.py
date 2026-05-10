"""Citation data models"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class CitationBase(BaseModel):
    paper_id: UUID
    snippet: str = Field(..., description="Source text snippet")
    page_ref: Optional[str] = Field(None, description="Page or section reference")
    claim_id: Optional[UUID] = None
    position_start: Optional[int] = None
    position_end: Optional[int] = None


class Citation(CitationBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class CitationCreate(CitationBase):
    pass


class CitationExport(BaseModel):
    format: str = Field(..., description="Export format: bibtex, ris")
    citations: list[Citation]
