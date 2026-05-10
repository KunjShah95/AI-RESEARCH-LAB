"""Projects API - user project management"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid


router = APIRouter()


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Project(BaseModel):
    id: str
    name: str
    description: Optional[str]
    user_id: str
    paper_count: int
    created_at: datetime
    updated_at: datetime


class ProjectPaperAdd(BaseModel):
    paper_id: str
    source: str
    notes: Optional[str] = None


class ProjectPaper(BaseModel):
    paper_id: str
    source: str
    notes: Optional[str]
    added_at: datetime


# In-memory storage for demo (replace with database in production)
projects_db: dict = {}
project_papers_db: dict = {}


@router.get("/", response_model=List[Project])
async def list_projects(user_id: str = "default"):
    """List all projects for a user"""
    user_projects = [p for p in projects_db.values() if p.user_id == user_id]
    return sorted(user_projects, key=lambda x: x.updated_at, reverse=True)


@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate, user_id: str = "default"):
    """Create a new project"""
    project_id = str(uuid.uuid4())
    now = datetime.utcnow()

    new_project = Project(
        id=project_id,
        name=project.name,
        description=project.description,
        user_id=user_id,
        paper_count=0,
        created_at=now,
        updated_at=now,
    )

    projects_db[project_id] = new_project
    project_papers_db[project_id] = []

    return new_project


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str, user_id: str = "default"):
    """Get a project by ID"""
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    project.paper_count = len(project_papers_db.get(project_id, []))
    return project


@router.put("/{project_id}", response_model=Project)
async def update_project(
    project_id: str, update: ProjectUpdate, user_id: str = "default"
):
    """Update a project"""
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    if update.name:
        project.name = update.name
    if update.description is not None:
        project.description = update.description

    project.updated_at = datetime.utcnow()
    return project


@router.delete("/{project_id}")
async def delete_project(project_id: str, user_id: str = "default"):
    """Delete a project"""
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    del projects_db[project_id]
    if project_id in project_papers_db:
        del project_papers_db[project_id]

    return {"message": "Project deleted"}


@router.get("/{project_id}/papers", response_model=List[ProjectPaper])
async def get_project_papers(project_id: str, user_id: str = "default"):
    """Get papers in a project"""
    project = projects_db.get(project_id)
    if not project or project.user_id != user_id:
        raise HTTPException(status_code=404, detail="Project not found")

    return project_papers_db.get(project_id, [])


@router.post("/{project_id}/papers")
async def add_paper_to_project(
    project_id: str, paper: ProjectPaperAdd, user_id: str = "default"
):
    """Add a paper to a project"""
    project = projects_db.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    project_papers = project_papers_db.get(project_id, [])

    if any(p.paper_id == paper.paper_id for p in project_papers):
        raise HTTPException(status_code=400, detail="Paper already in project")

    project_paper = ProjectPaper(
        paper_id=paper.paper_id,
        source=paper.source,
        notes=paper.notes,
        added_at=datetime.utcnow(),
    )

    project_papers.append(project_paper)
    project_papers_db[project_id] = project_papers

    project.paper_count = len(project_papers)
    project.updated_at = datetime.utcnow()

    return project_paper


@router.delete("/{project_id}/papers/{paper_id}")
async def remove_paper_from_project(
    project_id: str, paper_id: str, user_id: str = "default"
):
    """Remove a paper from a project"""
    project = projects_db.get(project_id)
    if not project or project.user_id != user_id:
        raise HTTPException(status_code=404, detail="Project not found")

    project_papers = project_papers_db.get(project_id, [])
    project_papers = [p for p in project_papers if p.paper_id != paper_id]
    project_papers_db[project_id] = project_papers

    project.paper_count = len(project_papers)
    project.updated_at = datetime.utcnow()

    return {"message": "Paper removed"}
