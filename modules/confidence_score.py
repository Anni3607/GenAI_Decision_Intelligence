
def estimate_decision_confidence(context):

    score = 1.0

    priorities = context.get(
        "priorities",
        {}
    )

    conflicts = context.get(
        "decision_conflicts",
        []
    )

    burnout = context.get(
        "burnout_sensitivity",
        ""
    )

    # =====================================
    # FEW PRIORITIES
    # =====================================

    if len(priorities) < 3:

        score -= 0.2

    # =====================================
    # MANY CONFLICTS
    # =====================================

    if len(conflicts) >= 2:

        score -= 0.25

    # =====================================
    # HIGH BURNOUT SENSITIVITY
    # =====================================

    if burnout == "high":

        score -= 0.1

    # =====================================
    # LIMITS
    # =====================================

    score = max(0.0, min(score, 1.0))

    return round(score, 2)
