# 🤖 Mini Agent Workflow Orchestrator

**Collaborative AI agents solving complex tasks together.**

This project is a lightweight framework for defining, running, and visualizing multi-agent AI workflows. Instead of messy, chained LLM calls, you can define specialized agents that perform distinct tasks, pass their results to one another, and collaboratively produce a final output.

---

### ✨ Demo

*(This is where you'll embed a GIF of your Streamlit app in action once it's complete!)*

![Demo GIF Placeholder](https://user-images.githubusercontent.com/10284317/144275140-5b1287c8-971c-42b1-a20c-033185a535c8.png)

*The demo shows a user entering a query, and the UI displays the stepwise outputs from a Researcher, Summarizer, and Critic agent before presenting the final polished result.*

---

### 🚀 Features

*   **🧩 Modular Agent Roles:** Define agents with specialized functions (e.g., Researcher, Summarizer, Critic).
*   **⛓️ Workflow Orchestration:** Define complex agent workflows using a simple JSON configuration.
*   **📊 Stepwise Visualization:** A clean Streamlit UI shows the input and output of each agent in the chain for full transparency.
*   **🔌 Pluggable AI Models:** Easily switch between models like GPT-4o-mini or open-source alternatives.
*   **📝 Execution Logging:** Intermediate outputs are logged, perfect for debugging and analysis.
*   **🌐 FastAPI Backend:** A robust, scalable backend serves the orchestration logic.

---

### 🛠️ Tech Stack

*   **Backend:** FastAPI, Python 3.10+
*   **Frontend:** Streamlit
*   **AI Agents:** OpenAI (GPT-4o-mini)
*   **Workflow Config:** JSON
*   **Server:** Uvicorn
*   **Core Libraries:** Pydantic, Requests, python-dotenv

---

### 🏁 Getting Started

Follow these steps to set up and run the project locally.

#### 1. Prerequisites

*   Python 3.10 or higher
*   An [OpenAI API Key](https://platform.openai.com/)

#### 2. Clone the Repository

```bash
git clone https://github.com/RamaPranav01/mini-agent-orchestrator.git
cd mini-agent-orchestrator
```

#### 3. Setup Environment and Install Dependencies

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
# venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file inside the `backend/` directory and add your OpenAI API key:

```ini
# backend/.env
OPENAI_API_KEY="sk-YourSecretKeyHere"
```

#### 5. Run the Application

You need to run two processes in two separate terminals.

**Terminal 1: Start the Backend (FastAPI)**

```bash
uvicorn backend.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

**Terminal 2: Start the Frontend (Streamlit)**

```bash
streamlit run frontend/app.py
```
The web application will open in your browser at `http://localhost:8501`.

---

### 🗺️ Future Roadmap

This project is a foundation. Here are some potential next steps:

*   [ ] **Branching & Conditional Logic:** Allow workflows to branch based on an agent's output (e.g., if a `CriticAgent` finds a flaw, re-run the `SummarizerAgent`).
*   [ ] **Vector DB Memory:** Integrate a vector database like Qdrant or ChromaDB to give agents long-term memory.
*   [ ] **Agent Marketplace:** Create a system to easily add and share new, community-contributed agents.
*   [ ] **Frontend Visualization:** Use a library like Mermaid.js or React Flow to draw the workflow graph dynamically.

---

### 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.