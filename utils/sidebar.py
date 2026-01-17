# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================


import streamlit as st
import os

from utils.api_key import ApiKeyService


# ---------------
# --- Sidebar ---
# ---------------

def render_sidebar():
    with st.sidebar:
        # --- Logo ---
        st.image(
            "https://www.massivumformung.de/assets/img/brand/logo_massivumformung.svg",
            width=200
        )

        st.divider()

        # --- OpenAI API Key --- TODO
        default_api_key = os.getenv("1OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") is not None else ""  # only for development environment, otherwise it should return None
        
        st.text_input(
            label="OpenAI API-Key",
            value=default_api_key,
            key="api_key",
            type="password",
            help="Den API-Key erstellt man mit einem OpenAI Account unter https://platform.openai.com/account/api-keys",
            placeholder="sk-...",
        )

        # Wenn API-Key geändert wurde, dann Session State zurücksetzen
        if st.session_state.api_key != st.session_state.last_api_key:
            st.session_state.last_api_key = st.session_state.api_key
            st.session_state.api_key_valid = False
            st.session_state.api_key_message = None
            st.session_state.pdf_indexed = False
            st.session_state.vector_store = None

            if st.session_state.api_key:
                with st.spinner("⌛ Prüfe API-Key…"):
                    valid, msg = ApiKeyService.validate(st.session_state.api_key)
                st.session_state.api_key_valid = valid
                st.session_state.api_key_message = msg

                if valid:
                    os.environ["OPENAI_API_KEY"] = st.session_state.api_key

        # Status anzeigen
        if st.session_state.api_key_valid:
            st.success("✅ API-Key ist gültig")
        else:
            if st.session_state.api_key_message:
                st.error(st.session_state.api_key_message)
            else:
                st.warning(" ⚠️ Bitte OpenAI API-Key eingeben.")
            st.stop()

