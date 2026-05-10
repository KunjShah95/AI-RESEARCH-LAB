"""AI Q&A Chat Engine - question answering over papers"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from app.models.paper import Paper


@dataclass
class QAPair:
    question: str
    answer: str
    sources: List[str]
    confidence: float


@dataclass
class ChatSession:
    session_id: str
    paper_id: str
    messages: List[Dict]
    created_at: str


class QAChatEngine:
    """Engine for AI-powered Q&A over papers"""

    def __init__(self):
        self.sessions: Dict[str, ChatSession] = {}
        self.model = None

    def answer_question(
        self,
        question: str,
        papers: List[Paper],
        chat_history: Optional[List[Dict]] = None,
    ) -> QAPair:
        """Answer a question based on paper content"""

        relevant_sections = self._find_relevant_sections(question, papers)
        answer = self._generate_answer(question, relevant_sections, papers)
        sources = [p.title for p in papers[:3]]
        confidence = self._calculate_confidence(question, relevant_sections)

        return QAPair(
            question=question, answer=answer, sources=sources, confidence=confidence
        )

    def _find_relevant_sections(
        self, question: str, papers: List[Paper]
    ) -> Dict[str, str]:
        """Find sections in papers relevant to the question"""
        relevant = {}
        question_keywords = set(question.lower().split())

        for paper in papers:
            sections = {
                "abstract": paper.abstract or "",
                "title": paper.title or "",
                "methods": getattr(paper, "methods", "") or "",
                "results": getattr(paper, "results", "") or "",
                "conclusions": getattr(paper, "conclusions", "") or "",
            }

            for section_name, content in sections.items():
                if not content:
                    continue
                section_keywords = set(content.lower().split())
                overlap = len(question_keywords & section_keywords)
                if overlap > 2:
                    relevant[f"{paper.title[:30]} - {section_name}"] = content[:500]

        return relevant

    def _generate_answer(
        self, question: str, relevant: Dict[str, str], papers: List[Paper]
    ) -> str:
        """Generate answer from relevant sections"""
        if not relevant:
            return "I couldn't find specific information to answer your question in the provided papers."

        key_papers = list(relevant.items())[:3]

        answer_parts = []

        if "method" in question.lower():
            for title, content in key_papers:
                if "method" in title.lower():
                    answer_parts.append(
                        f"Based on the methods section: {content[:300]}"
                    )

        if "result" in question.lower() or "find" in question.lower():
            for title, content in key_papers:
                if "result" in title.lower():
                    answer_parts.append(f"Regarding results: {content[:300]}")

        if not answer_parts:
            answer_parts.append(
                "Based on the papers reviewed, here's relevant information:"
            )
            for title, content in key_papers:
                answer_parts.append(f"- {title}: {content[:200]}")

        return "\n\n".join(answer_parts[:2])

    def _calculate_confidence(self, question: str, relevant: Dict[str, str]) -> float:
        """Calculate confidence score for the answer"""
        if not relevant:
            return 0.1

        base_confidence = min(0.5 + (len(relevant) * 0.1), 0.95)

        if len(question.split()) > 5:
            base_confidence += 0.1

        return min(base_confidence, 0.95)

    def create_session(self, paper_id: str) -> ChatSession:
        """Create a new chat session for a paper"""
        import uuid

        session_id = str(uuid.uuid4())

        session = ChatSession(
            session_id=session_id, paper_id=paper_id, messages=[], created_at="now"
        )

        self.sessions[session_id] = session
        return session

    def add_message(self, session_id: str, role: str, content: str):
        """Add message to chat session"""
        if session_id in self.sessions:
            self.sessions[session_id].messages.append(
                {"role": role, "content": content}
            )

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Get chat session by ID"""
        return self.sessions.get(session_id)


qa_chat_engine = QAChatEngine()
