
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

from modules.master_pipeline import run_decision_analysis

# =====================================================
# API CONFIG
# =====================================================

# IMPORTANT:
# NEVER hardcode API keys inside production code.
# Set them using environment variables.

OPENAI_API_KEY = os.getenv("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")
GROQ_API_KEY = os.getenv("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")

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GenAI Decision Intelligence",
    layout="wide"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }

    .stApp {
        background-color: #0f172a;
        color: white;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    .metric-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1e293b;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.title("🧠 GenAI Decision Intelligence System")

st.markdown(
    """
Hybrid Explainable AI Platform for intelligent decision analysis,
tradeoff evaluation, conflict detection, and grounded narrative reasoning.
"""
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Decision Input")

user_input = st.sidebar.text_area(
    "Describe your priorities, goals, concerns, and preferences:",
    height=250,
    placeholder="Example: I want strong career growth and high salary, but I also care about flexibility and avoiding burnout."
)

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Example Priorities")

st.sidebar.markdown(
    """
- High salary
- Career growth
- Work-life balance
- Flexibility
- Low stress
- Stability
"""
)

# =====================================================
# SAMPLE OPTIONS
# =====================================================

options = pd.DataFrame([

    {
        "name": "Startup X",
        "salary": 95,
        "career_growth": 92,
        "flexibility": 40,
        "stress": 90
    },

    {
        "name": "Corporate Y",
        "salary": 75,
        "career_growth": 65,
        "flexibility": 78,
        "stress": 45
    },

    {
        "name": "Remote Z",
        "salary": 68,
        "career_growth": 60,
        "flexibility": 95,
        "stress": 28
    }
])

benefit_criteria = [
    "salary",
    "career_growth",
    "flexibility"
]

cost_criteria = [
    "stress"
]

# =====================================================
# MAIN ACTION
# =====================================================

if st.sidebar.button("🚀 Run Decision Analysis"):

    if not user_input.strip():
        st.error("Please enter your decision context.")
        st.stop()

    with st.spinner("Running AI analysis..."):

        results = run_decision_analysis(
            user_input=user_input,
            options=options,
            benefit_criteria=benefit_criteria,
            cost_criteria=cost_criteria
        )

    ranked_results = results["ranked_results"]

    # =====================================================
    # TOP METRICS
    # =====================================================

    top_option = ranked_results.iloc[0]["name"]
    confidence = results["confidence"]
    conflicts = len(results["conflicts"])
    questions = len(results["questions"])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🏆 Recommended", top_option)

    with col2:
        st.metric("📊 Confidence", confidence)

    with col3:
        st.metric("⚠️ Conflicts", conflicts)

    with col4:
        st.metric("❓ Questions", questions)

    st.markdown("---")

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Rankings",
        "🧠 Narrative",
        "⚠️ Conflicts",
        "❓ Questions",
        "📈 Charts",
        "📋 Full Report"
    ])

    # =====================================================
    # TAB 1
    # =====================================================

    with tab1:

        st.subheader("Ranked Results")

        st.dataframe(
            ranked_results,
            use_container_width=True
        )

        st.success(
            f"Recommended Option: {top_option}"
        )

    # =====================================================
    # TAB 2
    # =====================================================

    with tab2:

        st.subheader("Narrative Intelligence")

        st.write(results["narrative"])

    # =====================================================
    # TAB 3
    # =====================================================

    with tab3:

        st.subheader("Detected Tradeoffs & Conflicts")

        if len(results["conflicts"]) == 0:

            st.success("No major conflicts detected.")

        else:

            for conflict in results["conflicts"]:
                st.warning(conflict)

    # =====================================================
    # TAB 4
    # =====================================================

    with tab4:

        st.subheader("Adaptive Clarification Questions")

        for question in results["questions"]:
            st.info(question)

    # =====================================================
    # TAB 5
    # =====================================================

    with tab5:

        st.subheader("Final Decision Scores")

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            ranked_results["name"],
            ranked_results["final_score"]
        )

        ax.set_ylabel("Final Scores")
        ax.set_title("Ranked Decision Scores")

        st.pyplot(fig)

        st.subheader("Criteria Comparison")

        criteria = [
            "salary",
            "career_growth",
            "flexibility",
            "stress"
        ]

        fig2, ax2 = plt.subplots(figsize=(10, 5))

        for _, row in ranked_results.iterrows():

            values = [
                row[c]
                for c in criteria
            ]

            ax2.plot(
                criteria,
                values,
                marker='o',
                label=row["name"]
            )

        ax2.legend()

        ax2.set_title("Criteria Comparison Across Options")

        st.pyplot(fig2)

    # =====================================================
    # TAB 6
    # =====================================================

    with tab6:

        st.subheader("Full Explainability Report")

        st.text(results["report"])

else:

    st.info("Enter your decision context in the sidebar and run the analysis.")
```

