"""Notes API - collaborative note management"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid


router = APIRouter()


class NoteCreate(BaseModel):
    content: str
    paper_id: Optional[str] = None
    project_id: Optional[str] = None
    is_public: bool = False


class NoteUpdate(BaseModel):
    content: Optional[str] = None
    is_public: Optional[bool] = None


class Note(BaseModel):
    id: str
    content: str
    paper_id: Optional[str]
    project_id: Optional[str]
    user_id: str
    is_public: bool
    created_at: datetime
    updated_at: datetime


# In-memory storage for demo
notes_db: dict = {}


@router.get("/", response_model=List[Note])
async def list_notes(
    paper_id: Optional[str] = None,
    project_id: Optional[str] = None,
    user_id: str = "default",
):
    """List notes for user"""
    notes = list(notes_db.values())

    if paper_id:
        notes = [n for n in notes if n.paper_id == paper_id]
    if project_id:
        notes = [n for n in notes if n.project_id == project_id]

    notes = [
        n
        for n in notes
        if n.user_id == user_id or (n.is_public and n.user_id != user_id)
    ]

    return sorted(notes, key=lambda x: x.updated_at, reverse=True)


@router.post("/", response_model=Note)
async def create_note(note: NoteCreate, user_id: str = "default"):
    """Create a new note"""
    note_id = str(uuid.uuid4())
    now = datetime.utcnow()

    new_note = Note(
        id=note_id,
        content=note.content,
        paper_id=note.paper_id,
        project_id=note.project_id,
        user_id=user_id,
        is_public=note.is_public,
        created_at=now,
        updated_at=now,
    )

    notes_db[note_id] = new_note
    return new_note


@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str, user_id: str = "default"):
    """Get a note by ID"""
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != user_id and not note.is_public:
        raise HTTPException(status_code=403, detail="Access denied")
    return note


@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, update: NoteUpdate, user_id: str = "default"):
    """Update a note"""
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if update.content is not None:
        note.content = update.content
    if update.is_public is not None:
        note.is_public = update.is_public

    note.updated_at = datetime.utcnow()
    return note


@router.delete("/{note_id}")
async def delete_note(note_id: str, user_id: str = "default"):
    """Delete a note"""
    note = notes_db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    del notes_db[note_id]
    return {"message": "Note deleted"}
