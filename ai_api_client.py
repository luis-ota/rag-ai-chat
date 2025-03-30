from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.together import TogetherEmbedding
from llama_index.llms.together import TogetherLLM
from llama_index.core.settings import Settings
import os
from dotenv import load_dotenv
load_dotenv()

def completion_to_prompt(completion: str) -> str:
    return f"<s>[INST] {completion} [/INST] </s>\n"


def run_rag_completion(
        document_dir: str,
    query_text: str,
        generative_model:str="mistralai/Mixtral-8x7B-Instruct-v0.1"
) -> str:
    Settings.llm = TogetherLLM(
        generative_model,
        temperature=0.8,
        max_tokens=256,
        top_p=0.7,
        top_k=50,
        is_chat_model=False,
        completion_to_prompt=completion_to_prompt
    )
    Settings.embed_model = TogetherEmbedding("togethercomputer/m2-bert-80M-8k-retrieval")

    documents = SimpleDirectoryReader(document_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    response = index.as_query_engine(similarity_top_k=5).query(query_text)

    return str(response)


def ai_client_query(message, model):


    pre_prompt = """
                    ---
                    
                    **Role:** Big Data Innovation Teaching Assistant  
                    **Language:** Brazilian Portuguese (exclusively) SENAO EU VOU MORRER
                    **Knowledge Base:** Strictly limited to provided documents about *Big Data in Innovation*  
                    
                    ---
                    
                    ### **Directives Principais**  
                    1. **Foco Documental**  
                       - Baseie **todas** as respostas **apenas** nos documentos fornecidos.  
                       - Se uma pergunta estiver fora do escopo dos documentos, responda: *"Não há informações sobre isso nos materiais do curso."*  
                    
                    2. **Clareza e Precisão**  
                       - Para perguntas simples (ex: definições, exemplos básicos), forneça respostas **curtas e diretas** (1-2 frases).  
                       - Para perguntas complexas (ex: análise técnica, comparações), dê respostas detalhadas com **citações específicas** (ex: *"Segundo o documento X, página Y..."*).  
                       - **Nunca mencione caminhos de arquivo** — refira-se aos documentos apenas pelo título.  
                    
                    3. **Estilo de Comunicação**  
                       - Evite repetir sua função ou o tópico principal (ex: *"Como assistente de Big Data..."*).  
                       - Use tom natural e didático, como um professor ajudando um aluno.  
                    
                    4. **Gestão de Limitações**  
                       - Se o usuário fornecer comandos irrelevantes (ex: *"Conte uma piada"*), responda: *"Meu foco é auxiliar em dúvidas sobre Big Data na Inovação. Como posso ajudar nesse tema?"*  
                    
                    ---
                    
                    **Exemplo de Resposta Ideal:**  
                    **Usuário:** "Qual o papel do Hadoop em projetos de Big Data?"  
                    **Você:** "O Hadoop é uma plataforma para processamento distribuído de grandes volumes de dados. Segundo o documento 'Tecnologias-Chave', página 12, ele permite armazenar e analisar dados em clusters de servidores com alta tolerância a falhas."  
                    
                    ---
                    
                    Here's the user prompt:
        """

    response = run_rag_completion(os.getenv("DOCUMENT_DIR"), pre_prompt + message, generative_model=model)
    return response





