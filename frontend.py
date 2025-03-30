import os

import streamlit as st
import time
from ai_api_client import ai_client_query
import concurrent.futures

class AIChatApp:
    def __init__(self):
        self.initialize_session()

    def initialize_session(self):
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "Estou aqui para te ajudar com Big Data em Inovação! 👇"}
            ]
        if "selected_model" not in st.session_state:
            st.session_state['selected_model'] = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        if 'loading' not in st.session_state:
            st.session_state['loading'] = False
        if 'doc' not in st.session_state:
            st.session_state['doc'] = ''

    def display_sidebar(self):
        st.sidebar.title("Configurações")
        models = {
                    "mistralai/Mixtral-8x7B-Instruct-v0.1": "Mixtral-8x7B Instruct v0.1",
                    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free": "DeepSeek R1 70B",
                     "meta-llama/Llama-3-70b-chat-hf": "Llama-3 70B ",
                     "Qwen/Qwen2.5-72B-Instruct-Turbo": "Qwen2.5 72B Instruct Turbo ",
                     "cartesia/sonic-2": "Cartesia/Sonic-2"
        }

        model = st.sidebar.selectbox(
            "Escolha o modelo desejado",
            list(models.values()),
            index=0,
        )
        st.session_state.selected_model = {v: k for k, v in models.items()}.get(model)

        with st.sidebar.container():
            st.title("Documentos usados:")
            for doc in [entry.path for entry in os.scandir(os.getenv('DOCUMENT_DIR')) if entry.is_file()]:
                if st.button(f"📄 {doc.split("/")[-1]}"):
                    st.session_state.selected_doc = doc
                    st.switch_page(f"/viewer?doc={doc}")

    def display_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def get_ai_response(self, user_input: str, model) -> str:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(ai_client_query, user_input, model)
            return future.result()

    def chat_loop(self, assistant_response=None):
        if not st.session_state.loading:
            if prompt := st.chat_input("What is up?"):
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("user"):
                    st.markdown(prompt)

                with st.chat_message("assistant"):
                    st.session_state.loading = True
                    message_placeholder = st.empty()
                    full_response = ""

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self.get_ai_response, prompt, st.session_state.selected_model)

                        thinking_text = "Pensando..."
                        while not future.done():
                            for i in range(len(thinking_text)):
                                tt_list = list(thinking_text)
                                tt_list[i] =  "🤔"
                                message_placeholder.markdown(f"{''.join(tt_list)}")
                                time.sleep(0.1)

                        assistant_response = future.result()

                    for chunk in assistant_response.split():
                        for char in chunk:
                            full_response += char
                            message_placeholder.markdown(full_response + "▌")
                            time.sleep(0.035)
                        full_response += " "

                    message_placeholder.markdown(full_response)

                st.session_state.messages.append({"role": "assistant", "content": full_response})

            st.session_state.loading = False

    def run(self):
        st.title("🤖 AI Chat made by ![Luis](github.com/luis-ota)")
        st.caption("RAG para materia de Bigdata.")

        self.display_sidebar()
        self.display_messages()
        self.chat_loop()


if __name__ == "__main__":
    app = AIChatApp()
    app.run()
