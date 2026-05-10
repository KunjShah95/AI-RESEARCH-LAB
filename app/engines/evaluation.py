"""Evaluation engine for assessing agent, paper, and summary quality"""

from enum import Enum
from uuid import UUID
from typing import Any
from app.models.evaluation import EvaluationCreate, Evaluation, EvaluationResult


class EvalType(str, Enum):
    """Types of evaluations"""

    AGENT = "agent"
    PAPER = "paper"
    SUMMARY = "summary"


class EvaluationEngine:
    """Engine for evaluating various outputs"""

    def evaluate_agent_performance(
        self,
        task_id: UUID,
        agent_name: str,
        output: str,
        expected_output: str | None = None,
    ) -> EvaluationResult:
        """Evaluate agent output quality"""
        metrics = {
            "output_length": len(output),
            "has_citations": "[Source:" in output,
        }

        score = 0.8 if "[Source:" in output else 0.5

        eval_create = EvaluationCreate(
            eval_type=EvalType.AGENT,
            target_id=task_id,
            score=score,
            metrics=metrics,
            details=f"Agent: {agent_name}",
        )

        return EvaluationResult(
            evaluation=Evaluation(**eval_create.model_dump()),
            passed=score >= 0.7,
            feedback="Agent output contains citations"
            if score >= 0.7
            else "Missing citations",
        )

    def evaluate_paper_quality(
        self, paper_id: UUID, abstract: str, title: str
    ) -> EvaluationResult:
        """Evaluate paper metadata quality"""
        metrics = {
            "title_length": len(title),
            "abstract_length": len(abstract) if abstract else 0,
            "has_abstract": bool(abstract),
        }

        score = 0.7
        if len(title) > 10:
            score += 0.1
        if abstract and len(abstract) > 100:
            score += 0.2

        eval_create = EvaluationCreate(
            eval_type=EvalType.PAPER,
            target_id=paper_id,
            score=min(score, 1.0),
            metrics=metrics,
            details=f"Title: {title[:50]}...",
        )

        return EvaluationResult(
            evaluation=Evaluation(**eval_create.model_dump()),
            passed=score >= 0.7,
            feedback="Paper metadata is complete"
            if score >= 0.7
            else "Paper metadata incomplete",
        )

    def evaluate_summary_quality(
        self, summary: str, source_count: int
    ) -> EvaluationResult:
        """Evaluate generated summary quality"""
        metrics = {
            "summary_length": len(summary),
            "source_count": source_count,
            "citation_density": source_count / max(len(summary), 1) * 1000,
        }

        score = 0.5

        if "[Source:" in summary:
            score += 0.2
        if len(summary) > 100:
            score += 0.1
        if source_count >= 3:
            score += 0.2

        eval_create = EvaluationCreate(
            eval_type=EvalType.SUMMARY,
            target_id=UUID("00000000-0000-0000-0000-000000000000"),
            score=min(score, 1.0),
            metrics=metrics,
            details=f"Sources: {source_count}",
        )

        return EvaluationResult(
            evaluation=Evaluation(**eval_create.model_dump()),
            passed=score >= 0.7,
            feedback="Summary meets quality criteria"
            if score >= 0.7
            else "Summary needs improvement",
        )

    def batch_evaluate(
        self, eval_type: EvalType, targets: list[dict[str, Any]]
    ) -> list[EvaluationResult]:
        """Evaluate multiple targets"""
        results = []

        for target in targets:
            if eval_type == EvalType.AGENT:
                result = self.evaluate_agent_performance(
                    target["task_id"], target["agent_name"], target["output"]
                )
            elif eval_type == EvalType.PAPER:
                result = self.evaluate_paper_quality(
                    target["paper_id"], target["abstract"], target["title"]
                )
            else:
                result = self.evaluate_summary_quality(
                    target["summary"], target["source_count"]
                )

            results.append(result)

        return results
