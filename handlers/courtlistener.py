"""
Handler for the Harvard Caselaw Access Project (CAP) API.
Provides case law search and summarization for the Multi-Agent RAG System.
"""
import requests
import os
from handlers.base import QueryHandler

class CAPHandler(QueryHandler):
    """
    Handles queries to the Harvard Caselaw Access Project (CAP) API.
    Implements the Adapter pattern to unify the interface for query handling.
    Supports optional API key authentication via the CAP_API_KEY environment variable.
    """
    API_URL = "https://api.case.law/v1/cases/"

    def run(self, query: str) -> str:
        """
        Query the CAP API for relevant case law.
        Args:
            query (str): The user's query.
        Returns:
            str: Summaries of relevant court opinions or error message.
        """
        params = {"search": query, "page_size": 3}
        headers = {"User-Agent": "Mozilla/5.0"}
        api_key = os.environ.get("CAP_API_KEY")
        # Warn if API key is missing (required for CAP API)
        if not api_key:
            return (
                "CAP API key is missing. Please register for an API key at https://case.law/api-key/ "
                "and set it as the CAP_API_KEY environment variable."
            )
        headers["Authorization"] = f"Token {api_key}"
        try:
            resp = requests.get(self.API_URL, params=params, headers=headers, timeout=30)
            if resp.status_code != 200:
                return f"CAP API error: {resp.status_code} - {resp.text[:500]}"
            if 'application/json' not in resp.headers.get('Content-Type', ''):
                return f"CAP API did not return JSON. Response: {resp.text[:500]}"
            data = resp.json()
        except Exception as e:
            return f"CAP API request failed: {e}"
        results = data.get('results', [])
        if not results:
            return "No relevant case law found."
        summaries = []
        for case in results:
            name = case.get('name_abbreviation', case.get('name', 'Unknown Case'))
            cite = case.get('citations', [{}])[0].get('cite', 'No citation')
            court = case.get('court', {}).get('name_abbreviation', 'Unknown Court')
            decision_date = case.get('decision_date', '?')
            summary = None
            # Try to get a summary from the first opinion text
            if case.get('casebody', {}).get('data', {}).get('opinions'):
                opinions = case['casebody']['data']['opinions']
                for op in opinions:
                    if op.get('text'):
                        summary = op['text'].split('\n')[0][:400]
                        break
            if not summary:
                summary = '[No summary available]'
            summaries.append(f"{name} ({cite}, {court}, {decision_date}): {summary}")
        return "\n\n".join(summaries) 