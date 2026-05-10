"""Citation Graph Engine - Build and analyze citation networks"""

from typing import List, Dict, Set, Optional, Tuple
from dataclasses import dataclass
from collections import deque


@dataclass
class CitationNode:
    """Node representing a paper in the citation graph"""

    paper_id: str
    title: str
    year: int
    citations_count: int = 0
    references_count: int = 0
    h_index: int = 0


@dataclass
class CitationEdge:
    """Edge representing citation relationship"""

    from_paper_id: str
    to_paper_id: str
    edge_type: str  # "cites", "referenced_by"
    weight: float = 1.0


@dataclass
class GraphMetrics:
    """Metrics for citation graph analysis"""

    total_nodes: int
    total_edges: int
    density: float
    avg_degree: float
    diameter: Optional[int]
    clustering_coef: float
    connected_components: int


@dataclass
class PathResult:
    """Result of path finding between two papers"""

    path: List[str]
    length: int
    papers: List[dict]
    exists: bool


class CitationGraphEngine:
    """Engine for building and analyzing citation graphs"""

    def __init__(self):
        self.nodes: Dict[str, CitationNode] = {}
        self.edges: List[CitationEdge] = []
        self.adjacency_list: Dict[str, Set[str]] = {}
        self.reverse_adjacency: Dict[str, Set[str]] = {}

    def add_paper(
        self,
        paper_id: str,
        title: str,
        year: int,
        citations_count: int = 0,
        references: List[str] = None,
    ) -> CitationNode:
        """Add a paper node to the graph"""
        node = CitationNode(
            paper_id=paper_id,
            title=title,
            year=year,
            citations_count=citations_count,
            references_count=len(references) if references else 0,
        )

        self.nodes[paper_id] = node

        if paper_id not in self.adjacency_list:
            self.adjacency_list[paper_id] = set()
        if paper_id not in self.reverse_adjacency:
            self.reverse_adjacency[paper_id] = set()

        if references:
            for ref_id in references:
                self.add_citation(paper_id, ref_id)

        return node

    def add_citation(
        self, citing_paper_id: str, cited_paper_id: str, edge_type: str = "cites"
    ) -> CitationEdge:
        """Add a citation edge between two papers"""
        if citing_paper_id not in self.adjacency_list:
            self.adjacency_list[citing_paper_id] = set()
        if cited_paper_id not in self.reverse_adjacency:
            self.reverse_adjacency[cited_paper_id] = set()

        edge = CitationEdge(
            from_paper_id=citing_paper_id,
            to_paper_id=cited_paper_id,
            edge_type=edge_type,
        )

        self.adjacency_list[citing_paper_id].add(cited_paper_id)
        self.reverse_adjacency[cited_paper_id].add(citing_paper_id)
        self.edges.append(edge)

        if cited_paper_id in self.nodes:
            self.nodes[cited_paper_id].citations_count += 1

        return edge

    def build_from_papers(
        self, papers: List[dict], citation_data: Dict[str, List[str]] = None
    ) -> None:
        """Build citation graph from paper list"""
        for paper in papers:
            self.add_paper(
                paper_id=paper.get("id", ""),
                title=paper.get("title", ""),
                year=paper.get("year", 0),
                citations_count=paper.get("citations", 0),
                references=paper.get("references", []),
            )

        if citation_data:
            for citing_id, cited_ids in citation_data.items():
                for cited_id in cited_ids:
                    self.add_citation(citing_id, cited_id)

    def get_paper_citations(self, paper_id: str) -> List[CitationNode]:
        """Get papers that this paper cites"""
        if paper_id not in self.adjacency_list:
            return []

        return [
            self.nodes[ref_id]
            for ref_id in self.adjacency_list[paper_id]
            if ref_id in self.nodes
        ]

    def get_paper_cited_by(self, paper_id: str) -> List[CitationNode]:
        """Get papers that cite this paper"""
        if paper_id not in self.reverse_adjacency:
            return []

        return [
            self.nodes[cit_id]
            for cit_id in self.reverse_adjacency[paper_id]
            if cit_id in self.nodes
        ]

    def find_shortest_path(
        self, source_id: str, target_id: str, max_depth: int = 10
    ) -> PathResult:
        """Find shortest path between two papers using BFS"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return PathResult(path=[], length=-1, papers=[], exists=False)

        if source_id == target_id:
            return PathResult(
                path=[source_id],
                length=0,
                papers=[self._paper_to_dict(self.nodes[source_id])],
                exists=True,
            )

        visited = {source_id}
        queue = deque([(source_id, [source_id])])

        while queue:
            current, path = queue.popleft()

            if len(path) > max_depth:
                continue

            for neighbor in self.adjacency_list.get(current, []):
                if neighbor == target_id:
                    full_path = path + [neighbor]
                    papers = [self.nodes[pid] for pid in full_path if pid in self.nodes]
                    return PathResult(
                        path=full_path,
                        length=len(full_path) - 1,
                        papers=[self._paper_to_dict(p) for p in papers],
                        exists=True,
                    )

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return PathResult(path=[], length=-1, papers=[], exists=False)

    def find_all_paths(
        self, source_id: str, target_id: str, max_depth: int = 5
    ) -> List[List[str]]:
        """Find all paths between two papers (limited depth)"""
        if source_id not in self.nodes or target_id not in self.nodes:
            return []

        all_paths = []

        def dfs(current: str, path: List[str], visited: Set[str]):
            if current == target_id:
                all_paths.append(path.copy())
                return

            if len(path) >= max_depth:
                return

            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(neighbor, path, visited)
                    path.pop()
                    visited.remove(neighbor)

        dfs(source_id, [source_id], {source_id})
        return all_paths

    def calculate_pagerank(
        self, damping: float = 0.85, iterations: int = 100, tolerance: float = 1e-6
    ) -> Dict[str, float]:
        """Calculate PageRank for all papers"""
        if not self.nodes:
            return {}

        n = len(self.nodes)
        ranks = {node_id: 1.0 / n for node_id in self.nodes}

        for _ in range(iterations):
            new_ranks = {}
            delta = 0.0

            for node_id in self.nodes:
                rank_sum = 0.0

                for in_node in self.reverse_adjacency.get(node_id, []):
                    out_degree = len(self.adjacency_list.get(in_node, []))
                    if out_degree > 0:
                        rank_sum += ranks[in_node] / out_degree

                new_rank = (1 - damping) / n + damping * rank_sum
                new_ranks[node_id] = new_rank
                delta += abs(new_rank - ranks.get(node_id, 0))

            ranks = new_ranks

            if delta < tolerance:
                break

        return ranks

    def get_influential_papers(
        self, metric: str = "pagerank", top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Get most influential papers by metric"""
        if metric == "pagerank":
            scores = self.calculate_pagerank()
        elif metric == "citations":
            scores = {pid: node.citations_count for pid, node in self.nodes.items()}
        elif metric == "degree":
            scores = {
                pid: len(self.adjacency_list.get(pid, []))
                + len(self.reverse_adjacency.get(pid, []))
                for pid in self.nodes
            }
        else:
            scores = {pid: 0 for pid in self.nodes}

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def get_graph_metrics(self) -> GraphMetrics:
        """Calculate graph-level metrics"""
        n = len(self.nodes)
        m = len(self.edges)

        if n == 0:
            return GraphMetrics(
                total_nodes=0,
                total_edges=0,
                density=0,
                avg_degree=0,
                diameter=None,
                clustering_coef=0,
                connected_components=0,
            )

        total_degree = sum(
            len(self.adjacency_list.get(pid, set()))
            + len(self.reverse_adjacency.get(pid, set()))
            for pid in self.nodes
        )
        avg_degree = total_degree / n

        max_possible_edges = n * (n - 1)
        density = m / max_possible_edges if max_possible_edges > 0 else 0

        components = self._count_connected_components()

        diameter = self._calculate_diameter()

        clustering = self._calculate_clustering_coefficient()

        return GraphMetrics(
            total_nodes=n,
            total_edges=m,
            density=density,
            avg_degree=avg_degree,
            diameter=diameter,
            clustering_coef=clustering,
            connected_components=components,
        )

    def _count_connected_components(self) -> int:
        """Count connected components using BFS"""
        visited = set()
        components = 0

        for node_id in self.nodes:
            if node_id not in visited:
                components += 1
                queue = deque([node_id])

                while queue:
                    current = queue.popleft()
                    if current in visited:
                        continue

                    visited.add(current)

                    for neighbor in self.adjacency_list.get(current, []):
                        if neighbor not in visited:
                            queue.append(neighbor)
                    for neighbor in self.reverse_adjacency.get(current, []):
                        if neighbor not in visited:
                            queue.append(neighbor)

        return components

    def _calculate_diameter(self) -> Optional[int]:
        """Calculate graph diameter using BFS from each node"""
        if not self.nodes:
            return None

        max_distance = 0

        for start_id in self.nodes:
            distances = {start_id: 0}
            queue = deque([start_id])

            while queue:
                current = queue.popleft()
                for neighbor in self.adjacency_list.get(current, []):
                    if neighbor not in distances:
                        distances[neighbor] = distances[current] + 1
                        queue.append(neighbor)

                for neighbor in self.reverse_adjacency.get(current, []):
                    if neighbor not in distances:
                        distances[neighbor] = distances[current] + 1
                        queue.append(neighbor)

            if distances:
                max_distance = max(max_distance, max(distances.values()))

        return max_distance if max_distance > 0 else None

    def _calculate_clustering_coefficient(self) -> float:
        """Calculate average clustering coefficient"""
        if not self.nodes:
            return 0.0

        total_coef = 0.0
        nodes_with_edges = 0

        for node_id in self.nodes:
            neighbors = self.adjacency_list.get(node_id, set())
            k = len(neighbors)

            if k < 2:
                continue

            edges_between_neighbors = 0
            for n1 in neighbors:
                for n2 in neighbors:
                    if n1 != n2:
                        if n2 in self.adjacency_list.get(n1, set()):
                            edges_between_neighbors += 1

            max_edges = k * (k - 1)
            cluster_coef = (
                edges_between_neighbors / (2 * max_edges) if max_edges > 0 else 0
            )
            total_coef += cluster_coef
            nodes_with_edges += 1

        return total_coef / nodes_with_edges if nodes_with_edges > 0 else 0.0

    def _paper_to_dict(self, node: CitationNode) -> dict:
        """Convert CitationNode to dict"""
        return {
            "id": node.paper_id,
            "title": node.title,
            "year": node.year,
            "citations_count": node.citations_count,
            "references_count": node.references_count,
        }

    def get_subgraph(
        self, paper_ids: List[str], include_references: int = 1
    ) -> "CitationGraphEngine":
        """Get subgraph centered on specific papers"""
        subgraph = CitationGraphEngine()

        for pid in paper_ids:
            if pid in self.nodes:
                subgraph.nodes[pid] = self.nodes[pid]

                if include_references >= 1:
                    for ref_id in self.adjacency_list.get(pid, []):
                        if ref_id in self.nodes:
                            subgraph.nodes[ref_id] = self.nodes[ref_id]

                if include_references >= 2:
                    for cited_id in self.reverse_adjacency.get(pid, []):
                        if cited_id in self.nodes:
                            subgraph.nodes[cited_id] = self.nodes[cited_id]

        for edge in self.edges:
            if (
                edge.from_paper_id in subgraph.nodes
                and edge.to_paper_id in subgraph.nodes
            ):
                subgraph.edges.append(edge)
                if edge.from_paper_id not in subgraph.adjacency_list:
                    subgraph.adjacency_list[edge.from_paper_id] = set()
                if edge.to_paper_id not in subgraph.reverse_adjacency:
                    subgraph.reverse_adjacency[edge.to_paper_id] = set()
                subgraph.adjacency_list[edge.from_paper_id].add(edge.to_paper_id)
                subgraph.reverse_adjacency[edge.to_paper_id].add(edge.from_paper_id)

        return subgraph

    def find_citation_cycles(self, max_length: int = 6) -> List[List[str]]:
        """Find citation cycles in the graph"""
        cycles = []

        def dfs(current: str, path: List[str], visited: Set[str], start: str):
            if len(path) >= 3 and current == start:
                cycles.append(path.copy())
                return

            if len(path) >= max_length:
                return

            for neighbor in self.adjacency_list.get(current, []):
                if neighbor in visited and neighbor != start:
                    continue
                if len(path) > 1 and neighbor == path[-2]:
                    continue

                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited, start)
                path.pop()
                visited.remove(neighbor)

        for start_id in self.nodes:
            dfs(start_id, [start_id], {start_id}, start_id)

        return cycles

    def calculate_impact_factor(self, paper_id: str, year: int = None) -> float:
        """Calculate impact factor for a paper"""
        if paper_id not in self.nodes:
            return 0.0

        citing_papers = self.get_paper_cited_by(paper_id)

        if year is None:
            return len(citing_papers)

        recent_citations = [
            p for p in citing_papers if p.year == year or p.year == year - 1
        ]

        return len(recent_citations)

    def get_citation_trends(self, paper_id: str) -> Dict[int, int]:
        """Get citation count by year"""
        citing_papers = self.get_paper_cited_by(paper_id)

        trends = {}
        for paper in citing_papers:
            year = paper.year
            trends[year] = trends.get(year, 0) + 1

        return dict(sorted(trends.items()))

    def export_graph_json(self) -> dict:
        """Export graph as JSON-serializable dict"""
        return {
            "nodes": [
                {
                    "id": pid,
                    "title": node.title,
                    "year": node.year,
                    "citations": node.citations_count,
                    "references": node.references_count,
                }
                for pid, node in self.nodes.items()
            ],
            "edges": [
                {"from": e.from_paper_id, "to": e.to_paper_id, "type": e.edge_type}
                for e in self.edges
            ],
            "metrics": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "density": self.get_graph_metrics().density,
            },
        }


