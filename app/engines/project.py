"""Project management for paper collections"""

from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class Project(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    papers: List[str] = []
    created_at: datetime
    updated_at: datetime


class ProjectManager:
    """Manager for research projects and shortlists"""

    def __init__(self):
        self._projects = {}

    def create_project(self, name: str, description: str = None) -> Project:
        """Create a new project"""
        project = Project(
            id=UUID(),
            name=name,
            description=description,
            papers=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        self._projects[str(project.id)] = project
        return project

    def get_project(self, project_id: UUID) -> Optional[Project]:
        """Get project by ID"""
        return self._projects.get(str(project_id))

    def list_projects(self) -> List[Project]:
        """List all projects"""
        return list(self._projects.values())

    def add_paper_to_project(self, project_id: UUID, paper_id: str) -> bool:
        """Add paper to project shortlist"""
        project = self._projects.get(str(project_id))
        if project:
            if paper_id not in project.papers:
                project.papers.append(paper_id)
                project.updated_at = datetime.now()
            return True
        return False

    def remove_paper_from_project(self, project_id: UUID, paper_id: str) -> bool:
        """Remove paper from project"""
        project = self._projects.get(str(project_id))
        if project:
            if paper_id in project.papers:
                project.papers.remove(paper_id)
                project.updated_at = datetime.now()
            return True
        return False

    def get_project_papers(self, project_id: UUID) -> List[str]:
        """Get all paper IDs in project"""
        project = self._projects.get(str(project_id))
        return project.papers if project else []

    def delete_project(self, project_id: UUID) -> bool:
        """Delete a project"""
        if str(project_id) in self._projects:
            del self._projects[str(project_id)]
            return True
        return False


project_manager = ProjectManager()
