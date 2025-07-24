# Policy Navigator Agent (AiXplain)

An Agentic Retrieval-Augmented Generation (RAG) system for querying and extracting insights from complex government regulations, compliance policies, and public health guidelines.

---

## 🧠 What Does This Agent Do?

This project implements a multi-agent RAG system that:
- Answers user queries about government regulations, legal codes, and public health policies.
- Retrieves, summarizes, and analyzes information from multiple sources (datasets, APIs, uploaded documents).
- Integrates with external APIs (e.g., Federal Register, CourtListener) and custom tools for advanced search and summarization.
- Supports extensible agent and tool architecture for future enhancements.

---

## 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your API keys and tokens, or set them directly in your environment:
     - `SLACK_TOKEN` (optional, for Slack notifications)
     - `SLACK_CHANNEL` (optional)
     - `COURTLISTENER_API_TOKEN` (for CourtListener API)
     - Any other required keys (see `config.py`)
4. **Run the main app:**
   ```bash
   python main.py
   ```

---

## 📚 Data Sources

- **Commercial Code:** [Link](https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM&tocTitle=+Commercial+Code+-+COM)
- **EPA Regulations:** [EPA Official Site](https://www.epa.gov/laws-regulations)
- **Federal Register:** [API Docs](https://www.federalregister.gov/developers/documentation/api/v1)
- **CourtListener:** [API Docs](https://www.courtlistener.com/api/rest-info/)
- **Upload Your Own Documents:** Supports PDF, TXT, and (future) DOCX files.

---

## 🛠️ Tool Integration Steps

- **aiXplain API:** Used for embedding and summarization. Configure your aiXplain credentials in your environment or `config.py`.
- **Custom Python Tools:**
  - Document parser and vector indexer for fast semantic search.
  - Handlers for ingesting and querying uploaded documents.
- **External APIs:**
  - Federal Register and CourtListener APIs are integrated via Adapter-pattern handlers. Set API tokens in your environment.
- **Adding New Tools/Agents:**
  - Implement a new handler class (see `handlers/`), register it in the main app or facade, and add to the CLI or UI.

---

## 🔔 Slack Integration

This agent can post every query and its response to a Slack channel for monitoring or collaboration.

### How to Enable

1. **Create a Slack App** and get a Bot Token (`SLACK_TOKEN`).
2. **Invite the bot** to your desired channel and get the channel ID (`SLACK_CHANNEL`).
3. **Set these environment variables** in your `.env` file:
   ```
   SLACK_TOKEN=xoxb-...
   SLACK_CHANNEL=C12345678
   ```
4. When you run the agent, every query and its response will be posted to the specified Slack channel (if configured).

### Example Slack Message

```
Query: What are the penalties for issuing a bad check?
Response: Section 3310: ... (summary of penalties)
```

---

## 💡 Example Inputs & Outputs

### Example 1: Querying Commercial Code
**Input:**
```
1  # (Select Commercial Code)
What are the penalties for issuing a bad check?
```
**Output:**
```
Commercial Code Agent response:
Section 3310: ... (summary of penalties)
```

### Example 2: EPA Regulation
**Input:**
```
2  # (Select EPA)
What are the latest EPA regulations on air quality?
```
**Output:**
```
EPA Agent response:
(Pulled summary from EPA dataset)
```

### Example 3: Federal Register
**Input:**
```
3  # (Select Federal Register)
Clean Air Act amendments 2023
```
**Output:**
```
Federal Register Tool response:
Title: ... (summary and publication date)
```

### Example 4: CourtListener
**Input:**
```
4  # (Select CourtListener)
Case law on Section 230
```
**Output:**
```
CourtListener Tool response:
CaseName (Citation): Summary...
```

---

## 🔮 Future Improvements

- **Add More Agents:**
  - Summarization, translation, analytics, or compliance-checking agents.
- **UI/UX Enhancements:**
  - Develop a web-based interface (e.g., Streamlit or React frontend).
  - Add visualization for search results and document relationships.
- **Additional Data Integrations:**
  - Integrate more legal, regulatory, or scientific datasets.
  - Support for real-time data feeds.
- **Caching & Memory Features:**
  - Implement caching for frequent queries.
  - Add persistent memory for user sessions and context-aware responses.
- **Multilingual Support:**
  - Enable querying and summarization in multiple languages.
- **Advanced Analytics:**
  - Add analytics dashboards for trends, compliance gaps, or risk assessment.

---

## 📖 References
- [aiXplain Documentation](https://docs.aixplain.com/)
- [Commercial Code](https://leginfo.legislature.ca.gov/faces/codesTOCSelected.xhtml?tocCode=COM&tocTitle=+Commercial+Code+-+COM)
- [EPA Laws & Regulations](https://www.epa.gov/laws-regulations)
- [Federal Register API](https://www.federalregister.gov/developers/documentation/api/v1)
- [CourtListener API](https://www.courtlistener.com/api/rest-info/)
