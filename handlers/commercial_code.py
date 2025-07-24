from handlers.base import QueryHandler
from aixplain.factories import AgentFactory, IndexFactory

# Handler for Commercial Code queries (Strategy pattern)
class CommercialCodeHandler(QueryHandler):
    """
    Handles queries related to the Commercial Code dataset using an agent.
    Implements the Strategy pattern for query handling.
    """
    def __init__(self):
        """
        Initializes the CommercialCodeHandler by creating an agent with the appropriate index.
        """
        index = self._get_index()
        self.agent = AgentFactory.create(
            name="Commercial Code Agent",
            description="Answers queries about the Commercial Code dataset.",
            instructions="You answer questions about the Commercial Code.",
            tools=[index] if index else []
        )

    def _get_index(self):
        """
        Finds and returns the Commercial Code index from the available indexes.
        Returns:
            The index object if found, else None.
        """
        for idx in IndexFactory.list():
            if getattr(idx, 'name', None) == "Commercial Code Index":
                return idx
        return None

    def run(self, query: str) -> str:
        """
        Runs the query using the agent.
        Args:
            query (str): The user's query.
        Returns:
            str: The agent's response.
        """
        response = self.agent.run(query)
        return response['data']['output'] 