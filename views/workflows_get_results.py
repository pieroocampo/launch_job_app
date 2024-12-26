import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Workflows", divider=True)
st.subheader("Get Job Results")

tab1, tab2 = st.tabs(["Try It", "Code"])

def fetch_workflow_results(workflow_id: str):
    try:
        run = w.jobs.runs_get(run_id=workflow_id)
        return {
            "status": run.state.life_cycle_state,
            "result": run.state.result_state,
        }
    except Exception as e:
        return {"error": str(e)}

if "workflow_check_success" not in st.session_state:
    st.session_state.workflow_check_success = False

with tab1:
    st.info(
        body="""
        To retrieve results from a workflow, provide the workflow run ID.
        Ensure the app's service principal has the necessary permissions to access workflows.
        """,
        icon="ℹ️",
    )

    workflow_id = st.text_input(
        label="Specify the Workflow Run ID",
        placeholder="workflow-id",
    )

    if st.button(label="Get Workflow Results", icon=":material/play-circle: "):
        if not workflow_id.strip():
            st.warning("Please specify a valid workflow run ID.", icon="⚠️")
        else:
            results = fetch_workflow_results(workflow_id.strip())
            if "error" in results:
                st.error(f"Error fetching workflow results: {results['error']}", icon="🚨")
            else:
                st.success("Workflow results retrieved successfully", icon="✅")
                st.json(results)

with tab2:
    st.code("""
    import os
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    workflow_id = "workflow-id"

    run = w.jobs.runs_get(run_id=workflow_id)
    print(f"Workflow status: {run.state.life_cycle_state}")
    print(f"Result: {run.state.result_state}")
    """)
