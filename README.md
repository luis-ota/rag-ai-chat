# AI Chat - RAG para Big Data e Inovação

Este projeto é um chatbot baseado em **Streamlit** que utiliza **RAG (Retrieval-Augmented Generation)** para fornecer respostas sobre **Big Data e Inovação**. Ele suporta múltiplos modelos de IA, incluindo **Gemini** e **Llama 3**, e faz uso de embeddings para busca eficiente em documentos.

---

## Funcionalidades
- Interface interativa via **Streamlit**.
- Seleção de modelos **Gemini** e **Llama 3**.
- Indexação eficiente de documentos para respostas contextuais (**RAG**).
- Exibição de respostas em tempo real com efeito de digitação.
- Cache para evitar reinicialização desnecessária dos modelos e documentos.

---

## Tecnologias Utilizadas
- **Python**
- **Streamlit**
- **LlamaIndex** (para busca vetorial e embeddings)
- **Google GenAI** e **Together AI** (para LLMs e embeddings)
- **dotenv** (para gerenciamento de chaves de API)
- **Concurrent Futures** (para execução assíncrona)

---

## Como Executar

### Clonar o Repositório
```sh
  git clone https://github.com/seu-usuario/ai-chat-rag.git
  cd ai-chat-rag
```

### Criar um Ambiente Virtual e Instalar Dependências
```sh
  python -m venv venv
  source venv/bin/activate  # No Windows: venv\Scripts\activate
  pip install -r requirements.txt
```

### Configurar as Chaves de API
Crie um arquivo **.env** na raiz do projeto e adicione suas chaves:
```
GEMINI_API_KEY=your-gemini-api-key
TOGETHER_API_KEY=your-together-api-key
DOCUMENT_DIR=path/to/documents
```

### Executar o Chatbot
```sh
  streamlit run app.py
```

---

## Como Funciona
1. O chatbot recebe perguntas do usuário.
2. O modelo de IA processa a pergunta e busca informações relevantes nos documentos indexados (**RAG**).
3. O resultado é exibido no **Streamlit**, com efeito de digitação e formatação correta.
