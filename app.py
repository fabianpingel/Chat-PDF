# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================

import streamlit as st

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.messages import AIMessageChunk
from langchain.agents import create_agent

from langgraph.checkpoint.memory import InMemorySaver

from utils.state import init_session_state
from utils.sidebar import render_sidebar
from utils.pdf import load_pdf
from utils.vectorstore import init_vector_store
from utils.config import SYSTEM_PROMPT, CHUNK_SIZE, CHUNK_OVERLAP, CHAT_MODEL_NAME

from dotenv import load_dotenv
load_dotenv()


# ---------------------
# --- Initial Setup ---
# ---------------------

# App Config
st.set_page_config(
    page_title="IMU Chat PDF",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session State Init
init_session_state()

# Sidebar rendern
render_sidebar()

# Vector Store sicher initialisieren
if st.session_state.vector_store is None:
    st.session_state.vector_store = init_vector_store()
# Vector Store aus Session State
vector_store = st.session_state.vector_store

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    add_start_index=True
)



# -------------
# --- Tool ----
# -------------

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve relevant information from the uploaded PDF."""
    retrieved_docs = vector_store.similarity_search(query, k=3)

    serialized = "\n\n".join(
        f"Quelle: {doc.metadata}\n{doc.page_content}"
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


# -------------
# --- Agent ---
# -------------

# Model initialisieren
llm = init_chat_model(
        model=CHAT_MODEL_NAME,
    )

# Agent erstellen
agent = create_agent(
    model=llm,
    tools=[retrieve_context],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver()
)



# ------------------
# --- PDF Upload ---
# ------------------

with st.sidebar:

    # PDF Upload
    st.file_uploader(
        label="PDF hochladen", 
        type="pdf",
        accept_multiple_files=False,
        key='uploaded_pdf',
        help="Hier das PDF-Dokument hochladen, zu dem Fragen gestellt werden sollen."
    )

    # PDF wurde hochgeladen & noch nicht indexiert
    if st.session_state.uploaded_pdf and not st.session_state.pdf_indexed:
        with st.spinner("⌛ PDF wird verarbeitet..."):
            docs = load_pdf(st.session_state.uploaded_pdf)
            splits = text_splitter.split_documents(docs)
            vector_store.add_documents(splits)
            st.session_state.pdf_indexed = True
            st.success("✅ PDF erfolgreich indexiert!")

    # PDF noch nicht hochgeladen   
    if not st.session_state.uploaded_pdf:
        st.session_state.pdf_indexed = False
        st.session_state.messages = []
        st.session_state.vector_store = None ##
        st.warning('⚠️ Bitte PDF hochladen')

    # Footer
    st.markdown(
        "<div style='position:fixed; bottom:15px;'>© 2025 Fabian Pingel</div>",
        unsafe_allow_html=True
    )



# -----------------
# --- MAIN Chat ---
# -----------------

if st.session_state.pdf_indexed:
 
    # Title
    st.title("🔨 massiverCHAT")

    # Chat-Verlauf anzeigen
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # Neue Nachricht eingeben
    if prompt := st.chat_input("Stelle eine Frage ans PDF..."):
        # Nutzer-Nachricht speichern & anzeigen
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # Antwort generieren & anzeigen
        with st.chat_message("assistant"):
            placeholder = st.empty()
            answer = ""

            for stream_mode, chunk in agent.stream(
                {"messages": [{"role": "user", "content": prompt}]},
                {"configurable": {"thread_id": "default"}},
                stream_mode=["values", "messages", "custom"]
            ):
                if stream_mode == "messages":
                    token, metadata = chunk

                    if isinstance(token, AIMessageChunk):
                        answer += token.content
                        placeholder.markdown(answer)

                if stream_mode == "values":
                    pass
        
        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