def get_neighbors(
    self, paper_id: str, depth: int = 1, direction: str = "both"
) -> Set[str]:
    """Get neighbors at given depth"""
    if paper_id not in self.nodes:
        return set()

    neighbors = set()
    current_level = {paper_id}

    for _ in range(depth):
        next_level = set()

        if direction in ["both", "out"]:
            for node in current_level:
                next_level.update(self.adjacency_list.get(node, []))

        if direction in ["both", "in"]:
            for node in current_level:
                next_level.update(self.reverse_adjacency.get(node, []))

        neighbors.update(next_level)
        current_level = next_level - neighbors

    neighbors.discard(paper_id)
    return neighbors


@dataclass
class RecommendationResult:
    """Result of paper recommendation"""

    paper_id: str
    title: str
    year: int
    score: float
    reason: str


@dataclass
class SimilarityResult:
    """Result of similarity calculation"""

    paper1_id: str
    paper2_id: str
    similarity_score: float
    shared_references: List[str]
    shared_citations: List[str]
    cocitation_count: int
    bibliographic_coupling: int


class CitationRecommendationEngine:
    """Engine for citation-based paper recommendations"""

    def __init__(self, graph: CitationGraphEngine):
        self.graph = graph

    def get_similar_papers(
        self, paper_id: str, top_k: int = 10, method: str = "combined"
    ) -> List[RecommendationResult]:
        """Get similar papers using various methods"""
        if paper_id not in self.graph.nodes:
            return []

        if method == "references":
            return self._by_shared_references(paper_id, top_k)
        elif method == "citations":
            return self._by_shared_citations(paper_id, top_k)
        elif method == "cocitation":
            return self._by_cocitation(paper_id, top_k)
        elif method == "bibliographic":
            return self._by_bibliographic_coupling(paper_id, top_k)
        else:
            return self._by_combined(paper_id, top_k)

    def _by_shared_references(
        self, paper_id: str, top_k: int
    ) -> List[RecommendationResult]:
        """Find papers with shared references"""
        paper_refs = self.graph.adjacency_list.get(paper_id, set())
        scores = {}

        for other_id in self.graph.nodes:
            if other_id == paper_id:
                continue
            other_refs = self.graph.adjacency_list.get(other_id, set())
            shared = len(paper_refs & other_refs)
            if shared > 0:
                scores[other_id] = shared

        return self._build_results(paper_id, scores, top_k, "shared references")

    def _by_shared_citations(
        self, paper_id: str, top_k: int
    ) -> List[RecommendationResult]:
        """Find papers with shared citations (cited by same papers)"""
        paper_cited_by = self.graph.reverse_adjacency.get(paper_id, set())
        scores = {}

        for other_id in self.graph.nodes:
            if other_id == paper_id:
                continue
            other_cited_by = self.graph.reverse_adjacency.get(other_id, set())
            shared = len(paper_cited_by & other_cited_by)
            if shared > 0:
                scores[other_id] = shared

        return self._build_results(paper_id, scores, top_k, "shared citing papers")

    def _by_cocitation(self, paper_id: str, top_k: int) -> List[RecommendationResult]:
        """Find papers that are frequently cited together"""
        paper_cited_by = self.graph.reverse_adjacency.get(paper_id, set())
        scores = {}

        for other_id in self.graph.nodes:
            if other_id == paper_id:
                continue
            other_cited_by = self.graph.reverse_adjacency.get(other_id, set())
            cocitation = len(paper_cited_by & other_cited_by)
            if cocitation > 0:
                scores[other_id] = cocitation

        return self._build_results(paper_id, scores, top_k, "co-cited frequently")

    def _by_bibliographic_coupling(
        self, paper_id: str, top_k: int
    ) -> List[RecommendationResult]:
        """Find papers that reference similar papers"""
        paper_refs = self.graph.adjacency_list.get(paper_id, set())
        scores = {}

        for other_id in self.graph.nodes:
            if other_id == paper_id:
                continue
            other_refs = self.graph.adjacency_list.get(other_id, set())
            coupling = len(paper_refs & other_refs)
            if coupling > 0:
                scores[other_id] = coupling

        return self._build_results(paper_id, scores, top_k, "similar reference lists")

    def _by_combined(self, paper_id: str, top_k: int) -> List[RecommendationResult]:
        """Combine multiple similarity methods"""
        paper_refs = self.graph.adjacency_list.get(paper_id, set())
        paper_cited_by = self.graph.reverse_adjacency.get(paper_id, set())

        scores = {}

        for other_id in self.graph.nodes:
            if other_id == paper_id:
                continue

            other_refs = self.graph.adjacency_list.get(other_id, set())
            other_cited_by = self.graph.reverse_adjacency.get(other_id, set())

            shared_refs = len(paper_refs & other_refs)
            shared_cits = len(paper_cited_by & other_cited_by)
            cocitation = len(paper_cited_by & other_cited_by)

            combined_score = shared_refs + shared_cits + (cocitation * 0.5)

            if combined_score > 0:
                scores[other_id] = combined_score

        return self._build_results(
            paper_id, scores, top_k, "multiple similarity signals"
        )

    def _build_results(
        self, paper_id: str, scores: Dict[str, float], top_k: int, reason: str
    ) -> List[RecommendationResult]:
        """Build recommendation results from scores"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for pid, score in sorted_scores:
            if pid in self.graph.nodes:
                node = self.graph.nodes[pid]
                results.append(
                    RecommendationResult(
                        paper_id=pid,
                        title=node.title,
                        year=node.year,
                        score=round(score, 3),
                        reason=reason,
                    )
                )

        return results

    def recommend_citing_papers(
        self, paper_id: str, top_k: int = 5
    ) -> List[RecommendationResult]:
        """Recommend papers that should cite this paper"""
        if paper_id not in self.graph.nodes:
            return []

        paper_refs = self.graph.adjacency_list.get(paper_id, set())
        scores = {}

        for other_id in self.graph.nodes:
            if other_id == paper_id:
                continue

            other_refs = self.graph.adjacency_list.get(other_id, set())

            if paper_id not in other_refs:
                overlap = len(paper_refs & other_refs)
                if overlap > 0:
                    scores[other_id] = overlap

        results = []
        for pid, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[
            :top_k
        ]:
            if pid in self.graph.nodes:
                node = self.graph.nodes[pid]
                results.append(
                    RecommendationResult(
                        paper_id=pid,
                        title=node.title,
                        year=node.year,
                        score=round(score, 3),
                        reason="references similar papers",
                    )
                )

        return results


class CitationAnalysisEngine:
    """Advanced citation analysis and metrics"""

    def __init__(self, graph: CitationGraphEngine):
        self.graph = graph

    def calculate_h_index(self, paper_id: str) -> int:
        """Calculate h-index for a paper's citation history"""
        citing_papers = self.graph.get_paper_cited_by(paper_id)
        citations = sorted([p.citations_count for p in citing_papers], reverse=True)

        h_index = 0
        for i, cit in enumerate(citations, 1):
            if cit >= i:
                h_index = i
            else:
                break

        return h_index

    def calculate_i10_index(self, paper_id: str) -> int:
        """Calculate i10-index (papers with 10+ citations)"""
        citing_papers = self.graph.get_paper_cited_by(paper_id)
        return sum(1 for p in citing_papers if p.citations_count >= 10)

    def calculate_citation_age(self, paper_id: str) -> float:
        """Calculate average age of citations in years"""
        if paper_id not in self.graph.nodes:
            return 0.0

        paper = self.graph.nodes[paper_id]
        citing_papers = self.graph.get_paper_cited_by(paper_id)

        if not citing_papers:
            return 0.0

        total_age = sum(paper.year - p.year for p in citing_papers)
        return round(total_age / len(citing_papers), 2)

    def calculate_field_normalized_citations(
        self, paper_id: str, field_avg_citations: float
    ) -> float:
        """Calculate field-normalized citation ratio"""
        if paper_id not in self.graph.nodes:
            return 0.0

        paper_citations = self.graph.nodes[paper_id].citations_count

        if field_avg_citations == 0:
            return 0.0

        return round(paper_citations / field_avg_citations, 3)

    def get_citation_velocity(self, paper_id: str, years: int = 3) -> Dict[int, int]:
        """Get citation velocity over time"""
        citing_papers = self.graph.get_paper_cited_by(paper_id)

        if paper_id not in self.graph.nodes:
            return {}

        current_year = self.graph.nodes[paper_id].year

        velocity = {}
        for year in range(current_year, current_year + years + 1):
            count = sum(1 for p in citing_papers if p.year == year)
            velocity[year] = count

        return velocity

    def calculate_aper_index(self, paper_id: str) -> float:
        """Calculate Author-level h-index equivalent (aper)"""
        citing_papers = self.graph.get_paper_cited_by(paper_id)
        citations = [p.citations_count for p in citing_papers]

        if not citations:
            return 0.0

        citations.sort(reverse=True)

        n = len(citations)
        aper = 0

        for i in range(1, n + 1):
            if citations[i - 1] >= i:
                aper = i
            else:
                break

        return aper

    def get_citation_distribution(self, paper_id: str) -> Dict[str, int]:
        """Get distribution of citations by year range"""
        citing_papers = self.graph.get_paper_cited_by(paper_id)

        distribution = {
            "0-1 years": 0,
            "1-3 years": 0,
            "3-5 years": 0,
            "5-10 years": 0,
            "10+ years": 0,
        }

        if paper_id not in self.graph.nodes:
            return distribution

        paper_year = self.graph.nodes[paper_id].year

        for p in citing_papers:
            age = paper_year - p.year

            if age <= 1:
                distribution["0-1 years"] += 1
            elif age <= 3:
                distribution["1-3 years"] += 1
            elif age <= 5:
                distribution["3-5 years"] += 1
            elif age <= 10:
                distribution["5-10 years"] += 1
            else:
                distribution["10+ years"] += 1

        return distribution

    def identify_citation_bridges(self, top_k: int = 10) -> List[Tuple[str, float]]:
        """Identify papers that bridge different research areas"""
        bridges = []

        for paper_id in self.graph.nodes:
            in_degree = len(self.graph.reverse_adjacency.get(paper_id, set()))
            out_degree = len(self.graph.adjacency_list.get(paper_id, set()))

            if in_degree > 0 and out_degree > 0:
                bridge_score = in_degree * out_degree
                bridges.append((paper_id, bridge_score))

        return sorted(bridges, key=lambda x: x[1], reverse=True)[:top_k]

    def get_research_frontier(self, paper_id: str, depth: int = 2) -> List[dict]:
        """Get papers that represent the research frontier"""
        if paper_id not in self.graph.nodes:
            return []

        paper = self.graph.nodes[paper_id]
        frontier = []

        cited_papers = self.graph.get_paper_cited_by(paper_id)

        for cited in cited_papers:
            new_citations = len(self.graph.get_paper_cited_by(cited.paper_id))

            if new_citations > paper.citations_count * 0.5:
                frontier.append(
                    {
                        "paper_id": cited.paper_id,
                        "title": cited.title,
                        "year": cited.year,
                        "new_citations": new_citations,
                        "growth_potential": "high",
                    }
                )

        return sorted(frontier, key=lambda x: x["new_citations"], reverse=True)


