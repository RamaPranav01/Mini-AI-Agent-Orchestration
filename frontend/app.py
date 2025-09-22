import streamlit as st
import requests
from streamlit_mermaid import st_mermaid

# --- Page Configuration ---
st.set_page_config(
    page_title="Mini Agent Orchestrator",
    page_icon="🤖",
    layout="wide"
)

# --- API Configuration ---
API_BASE_URL = "http://127.0.0.1:8000"

# --- Helper Functions ---

def generate_mermaid_diagram(workflow_steps):
    """Dynamically generates a Mermaid.js flowchart from workflow steps."""
    if not workflow_steps:
        return ""
    
    diagram = "graph TD;\n"
    # A(User Input) --> B(Researcher);
    # B --> C(Summarizer);
    # C --> D(Critic);
    # D --> E(Presenter);
    # E --> F(Final Output);
    
    # Define nodes
    nodes = {
        "start": "A[User Input]",
        "end": f"{chr(ord('A') + len(workflow_steps) + 1)}[Final Output]"
    }
    for i, step in enumerate(workflow_steps):
        node_id = chr(ord('A') + i + 1)
        nodes[step['agent']] = f"{node_id}[{step['agent']}]"

    # Define links
    diagram += f"    {nodes['start']} --> {nodes[workflow_steps[0]['agent']]};\n"
    for i in range(len(workflow_steps) - 1):
        from_agent = workflow_steps[i]['agent']
        to_agent = workflow_steps[i+1]['agent']
        diagram += f"    {nodes[from_agent]} --> {nodes[to_agent]};\n"
    diagram += f"    {nodes[workflow_steps[-1]['agent']]} --> {nodes['end']};\n"
    
    return diagram


def get_workflow_config():
    """Fetches the workflow configuration from the backend."""
    try:
        response = requests.get(f"{API_BASE_URL}/get-workflow-config")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not fetch workflow configuration. Is the backend running? Error: {e}")
        return None

# --- Main Application UI ---
st.title("🤖 Mini Agent Workflow Orchestrator")
st.markdown(
    "Define a query and watch as a team of AI agents collaborate to provide a result. "
    "The workflow below is dynamically generated from the backend configuration."
)

# Fetch and display the workflow diagram
workflow_config = get_workflow_config()
if workflow_config and "steps" in workflow_config:
    st.subheader("Workflow Diagram")
    mermaid_diagram = generate_mermaid_diagram(workflow_config["steps"])
    st_mermaid(mermaid_diagram)
else:
    st.warning("Could not load workflow diagram.")


# --- Input and Execution Section ---
st.subheader("1. Input Your Query")
user_query = st.text_area(
    "Enter the task you want the AI agents to solve:",
    "Summarize the pros and cons of AI regulation in India, including perspectives from tech companies and government.",
    height=100
)

if st.button("🚀 Run Workflow"):
    if not user_query:
        st.error("Please enter a query to run the workflow.")
    else:
        with st.spinner("Agents are at work... This may take a moment. 🧠"):
            try:
                # Call the Backend API to run the workflow
                payload = {"query": user_query}
                response = requests.post(f"{API_BASE_URL}/run-workflow", json=payload)
                response.raise_for_status()
                
                result = response.json()
                
                # Display Results
                st.subheader("2. Final Result")
                st.success(result.get("final_output", "No output received."))

                st.subheader("3. Agent Execution Log")
                st.info("See how the agents worked together, step by step.")

                workflow_log = result.get("workflow_log", [])
                if workflow_log:
                    for log_entry in workflow_log:
                        agent_name = log_entry.get('agent', f"Step {log_entry.get('step')}")
                        with st.expander(f"**Step {log_entry.get('step')}: {agent_name}**", expanded=False):
                            st.markdown("##### 📥 Input to Agent")
                            st.text_area("Input", value=log_entry.get('input', ''), height=150, disabled=True, key=f"input_{log_entry.get('step')}")
                            st.markdown("##### 📤 Output from Agent")
                            st.text_area("Output", value=log_entry.get('output', ''), height=250, disabled=True, key=f"output_{log_entry.get('step')}")
                else:
                    st.warning("Workflow log is empty.")

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend API. Is it running? Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")