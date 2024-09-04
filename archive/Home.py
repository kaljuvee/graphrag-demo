import streamlit as st
from graphrag.index import initialize_workspace, run_indexing_pipeline
from graphrag.query import run_query
import os

print("Starting the app")

st.title("GraphRAG Demo")

print("Title set")

# Sidebar for workspace initialization and indexing
st.sidebar.header("Workspace Setup")
root_path = st.sidebar.text_input("Root Path", value="./ragtest")

print(f"Root path set to: {root_path}")

if st.sidebar.button("Initialize Workspace"):
    print("Initialize Workspace button clicked")
    initialize_workspace(root_path=root_path)
    st.sidebar.success(f"Workspace initialized at {root_path}")

if st.sidebar.button("Run Indexing Pipeline"):
    print("Run Indexing Pipeline button clicked")
    run_indexing_pipeline(root_path=root_path)
    st.sidebar.success("Indexing pipeline completed")

# Main area for querying
st.header("Query Engine")

query = st.text_input("Enter your query:")
print(f"Query entered: {query}")

method = st.radio("Select query method:", ("global", "local"))
print(f"Method selected: {method}")

if st.button("Run Query"):
    print("Run Query button clicked")
    if not os.path.exists(root_path):
        st.error(f"Workspace not found at {root_path}. Please initialize the workspace first.")
    else:
        with st.spinner("Processing query..."):
            result = run_query(root_path=root_path, method=method, query=query)
        st.subheader("Query Result:")
        st.write(result)

print("End of script")