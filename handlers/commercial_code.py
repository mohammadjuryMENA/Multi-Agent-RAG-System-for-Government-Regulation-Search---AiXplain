from handlers.base import QueryHandler
from aixplain.factories import AgentFactory, IndexFactory

# Handler for Commercial Code queries
class CommercialCodeHandler(QueryHandler):
    def __init__(self):
        index = self._get_index()
        # Create the agent for Commercial Code queries
        self.agent = AgentFactory.create(
            name="Commercial Code Agent",
            description="Answers queries about the Commercial Code dataset.",
            instructions="You answer questions about the Commercial Code.",
            tools=[index] if index else []
        )

    def _get_index(self):
        # Find the Commercial Code index
        for idx in IndexFactory.list():
            if getattr(idx, 'name', None) == "Commercial Code Index":
                return idx
        return None

    def run(self, query: str) -> str:
        # Run the query using the agent
        response = self.agent.run(query)
        return response['data']['output'] 