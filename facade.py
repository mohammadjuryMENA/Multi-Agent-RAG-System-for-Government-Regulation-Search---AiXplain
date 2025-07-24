from handlers.commercial_code import CommercialCodeHandler
from handlers.epa import EPAHandler
from handlers.federal_register import FederalRegisterHandler
from handlers.courtlistener import CourtListenerHandler
from handlers.upload import UploadHandler

class PolicyNavigatorFacade:
    def __init__(self, slack_token=None, slack_channel=None):
        self.handlers = {
            'commercial code': CommercialCodeHandler(),
            'epa': EPAHandler(),
            'federal register': FederalRegisterHandler(),
            'court': CourtListenerHandler(),
        }
        self.upload_handler = UploadHandler()

    def handle_query(self, query: str) -> str:
        # Route the query to the correct handler based on prefix
        prefix = query.split(':', 1)[0].strip().lower()
        handler = self.handlers.get(prefix)
        if handler:
            return handler.run(query)
        else:
            return "[Error] Unknown query type."

    def handle_upload(self, path_or_url: str) -> str:
        return self.upload_handler.ingest(path_or_url) 