import streamlit as st
import tempfile
import os

from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import AIMessageChunk

from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError


SYSTEM_PROMPT = (
        "You have access to a tool that retrieves contextual information from a PDF document. "
        "Use the tool to help answer user queries."
    )

# ----------------------
# --- API Key prüfen ---
# ----------------------

def check_api_key(api_key: str) -> bool:
    try:
        client = OpenAI(api_key=api_key)
        client.responses.create(
            model="gpt-4.1-mini",
            input="ping"
        )
        return True

    # except AuthenticationError:
    #     # API-Key ist ungültig
    #     return False

    # except (APIConnectionError, RateLimitError):
    #     # Key evtl. gültig, aber temporäres Problem
    #     raise RuntimeError("API momentan nicht erreichbar")
    except Exception:
        return False        




# --------------------
# --- Initial Setup ---
# --------------------

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)


# Session State Init (WICHTIG: alles IMMER initialisieren)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False


# ------------------------
# --- Helper-Functions ---
# ------------------------

def load_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        path = tmp.name

    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
    finally:
        os.unlink(path)

    return docs


# -------------
# --- Tool ---
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


# ----------------
# --- APP ---
# ----------------


st.set_page_config(
    page_title="IMU FDB Chat",
    page_icon="📚",
    layout="wide"
)

# -------------
# --- Sidebar ---
# -------------

with st.sidebar:
    st.image(
        "https://www.massivumformung.de/assets/img/brand/logo_massivumformung.svg",
        width=200
    )

    st.divider()

    # OpenAI API Key
    api_key = st.text_input(
        "OpenAI API-Key",
        type="password",
        placeholder="sk-...",
        help="Den API-Key bekommt man mit einem OpenAI Account unter https://platform.openai.com/account/api-keys",
    )

    if not api_key:
        st.warning("Bitte OpenAI API-Key eingeben.")
        st.stop()

    if st.button("API-Key prüfen"):
        with st.spinner("Prüfe API-Key…"):
            try:
                if check_api_key(api_key):
                    st.success("✅ API-Key ist gültig")
                    st.session_state.api_key_valid = True
                else:
                    st.error("❌ Ungültiger API-Key")
                    st.stop()

            except AuthenticationError:
                st.error("❌ Ungültiger API-Key")

            except (APIConnectionError, RateLimitError):
                st.warning("⚠️ OpenAI API momentan nicht erreichbar")

            except Exception as e:
                st.error(f"Unerwarteter Fehler: {e}")

    if st.session_state.api_key_valid:
        #st.success("✔️ API-Key gesetzt")
        
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Vector Store
        if "vector_store" not in st.session_state:
            st.session_state.vector_store = InMemoryVectorStore(
                OpenAIEmbeddings(model="text-embedding-3-large")
            )

        vector_store = st.session_state.vector_store

        # Modell (Key wird automatisch aus ENV gelesen)
        llm = init_chat_model(
            model="gpt-4.1",
        )

        # -----------------
        # --- Agent ---
        # -----------------

        agent = create_agent(
            model=llm,
            tools=[retrieve_context],
            system_prompt=SYSTEM_PROMPT,
            checkpointer=InMemorySaver()
        )

        # PDF Upload
        uploaded_pdf = st.file_uploader("PDF hochladen", type="pdf")

        if uploaded_pdf and "pdf_indexed" not in st.session_state:
            with st.spinner("PDF wird verarbeitet..."):
                docs = load_pdf(uploaded_pdf)
                splits = text_splitter.split_documents(docs)
                vector_store.add_documents(splits)
                st.session_state.pdf_indexed = True
                st.success("PDF erfolgreich indexiert!")
        
        if not uploaded_pdf:
            st.warning('Bitte PDF hochladen')


    st.markdown(
        "<div style='position:fixed; bottom:15px;'>© 2025 Fabian Pingel</div>",
        unsafe_allow_html=True
    )



# -----------------
# --- Main UI ---
# -----------------

st.title("🔨 massiverCHAT")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("Stelle eine Frage zum PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

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

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

