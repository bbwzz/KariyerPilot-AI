import os
from pathlib import Path
from dotenv import load_dotenv

# Step 1: Securely compute the path and load environment variables before importing modules
base_path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=base_path / ".env")

# Step 2: Standard application imports
import streamlit as st
import backend
import ai_agent

# Initialize the Streamlit page configuration
st.set_page_config(page_title="KariyerPilot AI", layout="wide")

st.title("🚀 KariyerPilot AI")
st.caption("Composite AI Career Recommendation & Technical Roadmap Engine")

# Left Column: Inputs | Right Column: Analytics & Generated Roadmaps
col_in, col_out = st.columns([1, 2], gap="large")

with col_in:
    st.subheader("Your Technical Profile")
    skills = st.multiselect("Select your current skills/tools:", backend.VOCAB)
    target = st.selectbox("Select target career track:", list(backend.PROFILES.keys()))
    run_btn = st.button("Generate Strategy Blueprint", type="primary", use_container_width=True)

with col_out:
    if run_btn:
        if not skills:
            st.warning("Please select at least one skill to calculate your baseline profile.")
            st.stop()

        # 1. Pipeline Math Operations (Local Machine)
        scores = backend.get_scores(skills)
        gap = backend.get_gap(skills, target)
        archetype = backend.get_cluster(skills)

        # 2. Render Statistical Dashboards
        st.subheader("📊 Match Analytics & Predictive Clustering")

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(label=f"{target} Match Score", value=f"{scores.get(target, 0.0)}%")
        with m_col2:
            st.metric(label="Assigned Cohort Persona", value=archetype.split(" (")[0])

        with st.expander("Show Complete Market Compatibility Scores"):
            st.dataframe(
                [{"Career Track": k, "Compatibility Match": f"{v}%"} for k, v in scores.items()],
                use_container_width=True
            )

        if gap:
            st.info(f"💡 **Detected Skill Gaps for {target}:** {', '.join(gap)}")
        else:
            st.success(f"✅ You possess all fundamental skills mapped for {target}!")

        # 3. Generative Layer Synthesis (Gemini Connection)
        st.markdown("---")
        st.subheader("⚡ AI Guided Training Blueprint")

        with st.spinner("Synthesizing personalized study plan..."):
            try:
                plan = ai_agent.generate_roadmap(target, skills, gap, archetype)
                st.write(plan.get("summary", ""))

                # Tabbed UI for timeline tracking
                tab_titles = [f"Week {w.get('week')}" for w in plan.get("timeline", [])]
                if tab_titles:
                    tabs = st.tabs(tab_titles)
                    for i, w_data in enumerate(plan.get("timeline", [])):
                        with tabs[i]:
                            st.markdown(f"### 🎯 Focus: {w_data.get('focus')}")
                            st.markdown("**Action Items:**")
                            for task in w_data.get("tasks", []):
                                st.write(f"- [ ] {task}")
                            st.markdown("**Suggested Study Topics:**")
                            st.caption(", ".join(w_data.get("btk_topics", [])))

                # Capstone Project Section
                st.markdown(f"### 🛠️ Capstone Project Portfolio Goal: {plan.get('project_name')}")
                st.write(plan.get("project_details", ""))

            except Exception as e:
                st.error("The API Pipeline Encountered an Exception:")
                st.exception(e)
    else:
        st.info("Configure your current tools in the left pane and launch the engine to compute matching paths.")