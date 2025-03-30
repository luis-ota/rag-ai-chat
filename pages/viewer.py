import streamlit as st
import os

# Get document name from query parameters
doc_name = st.query_params.get("doc", "")

if not doc_name:
    st.error("No document selected.")
    st.stop()

DOCS_DIR = os.getenv("DOCUMENT_DIR")
doc_path = os.path.join(DOCS_DIR, doc_name)

st.title(f"📖 Viewing: {doc_name}")

# Check if the file exists
if not os.path.exists(doc_path):
    st.error("Document not found.")
    st.stop()

# Display Markdown files
if doc_name.endswith(".md"):
    with open(doc_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
    st.markdown(markdown_content, unsafe_allow_html=True)

# Embed PDF files using an iframe
elif doc_name.endswith(".pdf"):
    pdf_viewer = f"""
    <iframe src="{doc_path}" width="100%" height="600px"></iframe>
    """
    st.markdown(pdf_viewer, unsafe_allow_html=True)

