import pandas as pd

from modules.system_logger import (
    log_event,
    log_error
)

from modules.ai_reasoning import (
    extract_decision_context
)

from modules.narrative_engine import (
    generate_intelligent_narrative
)

from modules.confidence_engine import (
    analyze_conflicts,
    calculate_confidence_score
)

# =====================================================
# SIMPLE SCORING ENGINE
# =====================================================

def score_options(
    options,
    benefit_criteria,
    cost_criteria
):

    scored_df = options.copy()

    scored_df["benefit_score"] = scored_df[
        benefit_criteria
    ].sum(axis=1)

    scored_df["cost_score"] = scored_df[
        cost_criteria
    ].sum(axis=1)

    scored_df["final_score"] = (
        scored_df["benefit_score"]
        - scored_df["cost_score"]
    )

    scored_df = scored_df.sort_values(
        by="final_score",
        ascending=False
    )

    scored_df.reset_index(
        drop=True,
        inplace=True
    )

    return scored_df

# =====================================================
# MAIN PIPELINE
# =====================================================

def run_decision_analysis(
    user_input,
    options,
    benefit_criteria,
    cost_criteria
):

    try:

        log_event(
            "Decision analysis started."
        )

        # =============================================
        # CONTEXT EXTRACTION
        # =============================================

        context = extract_decision_context(
            user_input
        )

        # =============================================
        # OPTION SCORING
        # =============================================

        ranked_results = score_options(
            options,
            benefit_criteria,
            cost_criteria
        )

        # =============================================
        # CONFLICT ANALYSIS
        # =============================================

        conflicts = analyze_conflicts(
            context
        )

        # =============================================
        # CONFIDENCE SCORE
        # =============================================

        confidence = calculate_confidence_score(
            ranked_results,
            conflicts
        )

        # =============================================
        # QUESTIONS
        # =============================================

        questions = []

        if len(conflicts) > 0:

            questions.append(
                "Which factor matters more when tradeoffs occur?"
            )

        if confidence == "Low":

            questions.append(
                "Can you provide more detailed priorities?"
            )

        # =============================================
        # NARRATIVE
        # =============================================

        narrative = generate_intelligent_narrative(
            user_input=user_input,
            ranked_results=ranked_results,
            conflicts=conflicts,
            confidence=confidence
        )

        # =============================================
        # REPORT
        # =============================================

        report = f'''
==============================
GENAI DECISION REPORT
==============================

Recommended Option:
{ranked_results.iloc[0]["name"]}

Confidence:
{confidence}

Conflicts:
{conflicts}

Narrative:
{narrative}
'''

        log_event(
            "Decision analysis completed."
        )

        return {

            "ranked_results": ranked_results,

            "confidence": confidence,

            "conflicts": conflicts,

            "questions": questions,

            "narrative": narrative,

            "report": report
        }

    except Exception as e:

        log_error(str(e))

        return {

            "ranked_results": pd.DataFrame(),

            "confidence": "Low",

            "conflicts": [],

            "questions": [],

            "narrative": f"Pipeline failed: {str(e)}",

            "report": str(e)
        }
