import os
import requests
from bs4 import BeautifulSoup
from handlers.base import QueryHandler
from vectorstore.vector_index import VectorIndex
from tools.aixplain_tools import aixplain_embed

# Global index for uploaded documents
UPLOAD_INDEX = VectorIndex()

class UploadHandler(QueryHandler):
    def ingest(self, path_or_url: str) -> str:
        # Determine if input is a file or URL
        if path_or_url.startswith('http://') or path_or_url.startswith('https://'):
            try:
                resp = requests.get(path_or_url, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Extract visible text from paragraphs and headings
                texts = []
                for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
                    txt = tag.get_text(strip=True)
                    if txt:
                        texts.append(txt)
                content = '\n'.join(texts)
                if not content:
                    content = soup.get_text(separator='\n', strip=True)
                # Save to a temp file for downstream processing
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmp_file:
                    tmp_file.write(content)
                    tmp_path = tmp_file.name
                return f"URL content extracted and saved to {tmp_path}"
            except Exception as e:
                return f"[Error] Failed to extract URL content: {e}"
        else:
            if not os.path.exists(path_or_url):
                return f"Error: File not found: {path_or_url}"
            try:
                text = self._extract_from_file(path_or_url)
            except Exception as e:
                return f"Error: {e}"
            doc_name = os.path.basename(path_or_url)
        # Improved chunking: split by paragraph (double newline), fallback to 500 chars
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if len(paragraphs) > 1:
            chunks = paragraphs
        else:
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
        for i, chunk in enumerate(chunks):
            # Add document name and chunk number for source reference
            chunk_with_source = f"[{doc_name} - chunk {i+1}]:\n{chunk}"
            embedding = aixplain_embed(chunk_with_source)
            UPLOAD_INDEX.add_document(chunk_with_source, embedding)
        return f"Successfully ingested and indexed document: {doc_name} (chunks: {len(chunks)})"

    def _extract_from_file(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self._extract_pdf(file_path)
        elif ext == '.docx':
            return self._extract_docx(file_path)
        elif ext == '.txt':
            return self._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _extract_pdf(self, file_path: str) -> str:
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pdfplumber is required for PDF extraction. Please install it with 'pip install pdfplumber'.")
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        if not text.strip():
            raise ValueError("No extractable text found in PDF.")
        return text

    def _extract_docx(self, file_path: str) -> str:
        # TODO: Use python-docx to extract text
        return "[DOCX extraction not implemented]"

    def _extract_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_from_url(self, url: str) -> str:
        # TODO: Use newspaper3k or requests+BeautifulSoup for extraction
        return "[URL extraction not implemented]"

    def run(self, query: str) -> str:
        # Not used for upload handler
        return "[UploadHandler does not support run()]" 