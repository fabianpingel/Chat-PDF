# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================


import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader

# --------------------
# --- PDF Loader ----
# --------------------

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
