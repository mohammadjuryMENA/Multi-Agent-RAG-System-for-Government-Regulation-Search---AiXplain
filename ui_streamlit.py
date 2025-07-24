from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from facade import PolicyNavigatorFacade
from handlers.upload import UploadHandler
from handlers.uploaded_doc import UploadedDocHandler

print("Slack token:", os.environ.get("SLACK_TOKEN"))
print("Slack channel:", os.environ.get("SLACK_CHANNEL"))
# The facade will print if notifier is initialized

st.set_page_config(page_title="Policy Navigator Agent", layout="centered")
st.title("Policy Navigator Agent")

slack_token = os.environ.get("SLACK_TOKEN")
slack_channel = os.environ.get("SLACK_CHANNEL")
facade = PolicyNavigatorFacade(slack_token=slack_token, slack_channel=slack_channel) 