import os
from pathlib import Path
from dotenv import load_dotenv

# Securely compute the path and load environment variables before importing modules
base_path = Path(__file__).resolve().parent
load_dotenv(dotenv_path=base_path / ".env")

import streamlit as st
import backend
import ai_agent


# ─── Helpers ──────────────────────────────────────────────────────────────────

def plan_to_markdown(target: str, gap: list[str], plan: dict) -> str:
    """Serializes the generated roadmap into a clean, portable Markdown document."""
    # 1. Start with the headers
    lines = [
        f"# KariyerPilot Blueprint: {target}",
        f"\n## Summary\n{plan.get('summary', '')}",
        "\n## Skill Gaps to Close"
    ]

    # 2. Add the gaps using clean, readable standard logic
    if gap:
        lines.extend([f"- {s}" for s in gap])
    else:
        lines.append("- None — full coverage achieved!")

    # 3. Add the timeline header
    lines.append("\n## 4-Week Study Timeline")

    # 4. Loop through the weeks
    for week in plan.get("timeline", []):
        lines.append(f"\n### Week {week.get('week')}: {week.get('focus')}")
        lines.append("**Tasks:**")
        lines.extend(f"- [ ] {t}" for t in week.get("tasks", []))
        lines.append(f"\n**Topics:** {', '.join(week.get('btk_topics', []))}")

    # 5. Finish with the project
    lines.extend([
        f"\n## Capstone Project: {plan.get('project_name')}",
        plan.get("project_details", ""),
    ])

    return "\n".join(lines)


def clear_cache():
    """Wipes the stored roadmap so the next render triggers a fresh Gemini call."""
    st.session_state.pop("plan_cache", None)


# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="KariyerPilot AI", layout="wide")

st.title("🚀 KariyerPilot AI")
st.caption("Composite AI Career Recommendation & Technical Roadmap Engine")


# ─── Layout ───────────────────────────────────────────────────────────────────

col_in, col_out = st.columns([1, 2], gap="large")

with col_in:
    st.subheader("Your Technical Profile")
    skills = st.multiselect("Select your current skills/tools:", backend.VOCAB)
    target = st.selectbox("Select target career track:", list(backend.PROFILES.keys()))

    run_btn = st.button(
        "Generate Strategy Blueprint",
        type="primary",
        use_container_width=True,
    )

    # Only show Regenerate when a cached plan already exists
    if st.session_state.get("plan_cache"):
        st.button(
            "🔄 Regenerate",
            on_click=clear_cache,
            use_container_width=True,
        )


# ─── Output Column ────────────────────────────────────────────────────────────

with col_out:
    # Trigger on explicit button press OR when a cached plan is already loaded
    if run_btn or st.session_state.get("plan_cache"):

        if not skills:
            st.warning("Please select at least one skill to calculate your baseline profile.")
            st.stop()

        # 1. Deterministic pipeline (always runs — cheap and instant)
        scores    = backend.get_scores(skills)
        gap       = backend.get_gap(skills, target)
        archetype = backend.get_cluster(skills)

        # 2. Statistical dashboards
        st.subheader("📊 Match Analytics & Predictive Clustering")

        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.metric(label=f"{target} Match Score", value=f"{scores.get(target, 0.0)}%")
        with m_col2:
            st.metric(label="Assigned Cohort Persona", value=archetype.split(" (")[0])

        with st.expander("Show Complete Market Compatibility Scores"):
            st.dataframe(
                [{"Career Track": k, "Compatibility Match": f"{v}%"} for k, v in scores.items()],
                use_container_width=True,
            )

        if gap:
            st.info(f"💡 **Detected Skill Gaps for {target}:** {', '.join(gap)}")
        else:
            st.success(f"✅ You possess all fundamental skills mapped for {target}!")

        # 3. Generative layer — only calls Gemini when there is no cached plan
        st.markdown("---")
        st.subheader("⚡ AI Guided Training Blueprint")

        if run_btn or "plan_cache" not in st.session_state:
            with st.spinner("Synthesizing personalized study plan..."):
                try:
                    plan = ai_agent.generate_roadmap(target, skills, gap, archetype)
                    st.session_state["plan_cache"] = plan
                except Exception as e:
                    st.error("The API Pipeline Encountered an Exception:")
                    st.exception(e)
                    st.stop()

        plan = st.session_state["plan_cache"]

        # 4. Render the roadmap
        st.write(plan.get("summary", ""))

        tab_titles = [f"Week {w.get('week')}" for w in plan.get("timeline", [])]
        if tab_titles:
            tabs = st.tabs(tab_titles)
            for i, week in enumerate(plan.get("timeline", [])):
                with tabs[i]:
                    st.markdown(f"### 🎯 Focus: {week.get('focus')}")
                    st.markdown("**Action Items:**")
                    for task in week.get("tasks", []):
                        st.write(f"- [ ] {task}")
                    st.markdown("**Suggested Study Topics:**")
                    st.caption(", ".join(week.get("btk_topics", [])))

        st.markdown(f"### 🛠️ Capstone Project Portfolio Goal: {plan.get('project_name')}")
        st.write(plan.get("project_details", ""))

        # 5. Export
        st.markdown("---")
        st.download_button(
            label="📥 Export Blueprint as Markdown",
            data=plan_to_markdown(target, gap, plan),
            file_name=f"kariyer_blueprint_{target.lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    else:
        st.info("Configure your current tools in the left pane and launch the engine to compute matching paths.")