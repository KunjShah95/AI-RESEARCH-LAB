"""Pytest configuration and fixtures"""

import pytest
from app.config import Settings


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    return Settings(
        database_url="postgresql://localhost:5432/test", openai_api_key=None
    )


@pytest.fixture
def sample_paper():
    """Sample paper for testing"""
    from app.models.paper import Paper, Author
    from datetime import datetime
    from uuid import uuid4

    return Paper(
        id=uuid4(),
        source="arxiv",
        external_id="2301.00001",
        title="Test Paper on AI",
        authors=[Author(name="John Doe")],
        abstract="This is a test abstract",
        year=2024,
        doi=None,
        open_access=True,
        created_at=datetime.now(),
    )
