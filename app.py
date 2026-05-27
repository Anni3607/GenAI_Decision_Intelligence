import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from modules.master_pipeline import run_decision_analysis
from modules.domain_criteria import DOMAIN_CRITERIA
from modules.option_evaluator import evaluate_options

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

    .stApp {
        background-color: #0f172a;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    h1, h2, h3 {
        color: #f8fafc;
        font-weight: 600;
    }

    .glass-box {
        background: rgba(255,255,255,0.05);
        padding: 16px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        text-align: center;
        margin-bottom: 12px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# TITLE
# =====================================================

st.title("GenAI Decision Intelligence")

st.caption(
    "AI-assisted multi-criteria decision analysis system."
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Decision Setup")

domain = st.sidebar.selectbox(
    "Domain",
    [
        "Career",
        "Education",
        "Investment",
        "Tech Purchase",
        "Food",
        "Fitness",
        "Fashion"
    ]
)

criteria = DOMAIN_CRITERIA[domain]

# =====================================================
# USER INPUT
# =====================================================

st.sidebar.markdown("---")

user_input = st.sidebar.text_area(
    "Priorities & Goals",
    height=180,
    placeholder="Describe what matters most to you."
)

# =====================================================
# OPTIONS
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
        placeholder="Enter option"
    )

    option_names.append(option)

# =====================================================
# WEIGHTS
# =====================================================

st.sidebar.markdown("---")

st.sidebar.subheader("Criteria Importance")

weights = {}

for criterion in criteria:

    weights[criterion] = st.sidebar.slider(
        criterion.replace("_", " ").title(),
        1,
        10,
        5
    )

# =====================================================
# CRITERIA DISPLAY
# =====================================================

st.markdown("## Evaluation Criteria")

criteria_rows = [
    criteria[i:i+3]
    for i in range(0, len(criteria), 3)
]

for row in criteria_rows:

    cols = st.columns(len(row))

    for idx, criterion in enumerate(row):

        with cols[idx]:

            st.markdown(
                f"""
<div class="glass-box">
{criterion.replace("_", " ").title()}
</div>
""",
                unsafe_allow_html=True
            )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# RUN ANALYSIS
# =====================================================

if st.button("Run Decision Analysis"):

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

    with st.spinner("Evaluating options..."):

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

    with st.spinner("Generating analysis..."):

        results = run_decision_analysis(
            user_input=user_input,
            options=options_df,
            criteria=criteria,
            weights=weights
        )

    ranked_results = results["ranked_results"]

    # =================================================
    # CONFIDENCE
    # =================================================

    score_gap = (
        ranked_results.iloc[0]["final_score"]
        -
        ranked_results.iloc[1]["final_score"]
    )

    confidence_percent = int(
        50 + score_gap
    )

    # =================================================
    # SUBJECTIVE UNCERTAINTY
    # =================================================

    SUBJECTIVE_CRITERIA = [

        "taste",
        "style",
        "comfort",
        "trendiness",
        "design"
    ]

    subjective_penalty = 0

    for criterion in criteria:

        if (
            criterion in SUBJECTIVE_CRITERIA
            and weights[criterion] >= 7
        ):

            subjective_penalty += 4

    confidence_percent -= subjective_penalty

    confidence_percent = min(
        95,
        max(
            55,
            confidence_percent
        )
    )

    # =================================================
    # RESULTS HEADER
    # =================================================

    st.markdown("---")

    col1, col2 = st.columns(2)

    top_option = ranked_results.iloc[0]["name"]

    with col1:

        st.metric(
            "Recommended Option",
            top_option
        )

    with col2:

        st.metric(
            "Confidence",
            f"{confidence_percent}%"
        )

    # =================================================
