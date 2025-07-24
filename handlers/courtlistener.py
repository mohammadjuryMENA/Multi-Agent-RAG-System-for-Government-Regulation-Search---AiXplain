from handlers.base import QueryHandler
import requests
import os

# Adapter for the CourtListener API (Adapter pattern)
class CourtListenerHandler(QueryHandler):
    """
    Handles queries to the CourtListener API.
    Implements the Adapter pattern to unify the interface for query handling.
    """
    API_URL = "https://www.courtlistener.com/api/rest/v3/opinions/"
    API_TOKEN = os.environ.get("COURTLISTENER_API_TOKEN", "")  # Use env variable for token

    def run(self, query: str) -> str:
        """
        Query the CourtListener API for up to 5 relevant opinions.
        Args:
            query (str): The user's query.
        Returns:
            str: Summaries of relevant court opinions.
        """
        params = {"search": query, "page_size": 5}
        headers = {'Authorization': f'Token {self.API_TOKEN}'}
        resp = requests.get(self.API_URL, params=params, headers=headers, timeout=30)
        data = resp.json()
        results = data.get('results', [])
        if not results:
            return "No relevant court opinions found."
        summaries = []
        for opinion in results:
            case_name = (
                opinion.get('caseName') or
                opinion.get('case_name') or
                opinion.get('name_abbreviation') or
                "Unknown Case"
            )
            cite = (
                opinion.get('cite') or
                (opinion.get('citations') and opinion.get('citations')[0].get('cite')) or
                "No citation"
            )
            summary = opinion.get('summary') or opinion.get('headnotes')
            if summary:
                summary = summary.strip().replace('\n', ' ')
            else:
                plain_text = opinion.get('plain_text', '').strip()
                if plain_text:
                    paragraphs = [p.strip() for p in plain_text.split('\n') if p.strip()]
                    summary = None
                    for p in paragraphs:
                        if len(p) > 40 and not p.lower().startswith((
                            'filed', 'court', 'state of', 'appeal', 'supreme', 'district', 'county', 'judge',
                            'panel', 'date', 'before', 'argued', 'decided', 'counsel', 'attorney', 'prosecutor',
                            'defendant', 'plaintiff', 'appellant', 'appellee', 'respondent', 'petitioner', 'brief',
                            'syllabus', 'headnote')):
                            summary = p
                            break
                    if not summary:
                        summary = paragraphs[0] if paragraphs else '[No summary available]'
                else:
                    summary = '[No summary available]'
            summaries.append(f"{case_name} ({cite}): {summary}")
        # Return summaries for all found opinions
        return "\n\n".join(summaries) 