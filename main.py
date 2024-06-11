import streamlit as st
import subprocess

# Define the function to run the script
def run_script(script_name):
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    return result.stdout, result.stderr

# Streamlit UI
st.title("Run Python Script")

script_selected = st.selectbox("Select a script to run", ["script1.py", "script2.py", "script3.py"])

if st.button(f"Run {script_selected}"):
    st.write(f"Running {script_selected}...")
    stdout, stderr = run_script(script_selected)
    if stdout:
        st.write("Output:\n", stdout)
    if stderr:
        st.write("Errors:\n", stderr)