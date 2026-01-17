# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================


# Text-Splitter Konfiguration
CHUNK_SIZE = 1000      # Größe der Text-Segmente
CHUNK_OVERLAP = 200    # Überlappung zwischen den Segmenten
# ------------------------


# System Prompt für den Chatbot
SYSTEM_PROMPT = (
        "You have access to a tool that retrieves contextual information from a PDF document. "
        "Use the tool to help answer user queries."
    )
# ------------------------


# Chat Modell Konfiguration
CHAT_MODEL_NAME = "gpt-4.1"
CHAT_TEMPERATURE = 0.2
# ------------------------  

# Embedding Modell Konfiguration
EMBEDDING_MODEL_NAME = "text-embedding-3-large"
# ------------------------  