class CitationChainTracer:
    """Trace citation chains forward and backward"""

    def __init__(self, graph: CitationGraphEngine):
        self.graph = graph

    def trace_backwards(
        self, paper_id: str, max_depth: int = 5
    ) -> Dict[int, List[dict]]:
        """Trace citation chain backwards (references)"""
        if paper_id not in self.graph.nodes:
            return {}

        chain = {}

        def recursive_trace(pid: str, depth: int):
            if depth > max_depth or pid not in self.graph.nodes:
                return

            if depth not in chain:
                chain[depth] = []

            refs = self.graph.get_paper_citations(pid)

            for ref in refs:
                chain[depth].append(
                    {"id": ref.paper_id, "title": ref.title, "year": ref.year}
                )
                recursive_trace(ref.paper_id, depth + 1)

        recursive_trace(paper_id, 1)
        return chain

    def trace_forwards(
        self, paper_id: str, max_depth: int = 5
    ) -> Dict[int, List[dict]]:
        """Trace citation chain forwards (cited by)"""
        if paper_id not in self.graph.nodes:
            return {}

        chain = {}

        def recursive_trace(pid: str, depth: int):
            if depth > max_depth or pid not in self.graph.nodes:
                return

            if depth not in chain:
                chain[depth] = []

            cited = self.graph.get_paper_cited_by(pid)

            for cit in cited:
                chain[depth].append(
                    {"id": cit.paper_id, "title": cit.title, "year": cit.year}
                )
                recursive_trace(cit.paper_id, depth + 1)

        recursive_trace(paper_id, 1)
        return chain

    def find_citation_gaps(self, paper_id: str) -> List[dict]:
        """Find gaps in citation chain (missing connections)"""
        if paper_id not in self.graph.nodes:
            return []

        paper = self.graph.nodes[paper_id]
        cited_by = self.graph.get_paper_cited_by(paper_id)

        cited_by_years = {c.year for c in cited_by}

        gaps = []

        future_years = range(paper.year + 1, paper.year + 4)
        for year in future_years:
            if year not in cited_by_years:
                gaps.append(
                    {
                        "type": "future_citation",
                        "year": year,
                        "description": f"Potentially missing citations from {year}",
                    }
                )

        return gaps


