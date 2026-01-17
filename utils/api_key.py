# =============================================================================
# Project: IMU Chat PDF
# Author: Fabian Pingel
# Copyright (c) 2025 Fabian Pingel
# All rights reserved.
# =============================================================================

from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError

class ApiKeyService:
    @staticmethod
    def validate(api_key: str) -> tuple[bool, str]:
        try:
            client = OpenAI(api_key=api_key)
            client.responses.create(
                model="gpt-4.1-mini",
                input="ping"
            )
            return True, "✅ API-Key ist gültig"

        except AuthenticationError:
            return False, "❌ Ungültiger API-Key"

        except (APIConnectionError, RateLimitError):
            return False, "⌛ OpenAI API momentan nicht erreichbar"

        except Exception as e:
            return False, f"❌ Unerwarteter Fehler: {e}"
