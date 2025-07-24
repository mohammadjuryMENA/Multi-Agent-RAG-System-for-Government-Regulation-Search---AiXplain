"""
Facade for the Multi-Agent RAG System for Government Regulation Search.
Provides a unified interface to all agent handlers and upload logic.
"""
from handlers.commercial_code import CommercialCodeHandler
from handlers.epa import EPAHandler
from handlers.federal_register import FederalRegisterHandler
from handlers.courtlistener import CAPHandler
from handlers.upload import UploadHandler

class PolicyNavigatorFacade:
    """
    Facade class that provides a unified interface to all agent/tool handlers.
    Handles query routing and document ingestion.
    """
    def __init__(self, slack_token=None, slack_channel=None):
        # Register handlers for each supported query type
        self.handlers = {
            'commercial code': CommercialCodeHandler(),
            'epa': EPAHandler(),
            'federal register': FederalRegisterHandler(),
            'case law': CAPHandler(),
        }
        self.upload_handler = UploadHandler()

    def handle_query(self, query: str) -> str:
        """
        Route the query to the correct handler based on prefix.
        Args:
            query (str): The user's query, prefixed with the handler type.
        Returns:
            str: The handler's response or an error message.
        """
        prefix = query.split(':', 1)[0].strip().lower()
        handler = self.handlers.get(prefix)
        if handler:
            return handler.run(query)
        else:
            return "[Error] Unknown query type."

    def handle_upload(self, path_or_url: str) -> str:
        """
        Ingest a document or URL using the upload handler.
        Args:
            path_or_url (str): File path or URL to ingest.
        Returns:
            str: Status message from the upload handler.
        """
        return self.upload_handler.ingest(path_or_url) 