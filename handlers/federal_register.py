from handlers.base import QueryHandler
from agents.rag_agent import RAGAgent

# Adapter for the Federal Register API
class FederalRegisterHandler(QueryHandler):
    def __init__(self):
        self.agent = RAGAgent()

    def run(self, query: str) -> str:
        return self.agent.handle_query(query) 