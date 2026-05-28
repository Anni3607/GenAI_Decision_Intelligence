import pandas as pd

print("MASTER PIPELINE VERSION = FINAL_V5")

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

from modules.domain_cost_criteria import (
    DOMAIN_COST_CRITERIA
)

# =====================================================
# DYNAMIC WEIGHTED SCORING ENGINE
# =====================================================

def score_options(
    options,
    criteria,
    weights,
    domain
):

    scored_df = options.copy()

    final_scores = []

    cost_criteria = DOMAIN_COST_CRITERIA.get(
        domain,
        []
    )

    for _, row in scored_df.iterrows():

        total_score = 0

        for criterion in criteria:

            try:

                criterion_value = float(
                    row.get(criterion, 5)
                )

                criterion_weight = float(
                    weights.get(criterion, 5)
                )

                # =====================================
                # COST CRITERIA INVERSION
                # =====================================

                if criterion in cost_criteria:

                    adjusted_score = (
                        11 - criterion_value
                    )

                else:

                    adjusted_score = (
                        criterion_value
                    )

                weighted_score = (
                    adjusted_score
                    * criterion_weight
                )

                total_score += weighted_score

            except Exception:

                total_score += 0

        final_scores.append(
            round(total_score, 2)
        )

    scored_df["final_score"] = final_scores

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
# MAIN DECISION PIPELINE
# =====================================================

def run_decision_analysis(
    user_input,
    options,
    criteria,
    weights,
    domain
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
            options=options,
            criteria=criteria,
            weights=weights,
            domain=domain
        )

        # =============================================
        # CONFLICT ANALYSIS
        # =============================================

        conflicts = analyze_conflicts(
            context
        )

        # =============================================
        # CONFIDENCE SCORING
        # =============================================

        confidence = calculate_confidence_score(
            ranked_results,
            conflicts
        )

        # =============================================
        # ADAPTIVE QUESTIONS
        # =============================================

        questions = []

        if len(conflicts) > 0:

            questions.append(
                "Which criteria matter most when tradeoffs occur?"
            )

        # =============================================
        # NARRATIVE GENERATION
        # =============================================

        narrative = generate_intelligent_narrative(
            user_input=user_input,
            ranked_results=ranked_results,
            conflicts=conflicts,
            confidence=confidence
        )

        # =============================================
        # REPORT GENERATION
        # =============================================

        top_option = ranked_results.iloc[0]["name"]

        report = f"""
==================================================
GENAI DECISION INTELLIGENCE REPORT
==================================================

Recommended Option:
{top_option}

Confidence Level:
{confidence}

Detected Tradeoffs:
{conflicts}

Applied Criteria:
{criteria}

User Weights:
{weights}

AI Narrative:
{narrative}
"""

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

        error_message = str(e)

        print(
            f"PIPELINE ERROR: {error_message}"
        )

        log_error(
            error_message
        )

        return {

            "ranked_results": pd.DataFrame(),

            "confidence": 0,

            "conflicts": [],

            "questions": [],

            "narrative": f"Pipeline failed: {error_message}",

            "report": error_message
        }
