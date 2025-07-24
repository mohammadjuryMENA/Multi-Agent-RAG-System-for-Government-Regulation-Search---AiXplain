from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from facade import PolicyNavigatorFacade
from handlers.uploaded_doc import UploadedDocHandler

# --- Slack Integration ---
try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
    class SlackNotifier:
        def __init__(self, token: str, channel: str):
            self.client = WebClient(token=token)
            self.channel = channel
        def send_message(self, text: str):
            try:
                self.client.chat_postMessage(channel=self.channel, text=text)
            except SlackApiError as e:
                print(f"Slack API error: {e.response['error']}")
except ImportError:
    SlackNotifier = None

st.set_page_config(page_title="Policy Navigator Agent", layout="centered")
st.title("Policy Navigator Agent")

slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")
facade = PolicyNavigatorFacade(slack_token=slack_token, slack_channel=slack_channel)

# Initialize SlackNotifier if configured
slack_notifier = None
if SlackNotifier and slack_token and slack_channel:
    slack_notifier = SlackNotifier(slack_token, slack_channel)

# Sidebar for query type selection
query_type = st.sidebar.selectbox(
    "Select query type:",
    [
        "Commercial Code",
        "EPA",
        "Federal Register",
        "CourtListener",
        "Uploaded Documents"
    ]
)

st.sidebar.markdown("---")
# Upload document section
st.sidebar.header("Upload Document or Specify URL")
# Allow multiple file uploads
uploaded_files = st.sidebar.file_uploader("Choose files (PDF, TXT)", type=["pdf", "txt"], accept_multiple_files=True)
url_input = st.sidebar.text_input("Or enter a public URL")
if st.sidebar.button("Ingest Document/URL"):
    results = []
    # Ingest all uploaded files
    if uploaded_files:
        import tempfile
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            result = facade.handle_upload(tmp_path)
            results.append(f"{uploaded_file.name}: {result}")
    # Ingest from URL if provided
    if url_input:
        result = facade.handle_upload(url_input)
        results.append(f"URL: {result}")
    if results:
        st.sidebar.success("\n".join(results))
    else:
        st.sidebar.warning("Please upload at least one file or enter a URL.")

st.markdown("---")

# Main query input
st.header(f"Ask a question about {query_type}")
user_query = st.text_area("Enter your question:")
if st.button("Submit Query"):
    result = None
    if query_type == "Commercial Code":
        result = facade.handle_query("commercial code: " + user_query)
        st.success(result)
    elif query_type == "EPA":
        result = facade.handle_query("epa: " + user_query)
        st.success(result)
    elif query_type == "Federal Register":
        result = facade.handle_query("federal register: " + user_query)
        st.success(result)
    elif query_type == "CourtListener":
        result = facade.handle_query("court: " + user_query)
        st.success(result)
    elif query_type == "Uploaded Documents":
        handler = UploadedDocHandler()
        result = handler.run(user_query)
        st.success(result)
    # Post to Slack if configured
    if slack_notifier and result is not None:
        try:
            slack_notifier.send_message(f"Query: {user_query}\nResponse: {result}")
        except Exception as e:
            st.warning(f"Warning: Failed to post to Slack: {e}") 