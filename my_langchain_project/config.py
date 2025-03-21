import os
from dotenv import load_dotenv

load_dotenv()  # Lädt die Variablen aus .env

# Konfigurationen
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "") 