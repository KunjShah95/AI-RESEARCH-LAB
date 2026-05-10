"""Test pydantic models"""

import pytest
from uuid import uuid4
from datetime import datetime
from app.models.paper import Paper, Author
from app.models.citation import Citation
from app.models.evaluation import Evaluation, EvaluationResult


def test_paper_model_validation():
    paper = Paper(
        id=uuid4(),
        source="arxiv",
        external_id="2301.12345",
        title="Test Paper",
        authors=[Author(name="John Doe", orcid=None)],
        abstract="Test abstract",
        year=2024,
        created_at=datetime.now(),
    )
    assert paper.source == "arxiv"
    assert paper.title == "Test Paper"


def test_author_model():
    author = Author(name="Jane Doe", affiliation="MIT")
    assert author.name == "Jane Doe"
    assert author.affiliation == "MIT"


def test_citation_model():
    citation = Citation(
        id=uuid4(),
        paper_id=uuid4(),
        snippet="Test snippet",
        page_ref="page 1",
        created_at=datetime.now(),
    )
    assert citation.snippet == "Test snippet"


def test_evaluation_model():
    eval_model = Evaluation(
        id=uuid4(),
        eval_type="agent",
        target_id=uuid4(),
        score=0.85,
        metrics={"accuracy": 0.9},
        created_at=datetime.now(),
    )
    assert eval_model.eval_type == "agent"
    assert eval_model.score == 0.85
