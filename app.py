import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.master_pipeline import run_decision_analysis
from modules.domain_criteria import DOMAIN_CRITERIA

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
Universal Explainable AI Platform for decision analysis,
tradeoff evaluation, conflict detection, and strategic reasoning.
"""
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("⚙️ Decision Setup")

# =====================================================
# DOMAIN SELECTION
# =====================================================

domain = st.sidebar.selectbox(
    "Select Decision Domain",
    [
        "Career",
        "Education",
        "Investment",
        "Tech Purchase",
        "Food",
        "Fitness"
    ]
)

criteria = DOMAIN_CRITERIA[domain]

# =====================================================
# USER CONTEXT
# =====================================================

user_input = st.sidebar.text_area(
    "Describe your priorities and goals:",
    height=200,
    placeholder="Example: I want strong career growth but also flexibility and low stress."
)

# =====================================================
# OPTION INPUTS
# =====================================================

st.sidebar.markdown("---")

num_options = st.sidebar.slider(
    "Number of Options",
    2,
    5,
    2
)

option_names = []

for i in range(num_options):

    option = st.sidebar.text_input(
        f"Option {i+1}",
        placeholder="Enter option name"
    )

    option_names.append(option)

# =====================================================
# WEIGHT INPUTS
# =====================================================

st.sidebar.markdown("---")

st.sidebar.subheader("🎯 Criteria Importance")

weights = {}

for criterion in criteria:

    weights[criterion] = st.sidebar.slider(
        f"{criterion}",
        1,
        10,
        5
    )

# =====================================================
# OPTION SCORING INPUTS
# =====================================================

st.markdown("## 📋 Option Evaluation")

option_data = []

for option in option_names:

    if option.strip() == "":
        continue

    st.subheader(option)

    scores = {
        "name": option
    }

    cols = st.columns(len(criteria))

    for idx, criterion in enumerate(criteria):

        with cols[idx]:

            score = st.slider(
                f"{criterion}",
                1,
                10,
                5,
                key=f"{option}_{criterion}"
            )

            scores[criterion] = score

    option_data.append(scores)

# =====================================================
# CREATE DATAFRAME
# =====================================================

options_df = pd.DataFrame(option_data)

# =====================================================
# RUN ANALYSIS
# =====================================================

if st.button("🚀 Run Decision Analysis"):

    if len(option_data) < 2:

        st.error("Please enter at least 2 options.")
        st.stop()

    if not user_input.strip():

        st.error("Please describe your priorities.")
        st.stop()

    with st.spinner("Running AI analysis..."):

        results = run_decision_analysis(
            user_input=user_input,
            options=options_df,
            criteria=criteria,
            weights=weights
        )

    ranked_results = results["ranked_results"]

    # =================================================
    # METRICS
    # =================================================

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

    # =================================================
    # TABS
    # =================================================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Rankings",
        "🧠 Narrative",
        "⚠️ Conflicts",
        "❓ Questions",
        "📈 Charts",
        "📋 Full Report"
    ])

    # =================================================
    # TAB 1
    # =================================================

    with tab1:

        st.subheader("Ranked Results")

        st.dataframe(
            ranked_results,
            use_container_width=True
        )

    # =================================================
    # TAB 2
    # =================================================

    with tab2:

        st.subheader("Narrative Intelligence")

        st.write(results["narrative"])

    # =================================================
    # TAB 3
    # =================================================

    with tab3:

        st.subheader("Detected Tradeoffs")

        if len(results["conflicts"]) == 0:

            st.success(
                "No major conflicts detected."
            )

        else:

            for conflict in results["conflicts"]:

                st.warning(conflict)

    # =================================================
    # TAB 4
    # =================================================

    with tab4:

        st.subheader("Clarification Questions")

        for question in results["questions"]:

            st.info(question)

    # =================================================
    # TAB 5
    # =================================================

    with tab5:

        st.subheader("Final Scores")

        fig, ax = plt.subplots(figsize=(8, 5))

        ax.bar(
            ranked_results["name"],
            ranked_results["final_score"]
        )

        ax.set_ylabel("Final Score")

        ax.set_title("Option Rankings")

        st.pyplot(fig)

        plt.close(fig)

    # =================================================
    # TAB 6
    # =================================================

    with tab6:

        st.subheader("Full Explainability Report")

        st.text(results["report"])

else:

    st.info(
        "Configure your decision scenario and run the analysis."
    )
