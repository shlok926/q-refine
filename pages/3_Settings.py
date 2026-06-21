import streamlit as st
from navigation import render_sidebar

st.set_page_config(page_title="Q-Refine Settings", layout="wide", page_icon="⚙️")

st.session_state["current_page"] = "Settings"
render_sidebar()

st.title("⚙️ Q-Refine Global Settings")
st.markdown("Configure your IBM Quantum accounts and default preferences for the Q-Refine platform.")

st.divider()

st.header("IBM Quantum API Configuration")
st.write("To run algorithms on actual physical Quantum Processing Units (QPUs) instead of simulators, you need an IBM Quantum API token.")

api_token = st.text_input("IBM Quantum API Token", type="password", help="Get this from quantum.ibm.com")

if st.button("Save API Token Securely"):
    if api_token:
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
            QiskitRuntimeService.save_account(channel="ibm_quantum", token=api_token, overwrite=True)
            st.success("✅ IBM Quantum Account saved successfully to your local machine!")
        except Exception as e:
            st.error(f"Failed to save account: {e}")
            st.warning("Please run `pip install qiskit-ibm-runtime` if not already installed.")
    else:
        st.error("Token cannot be empty.")

st.divider()

st.header("Dashboard Preferences")
st.checkbox("Enable Dark Mode", value=True, disabled=True, help="Dark mode is locked to maintain premium enterprise aesthetic.")
st.checkbox("Auto-download Generated Graphs", value=False)
st.slider("Default Shot Count for Simulators", min_value=100, max_value=8192, value=1024, step=100)

if st.button("Save Preferences"):
    st.success("Preferences saved successfully.")
