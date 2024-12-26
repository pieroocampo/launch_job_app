import os
import io
import streamlit as st
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

st.header(body="Workflows", divider=True)
st.subheader("Run a Job")

tab1, tab2 = st.tabs(["Try It", "Code"])

def trigger_workflow(job_id: str, parameters: dict):
    try:
        run = w.jobs.run_now(job_id=job_id, notebook_params=parameters)
        return {
            "run_id": run.run_id,
            "state": "Triggered",
        }
    except Exception as e:
        return {"error": str(e)}

if "workflow_trigger_success" not in st.session_state:
    st.session_state.workflow_trigger_success = False

with tab1:
    st.info(
        body="""
        To trigger a workflow, provide the job ID and the input parameters as key-value pairs.
        Ensure the app's service principal has the necessary permissions to trigger workflows.
        """,
        icon="ℹ️",
    )

    job_id = st.text_input(
        label="Specify the Job ID",
        placeholder="job-id",
    )

    parameters_input = st.text_area(
        label="Specify Input Parameters (JSON format)",
        placeholder="{\"param1\": \"value1\", \"param2\": \"value2\"}",
    )

    if st.button(label="Trigger Workflow"):
        if not job_id.strip():
            st.warning("Please specify a valid job ID.", icon="⚠️")
        elif not parameters_input.strip():
            st.warning("Please specify input parameters.", icon="⚠️")
        else:
            try:
                parameters = eval(parameters_input.strip())
                results = trigger_workflow(job_id.strip(), parameters)
                if "error" in results:
                    st.error(f"Error triggering workflow: {results['error']}", icon="🚨")
                else:
                    st.success("Workflow triggered successfully", icon="✅")
                    st.json(results)
            except Exception as e:
                st.error(f"Error parsing input parameters: {e}", icon="🚨")

with tab2:
    st.code("""
    import os
    from databricks.sdk import WorkspaceClient

    w = WorkspaceClient()

    job_id = "job-id"
    parameters = {
        "param1": "value1",
        "param2": "value2"
    }

    try:
        run = w.jobs.run_now(job_id=job_id, notebook_params=parameters)
        print(f"Triggered workflow with run ID: {run.run_id}")
    except Exception as e:
        print(f"Error: {e}")
    """)

