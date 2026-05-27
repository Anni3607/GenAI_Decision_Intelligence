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

# =====================================================
# DOMAIN
# =====================================================

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
# MAIN ANALYSIS
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

    with st.spinner(
        "Evaluating options..."
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
    # MAIN PIPELINE
    # =================================================

    with st.spinner(
        "Generating analysis..."
    ):

        results = run_decision_analysis(
            user_input=user_input,
            options=options_df,
            criteria=criteria,
            weights=weights
        )

    ranked_results = results["ranked_results"]

    # =================================================
# CONFIDENCE %
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

# =================================================
# CLAMPING
# =================================================

confidence_percent = min(
    95,
    max(
        55,
        confidence_percent
    )
)

    # =================================================
    # METRICS
    # =================================================

    top_option = ranked_results.iloc[0]["name"]

    st.markdown("---")

    col1, col2 = st.columns(2)

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
    # TABS
    # =================================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "Rankings",
        "AI Evaluation",
        "Narrative",
        "Visuals"
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
            "AI Generated Evaluation"
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
            "Strategic Narrative"
        )

        st.write(
            results["narrative"]
        )

    # =================================================
    # TAB 4
    # =================================================

    with tab4:

        # =============================================
        # VISUAL 1
        # =============================================

        st.subheader(
            "Final Decision Scores"
        )

        fig1, ax1 = plt.subplots(
            figsize=(5, 3)
        )

        ax1.bar(
            ranked_results["name"],
            ranked_results["final_score"]
        )

        ax1.set_ylabel(
            "Weighted Score"
        )

        st.pyplot(
            fig1,
            use_container_width=False
        )

        plt.close(fig1)

        # =============================================
        # VISUAL 2
        # =============================================

        st.subheader(
            "Criteria Radar Comparison"
        )

        labels = criteria

        num_vars = len(labels)

        angles = np.linspace(
            0,
            2 * np.pi,
            num_vars,
            endpoint=False
        ).tolist()

        angles += angles[:1]

        fig2, ax2 = plt.subplots(
            figsize=(4.5, 4.5),
            subplot_kw=dict(polar=True)
        )

        for _, row in options_df.iterrows():

            values = [
                row[c]
                for c in criteria
            ]

            values += values[:1]

            ax2.plot(
                angles,
                values,
                linewidth=2,
                label=row["name"]
            )

            ax2.fill(
                angles,
                values,
                alpha=0.1
            )

        ax2.set_xticks(
            angles[:-1]
        )

        ax2.set_xticklabels(
            labels
        )

        ax2.legend(
            loc="upper right"
        )

        st.pyplot(
            fig2,
            use_container_width=False
        )

        plt.close(fig2)

        # =============================================
        # VISUAL 3
        # =============================================

        st.subheader(
            "User Priority Weights"
        )

        weight_df = pd.DataFrame({
            "criterion": criteria,
            "weight": [
                weights[c]
                for c in criteria
            ]
        })

        fig3, ax3 = plt.subplots(
            figsize=(5, 3)
        )

        ax3.barh(
            weight_df["criterion"],
            weight_df["weight"]
        )

        st.pyplot(
            fig3,
            use_container_width=False
        )

        plt.close(fig3)

        # =============================================
        # VISUAL 4
        # =============================================

        st.subheader(
            "Criteria Heatmap"
        )

        heatmap_df = options_df.set_index(
            "name"
        )

        fig4, ax4 = plt.subplots(
            figsize=(6, 2.5)
        )

        im = ax4.imshow(
            heatmap_df.values,
            aspect="auto"
        )

        ax4.set_xticks(
            np.arange(len(criteria))
        )

        ax4.set_xticklabels(
            criteria,
            rotation=45
        )

        ax4.set_yticks(
            np.arange(len(heatmap_df.index))
        )

        ax4.set_yticklabels(
            heatmap_df.index
        )

        plt.colorbar(im)

        st.pyplot(
            fig4,
            use_container_width=False
        )

        plt.close(fig4)

else:

    st.info(
        "Configure your decision scenario to begin analysis."
    )
