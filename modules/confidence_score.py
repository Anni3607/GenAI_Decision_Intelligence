# =====================================================
# CONFIDENCE ENGINE
# =====================================================

def analyze_conflicts(context):

    conflicts = []

    priorities = [
        str(p).lower()
        for p in context.get(
            "priorities",
            []
        )
    ]

    concerns = [
        str(c).lower()
        for c in context.get(
            "concerns",
            []
        )
    ]

    goals = [
        str(g).lower()
        for g in context.get(
            "goals",
            []
        )
    ]

    # =================================================
    # TRADEOFF DETECTION
    # =================================================

    if (
        "high salary" in priorities
        and "low stress" in priorities
    ):

        conflicts.append(
            "High salary and low stress may conflict in many industries."
        )

    if (
        "career growth" in priorities
        and "work-life balance" in priorities
    ):

        conflicts.append(
            "Fast career growth may reduce work-life balance."
        )

    if (
        "flexibility" in priorities
        and "stability" in priorities
    ):

        conflicts.append(
            "Highly flexible roles may provide less stability."
        )

    if (
        "startup" in goals
        and "low risk" in concerns
    ):

        conflicts.append(
            "Startup environments usually involve higher uncertainty."
        )

    return conflicts

# =====================================================
# CONFIDENCE SCORE
# =====================================================

def calculate_confidence_score(
    ranked_results,
    conflicts
):

    if ranked_results.empty:
        return "Low"

    if len(ranked_results) < 2:
        return "Medium"

    top_score = ranked_results.iloc[0][
        "final_score"
    ]

    second_score = ranked_results.iloc[1][
        "final_score"
    ]

    score_gap = top_score - second_score

    # =================================================
    # BASE CONFIDENCE
    # =================================================

    if score_gap >= 20:

        confidence = "High"

    elif score_gap >= 10:

        confidence = "Medium"

    else:

        confidence = "Low"

    # =================================================
    # CONFLICT ADJUSTMENT
    # =================================================

    if len(conflicts) >= 3:

        confidence = "Low"

    elif (
        len(conflicts) >= 1
        and confidence == "High"
    ):

        confidence = "Medium"

    return confidence
