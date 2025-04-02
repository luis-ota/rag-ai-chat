from dotenv import load_dotenv
import streamlit as st
from PIL import Image

if __name__ == "__main__":
    load_dotenv()

    st.set_page_config(
        page_icon=Image.open("./assests/favicon.ico"),
        layout="wide",
    )
    st.navigation([
        st.Page("app.py", title="AI Chat", icon='🤖'),
        st.Page("documents_viewer.py", title="Vizualizar documentos", icon='📄')
    ]).run()

