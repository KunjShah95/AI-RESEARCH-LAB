"""Paper Diff Engine - side-by-side paper comparison with diff view"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from difflib import SequenceMatcher, unified_diff, HtmlDiff
from app.models.paper import Paper


@dataclass
class DiffSection:
    section_name: str
    left_content: str
    right_content: str
    similarity: float
    changes: List[Dict]


@dataclass
class PaperDiff:
    left_paper: str
    right_paper: str
    overall_similarity: float
    sections: List[DiffSection]
    added_lines: List[str]
    removed_lines: List[str]
    modified_sections: List[str]


class PaperDiffEngine:
    """Engine for comparing papers side-by-side with diff view"""

    def __init__(self):
        self.comparison_fields = [
            "title",
            "abstract",
            "methods",
            "results",
            "conclusions",
        ]

    def compare_papers(self, paper1: Paper, paper2: Paper) -> PaperDiff:
        """Compare two papers and return detailed diff"""
        sections = []
        total_similarity = 0

        for field in self.comparison_fields:
            left_val = self._get_field(paper1, field)
            right_val = self._get_field(paper2, field)

            similarity = self._calculate_similarity(left_val, right_val)
            changes = self._find_changes(left_val, right_val)

            diff_section = DiffSection(
                section_name=field.replace("_", " ").title(),
                left_content=left_val[:500] if left_val else "",
                right_content=right_val[:500] if right_val else "",
                similarity=similarity,
                changes=changes,
            )
            sections.append(diff_section)
            total_similarity += similarity

        overall_similarity = total_similarity / len(self.comparison_fields)

        added, removed = self._find_line_changes(
            paper1.abstract or "", paper2.abstract or ""
        )

        return PaperDiff(
            left_paper=paper1.title,
            right_paper=paper2.title,
            overall_similarity=overall_similarity,
            sections=sections,
            added_lines=added,
            removed_lines=removed,
            modified_sections=[s.section_name for s in sections if s.similarity < 0.8],
        )

    def _get_field(self, paper: Paper, field: str) -> str:
        """Get field value from paper"""
        if field == "title":
            return paper.title or ""
        elif field == "abstract":
            return paper.abstract or ""
        elif field == "methods":
            return getattr(paper, "methods", "") or ""
        elif field == "results":
            return getattr(paper, "results", "") or ""
        elif field == "conclusions":
            return getattr(paper, "conclusions", "") or ""
        return ""

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1, text2).ratio()

    def _find_changes(self, text1: str, text2: str) -> List[Dict]:
        """Find specific changes between texts"""
        changes = []

        lines1 = text1.split("\n")
        lines2 = text2.split("\n")

        matcher = SequenceMatcher(None, lines1, lines2)
        opcodes = matcher.get_opcodes()

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "replace":
                changes.append(
                    {"type": "modified", "left": lines1[i1:i2], "right": lines2[j1:j2]}
                )
            elif tag == "delete":
                changes.append({"type": "removed", "content": lines1[i1:i2]})
            elif tag == "insert":
                changes.append({"type": "added", "content": lines2[j1:j2]})

        return changes

    def _find_line_changes(self, text1: str, text2: str) -> Tuple[List[str], List[str]]:
        """Find added and removed lines"""
        lines1 = set(text1.split("\n"))
        lines2 = set(text2.split("\n"))

        added = list(lines2 - lines1)
        removed = list(lines1 - lines2)

        return added[:20], removed[:20]

    def generate_unified_diff(
        self, text1: str, text1_name: str, text2: str, text2_name: str
    ) -> str:
        """Generate unified diff format"""
        lines1 = text1.split("\n")
        lines2 = text2.split("\n")

        diff = list(
            unified_diff(
                lines1, lines2, fromfile=text1_name, tofile=text2_name, lineterm=""
            )
        )

        return "\n".join(diff)

    def generate_html_diff(self, text1: str, text2: str) -> str:
        """Generate HTML side-by-side diff"""
        html_diff = HtmlDiff()
        return html_diff.make_file(
            text1.split("\n"), text2.split("\n"), context=True, numlines=3
        )

    def compare_multiple(self, papers: List[Paper]) -> List[PaperDiff]:
        """Compare multiple papers against each other"""
        diffs = []

        for i in range(len(papers)):
            for j in range(i + 1, len(papers)):
                diff = self.compare_papers(papers[i], papers[j])
                diffs.append(diff)

        return sorted(diffs, key=lambda x: x.overall_similarity, reverse=True)
