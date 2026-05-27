import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from modules.master_pipeline import run_decision_analysis
from modules.domain_criteria import DOMAIN_CRITERIA
from modules.option_evaluator import evaluate_options

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GenAI Decision Intelligence",
    layout="wide",
    page_icon="🧠"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f172a;
        color: white;
    }

    .main {
        background-color: #0f172a;
        color: white;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .glass-box {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.title("🧠 GenAI Decision Intelligence")

st.markdown(
    """
AI-powered multi-domain decision analysis platform for:

- Career Decisions
- Education Choices
- Investment Analysis
- Tech Product Comparisons
- Food & Lifestyle Decisions
- Fitness Strategy Evaluation

The system automatically evaluates options using AI,
applies your personal priorities,
detects tradeoffs,
and generates explainable strategic reasoning.
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

st.sidebar.markdown("---")

user_input = st.sidebar.text_area(
    "Describe your priorities and goals:",
    height=180,
    placeholder="Example: I care most about battery life, long-term reliability, and overall value."
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
# CRITERIA WEIGHTS
# =====================================================

st.sidebar.markdown("---")

st.sidebar.subheader("🎯 Criteria Importance")

st.sidebar.caption(
    "Adjust how important each factor is to YOU."
)

weights = {}

for criterion in criteria:

    weights[criterion] = st.sidebar.slider(
        criterion.replace("_", " ").title(),
        1,
        10,
        5
    )

# =====================================================
# INFO SECTION
# =====================================================

st.markdown("## 🧩 Current Evaluation Criteria")

criteria_cols = st.columns(len(criteria))

for idx, criterion in enumerate(criteria):

    with criteria_cols[idx]:

        st.markdown(
            f"""
<div class="glass-box">
<b>{criterion.replace("_", " ").title()}</b>
</div>
""",
            unsafe_allow_html=True
        )

# =====================================================
# RUN ANALYSIS
# =====================================================

if st.button("🚀 Run Decision Analysis"):

    valid_options = [

        option
        for option in option_names
        if option.strip() != ""
    ]

    if len(valid_options) < 2:

        st.error(
            "Please enter at least 2 options."
        )

        st.stop()

    if not user_input.strip():

        st.error(
            "Please describe your priorities."
        )

        st.stop()

    # =================================================
    # AI OPTION EVALUATION
    # =================================================

    with st.spinner(
        "🤖 AI is evaluating options..."
    ):

        evaluated_scores = evaluate_options(
            domain=domain,
            options=valid_options,
            criteria=criteria
        )

    option_data = []

    for option_name, scores in evaluated_scores.items():

        row = {
            "name": option_name
        }

        for criterion in criteria:

            row[criterion] = scores.get(
                criterion,
                5
            )

        option_data.append(row)

    options_df = pd.DataFrame(
        option_data
    )

    # =================================================
    # MAIN ANALYSIS
    # =================================================

    with st.spinner(
        "🧠 Running strategic reasoning engine..."
    ):

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

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🏆 Recommended",
            top_option
        )

    with col2:
        st.metric(
            "📊 Confidence",
            confidence
        )

    with col3:
        st.metric(
            "⚠️ Conflicts",
            conflicts
        )

    with col4:
        st.metric(
            "❓ Questions",
            questions
        )

    # =================================================
    # TABS
    # =================================================

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Rankings",
        "🤖 AI Evaluation",
        "🧠 Narrative",
        "⚠️ Tradeoffs",
        "📈 Visuals",
        "📋 Report"
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

        st.subheader(
            "AI-Generated Option Evaluation"
        )

        st.dataframe(
            options_df,
            use_container_width=True
        )

    # =================================================
    # TAB 3
    # =================================================

    with tab3:

        st.subheader(
            "Narrative Intelligence"
        )

        st.write(
            results["narrative"]
        )

    # =================================================
    # TAB 4
    # =================================================

    with tab4:

        st.subheader(
            "Detected Tradeoffs"
        )

        if len(results["conflicts"]) == 0:

            st.success(
                "No major tradeoffs detected."
            )

        else:

            for conflict in results["conflicts"]:

                st.warning(conflict)

    # =================================================
    # TAB 5
    # =================================================

    with tab5:

        st.subheader(
            "Final Decision Scores"
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.bar(
            ranked_results["name"],
            ranked_results["final_score"]
        )

        ax.set_ylabel(
            "Weighted Score"
        )

        ax.set_title(
            "AI Decision Rankings"
        )

        st.pyplot(fig)

        plt.close(fig)

    # =================================================
    # TAB 6
    # =================================================

    with tab6:

        st.subheader(
            "Full Explainability Report"
        )

        st.text(
            results["report"]
        )

else:

    st.info(
        "Configure your decision scenario and run the analysis."
    )
