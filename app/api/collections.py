"""Research Collections API - paper collections with sharing"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid


router = APIRouter()


class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    tags: Optional[List[str]] = []


class Collection(BaseModel):
    id: str
    name: str
    description: Optional[str]
    user_id: str
    is_public: bool
    tags: List[str]
    paper_count: int
    version: int
    created_at: datetime
    updated_at: datetime


class CollectionVersion(BaseModel):
    version: int
    changes: str
    created_at: datetime


collections_db: dict = {}
collection_versions: dict = {}
collection_papers: dict = {}


@router.get("/", response_model=List[Collection])
async def list_collections(user_id: str = "default", public_only: bool = False):
    """List user's collections"""
    collections = list(collections_db.values())

    if public_only:
        collections = [c for c in collections if c.is_public]
    else:
        collections = [c for c in collections if c.user_id == user_id or c.is_public]

    return sorted(collections, key=lambda x: x.updated_at, reverse=True)


@router.post("/", response_model=Collection)
async def create_collection(collection: CollectionCreate, user_id: str = "default"):
    """Create a new collection"""
    collection_id = str(uuid.uuid4())
    now = datetime.utcnow()

    new_collection = Collection(
        id=collection_id,
        name=collection.name,
        description=collection.description,
        user_id=user_id,
        is_public=collection.is_public,
        tags=collection.tags or [],
        paper_count=0,
        version=1,
        created_at=now,
        updated_at=now,
    )

    collections_db[collection_id] = new_collection
    collection_papers[collection_id] = []
    collection_versions[collection_id] = [
        CollectionVersion(version=1, changes="Initial version", created_at=now)
    ]

    return new_collection


@router.get("/{collection_id}", response_model=Collection)
async def get_collection(collection_id: str, user_id: str = "default"):
    """Get collection by ID"""
    collection = collections_db.get(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    if not collection.is_public and collection.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    collection.paper_count = len(collection_papers.get(collection_id, []))
    return collection


@router.put("/{collection_id}", response_model=Collection)
async def update_collection(
    collection_id: str, collection: CollectionCreate, user_id: str = "default"
):
    """Update collection (creates new version)"""
    existing = collections_db.get(collection_id)
    if not existing or existing.user_id != user_id:
        raise HTTPException(status_code=404, detail="Collection not found")

    existing.name = collection.name
    existing.description = collection.description
    existing.is_public = collection.is_public
    existing.tags = collection.tags or []
    existing.version += 1
    existing.updated_at = datetime.utcnow()

    version = CollectionVersion(
        version=existing.version,
        changes=f"Updated: {collection.name}",
        created_at=datetime.utcnow(),
    )
    collection_versions[collection_id].append(version)

    return existing


@router.delete("/{collection_id}")
async def delete_collection(collection_id: str, user_id: str = "default"):
    """Delete collection"""
    collection = collections_db.get(collection_id)
    if not collection or collection.user_id != user_id:
        raise HTTPException(status_code=404, detail="Collection not found")

    del collections_db[collection_id]
    if collection_id in collection_papers:
        del collection_papers[collection_id]

    return {"message": "Collection deleted"}


@router.get("/{collection_id}/versions")
async def get_collection_versions(collection_id: str):
    """Get collection version history"""
    return collection_versions.get(collection_id, [])


@router.post("/{collection_id}/share")
async def share_collection(collection_id: str, user_id: str = "default"):
    """Generate share link for collection"""
    collection = collections_db.get(collection_id)
    if not collection or collection.user_id != user_id:
        raise HTTPException(status_code=404, detail="Collection not found")

    import secrets

    share_token = secrets.token_urlsafe(16)

    return {
        "collection_id": collection_id,
        "share_link": f"/collections/shared/{share_token}",
        "public": collection.is_public,
    }
