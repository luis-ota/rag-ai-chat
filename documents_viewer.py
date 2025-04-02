import streamlit as st
import os

from streamlit_pdf_viewer import pdf_viewer

# Initialize session state
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# Show a message when no document is selected
if not st.session_state.selected_doc:
    st.title("Selecione um documento na barra lateral.")


def show_doc(doc_name, doc_path):
    st.title(f"📖 Vendo: {doc_name}")
    with st.sidebar:
        if st.button("❌ Fechar PDF"):
            st.session_state.selected_doc = None
            st.rerun()

    pdf_viewer(doc_path)


with st.sidebar:
    st.title("📁 Documentos disponíveis:")

    if not st.session_state.selected_doc:
        for doc in [entry.path for entry in os.scandir(os.getenv('DOCUMENT_DIR')) if entry.is_file()]:
            if st.button(f"📄 {doc.split('/')[-1]}"):
                st.session_state.selected_doc = doc
                st.rerun()

if st.session_state.selected_doc:
    show_doc(st.session_state.selected_doc.split("/")[-1], st.session_state.selected_doc)
