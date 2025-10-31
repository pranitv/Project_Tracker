import streamlit as st
import pandas as pd
import plotly.express as px
import os

"""
    App Config
"""
st.set_page_config(page_title="AI Project Tracker", page_icon="🤖", layout="wide")

st.title("🤖 AI Application Development Tracker (2025 Edition)")
st.write("Track your progress across Agentic AI, Multimodal AI, and Automation projects.")

"""
    Load/Initialize Data
"""
CSV_FILE = 'ai_project_tracker.csv'

if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame([
        ["AI Research Assistant", "Agentic AI", "LangChain + GPT-5 + Tavily", 5, False, 0, "❌", "Not started"],
        ["Autonomous Trading Agent", "Agentic AI", "RLlib + PySpark + LangGraph", 5, False, 0, "❌", "Need data feed integration"],
        ["AI Video Editor", "Multimodal AI", "GPT-4o + Whisper + MoviePy", 4, False, 0, "❌", ""],
        ["AI Data Engineer Agent", "Workflow Automation", "LangGraph + Azure ADF + Databricks", 5, False, 0, "❌", ""],
        ["AI Mentor / Career Coach", "Personalized AI", "GPT-4 + Pinecone + Streamlit", 4, False, 0, "❌", ""],
        ["Self-Updating Knowledge Bot", "Knowledge Systems", "LangGraph + Tavily + Pinecone", 5, False, 0, "❌", ""],
        ["Agent Swarm Simulator", "Advanced AI", "CrewAI + AutoGen + GPT-5", 5, False, 0, "❌", ""],
    ], columns=["App Name", "Domain", "Tech Stack", "Priority", "Started", "Progress (%)", "Completed", "Notes"])

"""
    Sidebar controls
"""
st.sidebar.header("📂 Filters")
domain_filter = st.sidebar.multiselect("Filter by Domain", df["Domain"].unique())
priority_filter = st.sidebar.slider("Minimum Priority", 1,5,1)

filtered_df = df.copy()
if domain_filter:
    filtered_df = filtered_df[filtered_df["Domain"].isin(domain_filter)]
filtered_df = filtered_df[filtered_df["Priority"]>= priority_filter]

"""
    Editable Table
"""
st.subheader("🧩 Project Overview")
edited_df = st.data_editor(
    filtered_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Started": st.column_config.CheckboxColumn("Started"),
        "Completed": st.column_config.CheckboxColumn("Completed"),
        "Progress (%)": st.column_config.NumberColumn("Progress (%)", min_value=0, max_value=100, step=5),
        "Priority (1–5)": st.column_config.NumberColumn("Priority", min_value=1, max_value=5, step=1),
    }
)

"""
    Save Data
"""
if st.button("💾 Save Changes"):
    edited_df.to_csv(CSV_FILE, index=False)
    st.success("Progress saved successfully!")

"""
    Stats & Visualization
"""
st.divider()
st.subheader("📊 Progress Summary")

avg_progress = int(edited_df["Progress (%)"].mean())
completed_count = (edited_df["Completed"] == "✅").sum() if "✅" in edited_df["Completed"].values else 0
started_count = edited_df["Started"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Average Progress", f"{avg_progress}%")
col2.metric("Projects Started", started_count)
col3.metric("Total Projects", len(edited_df))

fig = px.bar(
    edited_df,
    x="App Name",
    y="Progress (%)",
    color="Domain",
    title="📈 Progress by Project",
    text="Progress (%)",
)
st.plotly_chart(fig, use_container_width=True)

"""
    Add New Project
"""
st.divider()
st.subheader("➕ Add a New Project")

with st.form("new_project_form"):
    name = st.text_input("App Name")
    domain = st.selectbox("Domain", ["Agentic AI", "Multimodal AI", "Workflow Automation", "Personalized AI", "Knowledge Systems", "Advanced AI"])
    tech = st.text_input("Tech Stack")
    priority = st.slider("Priority (1–5)", 1, 5, 3)
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Project")

    if submitted and name:
        new_row = pd.DataFrame([[name, domain, tech, priority, False, 0, "❌", notes]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success(f"✅ Added '{name}' to your tracker!")