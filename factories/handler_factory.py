from handlers.commercial_code import CommercialCodeHandler
from handlers.epa import EPAHandler
from handlers.federal_register import FederalRegisterHandler
from handlers.courtlistener import CourtListenerHandler
from handlers.uploaded_doc import UploadedDocHandler

class HandlerFactory:
    @staticmethod
    def get_handler(query: str):
        # Keyword-based routing to select the appropriate handler
        q = query.lower()
        if q.startswith('upload:') or q.startswith('uploaded:'):
            return UploadedDocHandler()
        if any(x in q for x in ["epa", "environment", "clean air act"]):
            return EPAHandler()
        elif any(x in q for x in ["federal register", "executive order", "regulation", "notices", "department of transportation", "public comments"]):
            return FederalRegisterHandler()
        elif any(x in q for x in ["court", "case", "sued", "precedent", "litigation", "supreme court", "outcome", "v.", "amendment", "section 230", "patriot act", "fair use", "roommates.com", "fourth amendment"]):
            return CourtListenerHandler()
        else:
            return CommercialCodeHandler() 