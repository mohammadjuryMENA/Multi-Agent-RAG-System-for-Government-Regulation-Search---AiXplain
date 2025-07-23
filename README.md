# Multi-Agent RAG System for Government Regulation Search (aiXplain)

A modular, agentic Retrieval-Augmented Generation (RAG) system for querying, analyzing, and extracting insights from complex government regulations, compliance policies, and public health guidelines.

---

## What This Agent Does
This project implements a multi-agent RAG pipeline that allows users to:
- Query and retrieve relevant sections from large regulatory documents
- Summarize, analyze, and cross-reference legal and policy texts
- Integrate with external APIs and datasets for up-to-date information
- Support extensible agent and tool integration for advanced workflows

Agents include retrievers, policy checkers, case law summarizers, and can be extended for analytics, summarization, or translation tasks.

---

## Project Overview
- **Multi-agent RAG pipeline:** Modular agents for retrieval, policy checking, summarization, and more
- **Vector-based document retrieval:** Fast, semantic search over ingested documents
- **Flexible ingestion:** Supports datasets, public websites, and document uploads
- **Tool integration:** Easily connect APIs, custom Python tools, and data sources
- **CLI and Streamlit UI:** Interact via command line or web interface

---

## Dataset & Source Links
- **California Commercial Code - COM:** [leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM&tocTitle=+Commercial+Code+-+COM](https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM&tocTitle=+Commercial+Code+-+COM)
- **EPA, Federal Register, CourtListener:** Integrated via API handlers (see `handlers/`)
- **aiXplain API:** [aiXplain Documentation](https://docs.aixplain.com/)
- **Custom uploads:** Place PDFs or docs in the `documents/` folder

---

## Setup Instructions
1. **Clone the repository:**
   ```sh
   git clone https://github.com/mohammadjuryMENA/Multi-Agent-RAG-System-for-Government-Regulation-Search---AiXplain.git
   cd Multi-Agent-RAG-System-for-Government-Regulation-Search---AiXplain
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure API keys:**
   - Add your API keys to `config.py` or set as environment variables as needed (see comments in `config.py`).
4. **Ingest data:**
   - Use scripts in `scripts/` to ingest datasets or documents, e.g.:
     ```sh
     python scripts/ingest_commercial_code.py
     python scripts/ingest_all.py
     ```
5. **Run the main app:**
   - CLI: `python main.py`
   - Streamlit UI: `streamlit run ui_streamlit.py`

---

## Tool Integration Steps
- **aiXplain API:**
  - Configure credentials in `config.py`.
  - Used for advanced NLP tasks (summarization, translation, etc.).
- **Custom Python Tools:**
  - Located in `tools/` (e.g., `aixplain_tools.py`, `caselaw_api.py`).
  - Extend or add new tools as needed for your workflow.
- **CSV/SQL Integration:**
  - Use scripts in `scripts/` to ingest and index tabular data.
- **API Handlers:**
  - See `handlers/` for integration with EPA, Federal Register, CourtListener, and more.

---

## Example Inputs & Outputs
**Input (CLI or UI):**
```
What are the compliance requirements for vehicle registration in California?
```
**Output:**
```
Relevant sections from the California Commercial Code:
- Section 5600: [summary...]
- Section 5601: [summary...]

Additional requirements from EPA:
- [EPA policy summary...]
```

**Input:**
```
Summarize case law related to Section 1101 of the Commercial Code.
```
**Output:**
```
Case Law Summary:
- [Case 1]: [summary...]
- [Case 2]: [summary...]
```

---

## Future Improvements
- **Add more agents:**
  - Summarization, analytics, translation, or Q&A agents
- **UI improvements:**
  - Enhanced Streamlit or web UI, better visualization, user authentication
- **Additional data integrations:**
  - More government datasets, international regulations, real-time data feeds
- **Caching & memory features:**
  - Persistent memory for agents, faster repeated queries, session history
- **Multilingual support:**
  - Support for non-English regulations and queries
- **Advanced analytics:**
  - Trend analysis, compliance risk scoring, policy change detection

---

## References
- [aiXplain Documentation](https://docs.aixplain.com/)
- [California Commercial Code](https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM&tocTitle=+Commercial+Code+-+COM)
- [EPA](https://www.epa.gov/)
- [CourtListener](https://www.courtlistener.com/)
- [Federal Register](https://www.federalregister.gov/)
