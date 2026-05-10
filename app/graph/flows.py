"""LangGraph workflow definitions"""

from langgraph.graph import StateGraph, START, END
from app.graph.state import ResearchState, DebateState


def create_research_flow():
    """Create the research workflow graph"""
    graph = StateGraph(ResearchState)

    def classify(state: ResearchState) -> dict:
        """Route based on query complexity"""
        query = state["query"]
        if "debate" in query.lower() or "compare" in query.lower():
            return {"routing": "detailed"}
        return {"routing": "simple"}

    def search_papers(state: ResearchState) -> dict:
        """Search for papers (mock)"""
        return {
            "papers": [{"title": f"Paper about {state['query']}", "source": "mock"}]
        }

    def research(state: ResearchState) -> dict:
        """Run research agent (mock)"""
        return {"research_notes": f"Research findings for: {state['query']}"}

    def critique(state: ResearchState) -> dict:
        """Run critique agent (mock)"""
        return {"critique_notes": "Critique: Claims verified, good quality"}

    def synthesize(state: ResearchState) -> dict:
        """Synthesize final report"""
        return {
            "final_report": f"Report on {state['query']}:\n\n{state['research_notes']}"
        }

    graph.add_node("classify", classify)
    graph.add_node("search", search_papers)
    graph.add_node("research", research)
    graph.add_node("critique", critique)
    graph.add_node("synthesize", synthesize)

    graph.add_edge(START, "classify")
    graph.add_edge("classify", "search")
    graph.add_edge("search", "research")

    graph.add_conditional_edges(
        "research",
        lambda s: "critique" if s.get("routing") == "detailed" else "synthesize",
    )
    graph.add_edge("critique", "synthesize")
    graph.add_edge("synthesize", END)

    return graph.compile()


def create_debate_flow():
    """Create the debate workflow graph"""
    graph = StateGraph(DebateState)

    def proponent_argue(state: DebateState) -> dict:
        return {"proponent_arguments": f"Arguments FOR: {state['thesis']}"}

    def critic_argue(state: DebateState) -> dict:
        return {"critic_arguments": f"Arguments AGAINST: {state['thesis']}"}

    def methodologist_eval(state: DebateState) -> dict:
        return {"methodology_evaluation": "Methodology is sound"}

    def synthesize_verdict(state: DebateState) -> dict:
        return {
            "final_verdict": f"Verdict on: {state['thesis']}",
            "vote_pro": 2,
            "vote_con": 1,
            "confidence": 0.75,
        }

    graph.add_node("proponent", proponent_argue)
    graph.add_node("critic", critic_argue)
    graph.add_node("methodologist", methodologist_eval)
    graph.add_node("verdict", synthesize_verdict)

    graph.add_edge(START, "proponent")
    graph.add_edge(START, "critic")
    graph.add_edge("proponent", "methodologist")
    graph.add_edge("critic", "methodologist")
    graph.add_edge("methodologist", "verdict")
    graph.add_edge("verdict", END)

    return graph.compile()


research_graph = create_research_flow()
debate_graph = create_debate_flow()
