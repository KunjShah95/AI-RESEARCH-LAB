"""Core engines"""

from app.engines.diff import PaperDiffEngine, PaperDiff, DiffSection
from app.engines.evaluation import EvaluationEngine, EvalType
from app.engines.citation import CitationEngine
from app.engines.citation_formatter import CitationFormatter, CitationStyle
from app.engines.synthesis import SynthesisEngine, Insight, ResearchGap
from app.engines.comparison import ComparisonEngine
from app.engines.export import ExportEngine
from app.engines.dedup import DuplicateDetector
from app.engines.project import ProjectManager, Project, project_manager
from app.engines.pdf_export import PDFExportEngine
from app.engines.rss_monitor import RSSMonitor, rss_monitor
from app.engines.qa_chat import QAChatEngine, qa_chat_engine
from app.engines.discovery import RelatedPaperDiscovery, related_discovery
from app.engines.advanced_search import (
    AdvancedSearchEngine,
    advanced_search_engine,
    SearchType,
    SearchFilters,
    SearchResult,
)


__all__ = [
    "PaperDiffEngine",
    "PaperDiff",
    "DiffSection",
    "EvaluationEngine",
    "EvalType",
    "CitationEngine",
    "CitationFormatter",
    "CitationStyle",
    "SynthesisEngine",
    "Insight",
    "ResearchGap",
    "ComparisonEngine",
    "ExportEngine",
    "DuplicateDetector",
    "ProjectManager",
    "Project",
    "project_manager",
    "PDFExportEngine",
    "RSSMonitor",
    "rss_monitor",
    "QAChatEngine",
    "qa_chat_engine",
    "RelatedPaperDiscovery",
    "related_discovery",
    "AdvancedSearchEngine",
    "advanced_search_engine",
    "SearchType",
    "SearchFilters",
    "SearchResult",
]