class NetworkVisualizationGenerator:
    """Generate visualization data for citation networks"""

    def __init__(self, graph: CitationGraphEngine):
        self.graph = graph

    def generate_d3_json(
        self, paper_ids: List[str] = None, include_neighbors: int = 1
    ) -> dict:
        """Generate D3.js compatible JSON"""
        if paper_ids:
            subgraph = self.graph.get_subgraph(paper_ids, include_neighbors)
            nodes = subgraph.nodes
            edges = subgraph.edges
        else:
            nodes = self.graph.nodes
            edges = self.graph.edges

        d3_nodes = []
        for pid, node in nodes.items():
            d3_nodes.append(
                {
                    "id": pid,
                    "label": node.title[:50] + "..."
                    if len(node.title) > 50
                    else node.title,
                    "year": node.year,
                    "citations": node.citations_count,
                    "radius": min(max(node.citations_count / 10, 5), 30),
                }
            )

        d3_links = []
        for edge in edges:
            d3_links.append(
                {
                    "source": edge.from_paper_id,
                    "target": edge.to_paper_id,
                    "type": edge.edge_type,
                }
            )

        return {
            "nodes": d3_nodes,
            "links": d3_links,
            "metadata": {"total_nodes": len(d3_nodes), "total_links": len(d3_links)},
        }

    def generate_cytoscape_json(self, paper_ids: List[str] = None) -> dict:
        """Generate Cytoscape.js compatible JSON"""
        if paper_ids:
            subgraph = self.graph.get_subgraph(paper_ids, 1)
            nodes = subgraph.nodes
            edges = subgraph.edges
        else:
            nodes = self.graph.nodes
            edges = self.graph.edges

        elements = []

        for pid, node in nodes.items():
            elements.append(
                {
                    "data": {
                        "id": pid,
                        "label": node.title[:30],
                        "year": node.year,
                        "citations": node.citations_count,
                    }
                }
            )

        for edge in edges:
            elements.append(
                {
                    "data": {
                        "id": f"{edge.from_paper_id}-{edge.to_paper_id}",
                        "source": edge.from_paper_id,
                        "target": edge.to_paper_id,
                    }
                }
            )

        return {"elements": elements}

    def generate_graphml(self) -> str:
        """Generate GraphML format string"""
        graphml = """<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="title" for="node" attr.name="title"/>
  <key id="year" for="node" attr.name="year"/>
  <key id="citations" for="node" attr.name="citations"/>
  <key id="weight" for="edge" attr.name="weight"/>
  <graph id="CitationGraph" edgedefault="directed">
"""

        for pid, node in self.graph.nodes.items():
            graphml += f"""    <node id="{pid}">
      <data key="title">{node.title}</data>
      <data key="year">{node.year}</data>
      <data key="citations">{node.citations_count}</data>
    </node>
"""

        for edge in self.graph.edges:
            graphml += f"""    <edge source="{edge.from_paper_id}" target="{edge.to_paper_id}">
      <data key="weight">{edge.weight}</data>
    </edge>
"""

        graphml += "  </graph>\n</graphml>"

        return graphml
