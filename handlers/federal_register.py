from handlers.base import QueryHandler
from tools.federal_register_api import query_federal_register_api

# Adapter for the Federal Register API
class FederalRegisterHandler(QueryHandler):
    def run(self, query: str) -> str:
        # Query the Federal Register API and return the result
        resp = query_federal_register_api(query)
        return resp 