# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================


import streamlit as st


# ----------------------
# --- Session State ----
# ----------------------

def init_session_state():
    defaults = {
        "messages": [],
        "api_key_valid": False,
        "api_key_message": None,
        "last_api_key": None,
        "pdf_indexed": False,
        "vector_store": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
