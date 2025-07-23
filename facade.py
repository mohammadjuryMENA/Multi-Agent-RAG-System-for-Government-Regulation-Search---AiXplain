from factories.handler_factory import HandlerFactory
from handlers.upload import UploadHandler

class PolicyNavigatorFacade:
    # Facade class to provide a unified interface for handling queries
    def handle_query(self, query: str) -> str:
        # Use the HandlerFactory to select the correct handler for the query
        handler = HandlerFactory.get_handler(query)
        return handler.run(query)

    def handle_upload(self, path_or_url: str) -> str:
        # Use the UploadHandler to process document or URL ingestion
        handler = UploadHandler()
        return handler.ingest(path_or_url) 