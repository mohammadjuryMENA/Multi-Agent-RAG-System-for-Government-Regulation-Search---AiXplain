from handlers.base import QueryHandler
from handlers.upload import UPLOAD_INDEX
from tools.aixplain_tools import aixplain_embed, aixplain_summarize

class UploadedDocHandler(QueryHandler):
    def run(self, query: str) -> str:
        # Remove the 'upload:' or 'uploaded:' prefix if present
        q = query
        if q.lower().startswith('upload:'):
            q = q[len('upload:'):].strip()
        elif q.lower().startswith('uploaded:'):
            q = q[len('uploaded:'):].strip()
        embedding = aixplain_embed(q)
        retrieved = UPLOAD_INDEX.query(q, embedding, top_k=2)
        if not retrieved:
            return "No relevant information found in uploaded documents."
        # Summarize the most relevant chunk(s) and include source reference
        answers = []
        for chunk in retrieved:
            summary = aixplain_summarize(chunk) or chunk[:300]
            answers.append(summary)
        return '\n\n'.join(answers) 