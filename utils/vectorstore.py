# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================


from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from utils.config import EMBEDDING_MODEL_NAME


# --------------------
# --- Vector Store ---
# --------------------

def init_vector_store():
    return InMemoryVectorStore(
        OpenAIEmbeddings(
            model=EMBEDDING_MODEL_NAME,
        )
    )
