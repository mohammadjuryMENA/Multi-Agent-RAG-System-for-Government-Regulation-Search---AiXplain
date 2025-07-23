import streamlit as st
from facade import PolicyNavigatorFacade
from handlers.upload import UploadHandler
from handlers.uploaded_doc import UploadedDocHandler

st.set_page_config(page_title="Policy Navigator Agent", layout="centered")
st.title("Policy Navigator Agent")

facade = PolicyNavigatorFacade()

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
uploaded_file = st.sidebar.file_uploader("Choose a file (PDF, TXT)", type=["pdf", "txt"])
url_input = st.sidebar.text_input("Or enter a public URL")
if st.sidebar.button("Ingest Document/URL"):
    if uploaded_file is not None:
        # Save uploaded file to a temp location
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + uploaded_file.name.split('.')[-1]) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        result = facade.handle_upload(tmp_path)
        st.sidebar.success(result)
    elif url_input:
        result = facade.handle_upload(url_input)
        st.sidebar.success(result)
    else:
        st.sidebar.warning("Please upload a file or enter a URL.")

st.markdown("---")

# Main query input
st.header(f"Ask a question about {query_type}")
user_query = st.text_area("Enter your question:")
if st.button("Submit Query"):
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