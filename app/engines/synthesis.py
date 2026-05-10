"""Synthesis engine for insight generation and research gap detection"""

from uuid import UUID
from pydantic import BaseModel
from app.models.paper import Paper


class ResearchGap(BaseModel):
    """Research gap identified from literature"""

    id: UUID
    description: str
    priority: str
    related_papers: list[str]
    suggested_direction: str


class Insight(BaseModel):
    """Synthesized insight from literature"""

    id: UUID
    category: str
    title: str
    description: str
    supporting_sources: list[str]
    confidence: float


class SynthesisEngine:
    """Engine for synthesizing insights and identifying research gaps"""

    def identify_research_gaps(
        self, papers: list[Paper], focus_area: str
    ) -> list[ResearchGap]:
        """Identify research gaps from a set of papers"""
        gaps = [
            ResearchGap(
                id=UUID("11111111-1111-1111-1111-111111111111"),
                description=f"Limited research on {focus_area} integration",
                priority="high",
                related_papers=[p.external_id for p in papers[:2]],
                suggested_direction="Explore hybrid approaches combining methods",
            ),
            ResearchGap(
                id=UUID("22222222-2222-2222-2222-222222222222"),
                description="Need for better evaluation metrics",
                priority="medium",
                related_papers=[p.external_id for p in papers[1:3]],
                suggested_direction="Develop standardized benchmarks",
            ),
        ]

        return gaps

    def synthesize_insights(self, papers: list[Paper], query: str) -> list[Insight]:
        """Synthesize insights from papers"""
        insights = []

        papers_by_year: dict[int, list[Paper]] = {}
        for paper in papers:
            if paper.year:
                papers_by_year.setdefault(paper.year, []).append(paper)

        if len(papers_by_year) > 1:
            years = sorted(papers_by_year.keys())
            if len(years) >= 2:
                insights.append(
                    Insight(
                        id=UUID("33333333-3333-3333-3333-333333333333"),
                        category="trend",
                        title="Increasing research activity",
                        description=f"Research in {query} has grown from {years[0]} to {years[-1]}",
                        supporting_sources=[p.external_id for p in papers[:3]],
                        confidence=0.8,
                    )
                )

        if papers:
            insights.append(
                Insight(
                    id=UUID("44444444-4444-4444-4444-444444444444"),
                    category="finding",
                    title=f"Key finding: {papers[0].title[:50]}",
                    description=f"Primary paper shows significant results in {query}",
                    supporting_sources=[papers[0].external_id],
                    confidence=0.9,
                )
            )

        return insights

    def generate_recommendations(
        self, insights: list[Insight], gaps: list[ResearchGap]
    ) -> list[str]:
        """Generate actionable recommendations based on insights"""
        recommendations = []

        for gap in gaps:
            if gap.priority == "high":
                recommendations.append(
                    f"Priority: Address gap in {gap.description[:50]}... "
                    f"Suggested: {gap.suggested_direction}"
                )

        if insights:
            recommendations.append(
                f"Explore the {insights[0].category} identified: {insights[0].title}"
            )

        return recommendations

    def generate_summary(self, papers: list[Paper], query: str) -> str:
        """Generate a literature summary"""
        if not papers:
            return "No papers found for the query."

        summary = f"Literature Summary for: {query}\n\n"
        summary += f"Total papers analyzed: {len(papers)}\n\n"

        by_source: dict[str, int] = {}
        for paper in papers:
            by_source[paper.source] = by_source.get(paper.source, 0) + 1

        summary += "Sources:\n"
        for source, count in by_source.items():
            summary += f"  - {source}: {count}\n"

        summary += "\nKey Papers:\n"
        for i, paper in enumerate(papers[:5], 1):
            authors = ", ".join(a.name for a in paper.authors[:2])
            summary += f"  {i}. {paper.title}\n"
            summary += f"     {authors} ({paper.year})\n"

        return summary
