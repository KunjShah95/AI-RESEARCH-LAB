"""Citation Graph API - Build and analyze citation networks"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional

try:
    from app.engines.citation_graph import (
        CitationGraphEngine,
        CitationRecommendationEngine,
        CitationAnalysisEngine,
        CitationChainTracer,
        NetworkVisualizationGenerator,
    )
except ImportError:
    from app.engines.citation_graph import CitationGraphEngine

    CitationRecommendationEngine = None
    CitationAnalysisEngine = None
    CitationChainTracer = None
    NetworkVisualizationGenerator = None

try:
    from app.auth import get_current_user
except ImportError:

    def get_current_user():
        return None


router = APIRouter(prefix="/api/graph", tags=["citation-graph"])

citation_graph = CitationGraphEngine()


class PaperInput(BaseModel):
    id: str
    title: str
    year: int
    citations: int = 0
    references: List[str] = []


class GraphBuildRequest(BaseModel):
    papers: List[PaperInput]


class PathRequest(BaseModel):
    source_id: str
    target_id: str
    max_depth: int = 10


class SubgraphRequest(BaseModel):
    paper_ids: List[str]
    include_references: int = 1


@router.post("/build")
async def build_graph(
    request: GraphBuildRequest, current_user=Depends(get_current_user)
):
    """Build citation graph from papers"""
    papers_data = [p.model_dump() for p in request.papers]
    citation_graph.build_from_papers(papers_data)

    metrics = citation_graph.get_graph_metrics()

    return {
        "status": "success",
        "metrics": {
            "total_nodes": metrics.total_nodes,
            "total_edges": metrics.total_edges,
            "density": round(metrics.density, 4),
            "avg_degree": round(metrics.avg_degree, 2),
            "diameter": metrics.diameter,
            "connected_components": metrics.connected_components,
        },
    }


@router.get("/metrics")
async def get_metrics(current_user=Depends(get_current_user)):
    """Get graph metrics"""
    metrics = citation_graph.get_graph_metrics()

    return {
        "total_nodes": metrics.total_nodes,
        "total_edges": metrics.total_edges,
        "density": round(metrics.density, 4),
        "avg_degree": round(metrics.avg_degree, 2),
        "diameter": metrics.diameter,
        "clustering_coef": round(metrics.clustering_coef, 4),
        "connected_components": metrics.connected_components,
    }


@router.post("/path")
async def find_path(request: PathRequest, current_user=Depends(get_current_user)):
    """Find shortest path between two papers"""
    result = citation_graph.find_shortest_path(
        request.source_id, request.target_id, request.max_depth
    )

    return {
        "exists": result.exists,
        "length": result.length,
        "path": result.path,
        "papers": result.papers,
    }


@router.get("/papers/{paper_id}/citations")
async def get_paper_citations(paper_id: str, current_user=Depends(get_current_user)):
    """Get papers that this paper cites"""
    citations = citation_graph.get_paper_citations(paper_id)

    return {
        "paper_id": paper_id,
        "citations": [
            {
                "id": p.paper_id,
                "title": p.title,
                "year": p.year,
                "citations_count": p.citations_count,
            }
            for p in citations
        ],
    }


@router.get("/papers/{paper_id}/cited-by")
async def get_cited_by(paper_id: str, current_user=Depends(get_current_user)):
    """Get papers that cite this paper"""
    cited_by = citation_graph.get_paper_cited_by(paper_id)

    return {
        "paper_id": paper_id,
        "cited_by": [
            {
                "id": p.paper_id,
                "title": p.title,
                "year": p.year,
                "citations_count": p.citations_count,
            }
            for p in cited_by
        ],
    }


@router.get("/influential")
async def get_influential_papers(
    metric: str = "pagerank", top_k: int = 10, current_user=Depends(get_current_user)
):
    """Get most influential papers"""
    papers = citation_graph.get_influential_papers(metric, top_k)

    return {
        "metric": metric,
        "papers": [
            {
                "id": pid,
                "score": round(score, 4),
                "title": citation_graph.nodes.get(pid, {}).title
                if pid in citation_graph.nodes
                else "",
                "year": citation_graph.nodes.get(pid, {}).year
                if pid in citation_graph.nodes
                else 0,
            }
            for pid, score in papers
        ],
    }


@router.post("/subgraph")
async def get_subgraph(
    request: SubgraphRequest, current_user=Depends(get_current_user)
):
    """Get subgraph centered on specific papers"""
    subgraph = citation_graph.get_subgraph(
        request.paper_ids, request.include_references
    )

    return subgraph.export_graph_json()


@router.get("/pagerank")
async def get_pagerank(current_user=Depends(get_current_user)):
    """Get PageRank scores for all papers"""
    ranks = citation_graph.calculate_pagerank()

    sorted_ranks = sorted(ranks.items(), key=lambda x: x[1], reverse=True)

    return {
        "pagerank": [
            {"id": pid, "score": round(score, 6)} for pid, score in sorted_ranks[:50]
        ]
    }


@router.get("/cycles")
async def get_cycles(max_length: int = 6, current_user=Depends(get_current_user)):
    """Find citation cycles"""
    cycles = citation_graph.find_citation_cycles(max_length)

    return {"cycles_count": len(cycles), "cycles": cycles[:10]}


@router.get("/trends/{paper_id}")
async def get_citation_trends(paper_id: str, current_user=Depends(get_current_user)):
    """Get citation trends for a paper"""
    trends = citation_graph.get_citation_trends(paper_id)

    return {"paper_id": paper_id, "trends": trends}


@router.get("/impact/{paper_id}")
async def get_impact(
    paper_id: str, year: Optional[int] = None, current_user=Depends(get_current_user)
):
    """Get impact factor for a paper"""
    impact = citation_graph.calculate_impact_factor(paper_id, year)

    return {"paper_id": paper_id, "year": year, "impact_factor": impact}


@router.get("/neighbors/{paper_id}")
async def get_neighbors(
    paper_id: str,
    depth: int = 1,
    direction: str = "both",
    current_user=Depends(get_current_user),
):
    """Get neighboring papers"""
    neighbors = citation_graph.get_neighbors(paper_id, depth, direction)

    return {
        "paper_id": paper_id,
        "depth": depth,
        "direction": direction,
        "neighbors": list(neighbors),
        "count": len(neighbors),
    }


@router.get("/export")
async def export_graph(current_user=Depends(get_current_user)):
    """Export entire graph as JSON"""
    return citation_graph.export_graph_json()


@router.post("/reset")
async def reset_graph(current_user=Depends(get_current_user)):
    """Reset the citation graph"""
    global citation_graph
    citation_graph = CitationGraphEngine()

    return {"status": "success", "message": "Graph reset successfully"}


# ===== NEW ADVANCED FEATURES =====


@router.get("/recommendations/{paper_id}")
async def get_recommendations(
    paper_id: str,
    top_k: int = 10,
    method: str = "combined",
    current_user=Depends(get_current_user),
):
    """Get similar paper recommendations"""
    if CitationRecommendationEngine is None:
        return {"error": "Feature not available"}

    rec_engine = CitationRecommendationEngine(citation_graph)
    results = rec_engine.get_similar_papers(paper_id, top_k, method)

    return {
        "paper_id": paper_id,
        "method": method,
        "recommendations": [
            {
                "paper_id": r.paper_id,
                "title": r.title,
                "year": r.year,
                "score": r.score,
                "reason": r.reason,
            }
            for r in results
        ],
    }


@router.get("/analysis/{paper_id}")
async def get_paper_analysis(paper_id: str, current_user=Depends(get_current_user)):
    """Get comprehensive analysis for a paper"""
    if CitationAnalysisEngine is None:
        return {"error": "Feature not available"}

    ana_engine = CitationAnalysisEngine(citation_graph)

    return {
        "paper_id": paper_id,
        "h_index": ana_engine.calculate_h_index(paper_id),
        "i10_index": ana_engine.calculate_i10_index(paper_id),
        "avg_citation_age": ana_engine.calculate_citation_age(paper_id),
        "citation_distribution": ana_engine.get_citation_distribution(paper_id),
    }


@router.get("/chains/backwards/{paper_id}")
async def trace_backwards(
    paper_id: str, max_depth: int = 5, current_user=Depends(get_current_user)
):
    """Trace citation chain backwards (references)"""
    if CitationChainTracer is None:
        return {"error": "Feature not available"}

    tracer = CitationChainTracer(citation_graph)
    chain = tracer.trace_backwards(paper_id, max_depth)

    return {"paper_id": paper_id, "chain": chain}


@router.get("/chains/forwards/{paper_id}")
async def trace_forwards(
    paper_id: str, max_depth: int = 5, current_user=Depends(get_current_user)
):
    """Trace citation chain forwards (cited by)"""
    if CitationChainTracer is None:
        return {"error": "Feature not available"}

    tracer = CitationChainTracer(citation_graph)
    chain = tracer.trace_forwards(paper_id, max_depth)

    return {"paper_id": paper_id, "chain": chain}


@router.get("/visualization/d3")
async def get_d3_visualization(
    paper_ids: Optional[str] = None,
    include_neighbors: int = 1,
    current_user=Depends(get_current_user),
):
    """Get D3.js compatible visualization data"""
    if NetworkVisualizationGenerator is None:
        return {"error": "Feature not available"}

    viz = NetworkVisualizationGenerator(citation_graph)

    paper_list = paper_ids.split(",") if paper_ids else None
    data = viz.generate_d3_json(paper_list, include_neighbors)

    return data


@router.get("/visualization/cytoscape")
async def get_cytoscape_visualization(
    paper_ids: Optional[str] = None, current_user=Depends(get_current_user)
):
    """Get Cytoscape.js compatible visualization data"""
    if NetworkVisualizationGenerator is None:
        return {"error": "Feature not available"}

    viz = NetworkVisualizationGenerator(citation_graph)

    paper_list = paper_ids.split(",") if paper_ids else None
    data = viz.generate_cytoscape_json(paper_list)

    return data


@router.get("/bridges")
async def get_citation_bridges(top_k: int = 10, current_user=Depends(get_current_user)):
    """Get papers that bridge different research areas"""
    if CitationAnalysisEngine is None:
        return {"error": "Feature not available"}

    ana_engine = CitationAnalysisEngine(citation_graph)
    bridges = ana_engine.identify_citation_bridges(top_k)

    return {
        "bridges": [
            {
                "paper_id": pid,
                "score": round(score, 2),
                "title": citation_graph.nodes.get(pid).title
                if pid in citation_graph.nodes
                else "",
            }
            for pid, score in bridges
        ]
    }


@router.get("/frontier/{paper_id}")
async def get_research_frontier(
    paper_id: str, depth: int = 2, current_user=Depends(get_current_user)
):
    """Get papers representing the research frontier"""
    if CitationAnalysisEngine is None:
        return {"error": "Feature not available"}

    ana_engine = CitationAnalysisEngine(citation_graph)
    frontier = ana_engine.get_research_frontier(paper_id, depth)

    return {"paper_id": paper_id, "frontier": frontier}


@router.get("/velocity/{paper_id}")
async def get_citation_velocity(
    paper_id: str, years: int = 3, current_user=Depends(get_current_user)
):
    """Get citation velocity over time"""
    if CitationAnalysisEngine is None:
        return {"error": "Feature not available"}

    ana_engine = CitationAnalysisEngine(citation_graph)
    velocity = ana_engine.get_citation_velocity(paper_id, years)

    return {"paper_id": paper_id, "velocity": velocity}
