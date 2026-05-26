
def convert_priority(value):

    # =====================================
    # STRING → NUMBER
    # =====================================

    if isinstance(value, str):

        mapping = {
            "very high": 10,
            "high": 8,
            "medium": 5,
            "low": 3,
            "very low": 1
        }

        return mapping.get(
            value.lower(),
            5
        )

    # =====================================
    # NUMBER
    # =====================================

    elif isinstance(value, (int, float)):

        return value

    # =====================================
    # FALLBACK
    # =====================================

    return 5


def generate_adaptive_questions(context):

    questions = []

    priorities = context.get(
        "priorities",
        {}
    )

    risk = context.get(
        "risk_tolerance",
        ""
    ).lower()

    burnout = context.get(
        "burnout_sensitivity",
        ""
    ).lower()

    # =====================================
    # NORMALIZED PRIORITIES
    # =====================================

    salary = convert_priority(
        priorities.get("salary", 0)
    )

    growth = convert_priority(
        priorities.get("career_growth", 0)
    )

    flexibility = convert_priority(
        priorities.get("flexibility", 0)
    )

    # =====================================
    # SALARY VS BALANCE
    # =====================================

    if (
        salary >= 7
        and
        burnout in ["medium", "high"]
    ):

        questions.append(
            "Would you sacrifice some salary for significantly better work-life balance?"
        )

    # =====================================
    # GROWTH VS STABILITY
    # =====================================

    if (
        growth >= 7
        and
        risk == "low"
    ):

        questions.append(
            "Would you prefer slower but more stable career growth?"
        )

    # =====================================
    # FLEXIBILITY CLARIFICATION
    # =====================================

    if flexibility >= 7:

        questions.append(
            "Does flexibility mean remote work, flexible hours, or lower workload for you?"
        )

    # =====================================
    # MISSING STABILITY SIGNAL
    # =====================================

    if "stability" not in priorities:

        questions.append(
            "How important is long-term job stability to you?"
        )

    # =====================================
    # WORK ENVIRONMENT
    # =====================================

    if burnout != "low":

        questions.append(
            "What kind of work environment helps you perform best?"
        )

    return questions
