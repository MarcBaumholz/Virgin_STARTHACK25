# Virgin Sustainability Platform - LangChain & Qdrant Agent

## Übersicht
Dieses Projekt demonstriert den Aufbau eines KI-Agenten mithilfe von LangChain, der
- CSV-Daten (Virgin-Initiativen) lädt,
- mittels SentenceTransformer-Embeddings in einen Qdrant-Vektorstore überführt und
- über einen RetrievalQA-Chain abfragbar macht.

Der Agent nutzt einen benutzerdefinierten LLM-Wrapper (OpenRouterLLM), der ein kostenloses Google-Modell über OpenRouter anspricht.

## Enthaltene Funktionalitäten
1. **Datenlade-Tool (data_loader.py):** Liest die CSV-Datei ein und wandelt jede Zeile in ein Document um.
2. **Vectorstore-Integration (vector_store.py):** Verwendet HuggingFaceEmbeddings (z. B. "all-MiniLM-L6-v2") und speichert die Vektoren in Qdrant.
3. **Agent-Implementierung (agent.py):** 
   - Custom LLM (OpenRouterLLM) zur Nutzung der OpenRouter-API.
   - Aufbau eines RetrievalQA-Chain, der den Vektorstore als Retriever nutzt.
4. **Hauptprogramm (main.py):** Startet eine Kommandozeilen-Interaktion, in der der Agent Fragen beantwortet.

## Setup und Ausführung
1. Klone das Repository und navigiere in den Projektordner.
2. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
3. Lege eine `.env`-Datei an und setze deinen `OPENROUTER_API_KEY` (und ggf. Qdrant-Konfiguration).
4. Stelle sicher, dass Qdrant läuft (lokal oder als Service).
5. Baue den Vektorstore und starte den Agenten:
   ```bash
   python main.py
   ```

## Tools im Überblick
- **LangChain:** Framework zur Erstellung modularer LLM-Pipelines. Hier nutzen wir es für die RetrievalQA-Kette.
- **Qdrant:** Vektor-Datenbank, in der die Embeddings der Dokumente gespeichert werden. Vorteile: Open Source, speziell für Vektorsuche optimiert.  
- **OpenRouterLLM:** Ein benutzerdefinierter LLM-Wrapper, der ein kostenloses Google-Modell ansteuert.
- **HuggingFaceEmbeddings:** Wir nutzen ein kostenloses Modell (z. B. "all-MiniLM-L6-v2") für die Generierung der Dokumentenembeddings.

## Unterschiede & Überlegungen
- **LangChain vs. LlamaIndex:**  
  LangChain bietet eine umfassendere, modulare Pipeline (Chains, Agents, Tools) und ist ideal für komplexe Workflows. LlamaIndex ist dagegen fokussiert auf schnelles Dokumentenindexing und Retrieval.
- **RAG-System:**  
  Für ein Retrieval-Augmented Generation (RAG)-System eignen sich Vektor-Datenbanken wie Qdrant sehr gut. Für kleinere Projekte kann auch ein lokaler FAISS-Index genutzt werden.
- **Datenbanken:**  
  - **Qdrant:** Hervorragend für Vektorsuche, open source und skalierbar.  
  - **Supabase:** All-in-one-Lösung (Postgres + Vektor-Suche), gut wenn man bereits relationales DB-Management nutzt.  
  - **Neo4j:** Sehr mächtig bei graphbasierten Abfragen (z. B. komplexe Beziehungen zwischen Projekten, Regionen und Partnern), kann aber für reines Retrieval überdimensioniert sein. 