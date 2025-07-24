from handlers.base import QueryHandler
from aixplain.factories import AgentFactory, IndexFactory

# Handler for EPA queries
class EPAHandler(QueryHandler):
    def __init__(self):
        index = self._get_index()
        # Create the agent for EPA queries
        self.agent = AgentFactory.create(
            name="EPA Agent",
            description="Answers queries about EPA regulations.",
            instructions="You answer questions about EPA regulations.",
            tools=[index] if index else []
        )

    def _get_index(self):
        # Find the EPA index
        for idx in IndexFactory.list():
            if getattr(idx, 'name', None) == "EPA Index":
                return idx
        return None

    def run(self, query: str) -> str:
        # Run the query using the agent
        response = self.agent.run(query)
        return response['data']['output'] 