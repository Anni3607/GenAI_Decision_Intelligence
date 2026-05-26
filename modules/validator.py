
VALID_PRIORITIES = [

    "salary",
    "career_growth",
    "flexibility",
    "stress",
    "stability",
    "work_life_balance"
]


# ==========================================
# NORMALIZE PRIORITY VALUE
# ==========================================

def normalize_priority_value(value):

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

    elif isinstance(value, (int, float)):

        return max(
            0,
            min(value, 10)
        )

    return 5


# ==========================================
# VALIDATE CONTEXT
# ==========================================

def validate_context(context):

    validated = {}

    priorities = context.get(
        "priorities",
        {}
    )

    validated_priorities = {}

    for key, value in priorities.items():

        if key in VALID_PRIORITIES:

            validated_priorities[key] = (
                normalize_priority_value(value)
            )

    validated["priorities"] = (
        validated_priorities
    )

    # ======================================
    # SAFE STRINGS
    # ======================================

    validated["risk_tolerance"] = str(
        context.get(
            "risk_tolerance",
            "medium"
        )
    ).lower()

    validated["burnout_sensitivity"] = str(
        context.get(
            "burnout_sensitivity",
            "medium"
        )
    ).lower()

    # ======================================
    # SAFE LISTS
    # ======================================

    validated["hidden_priorities"] = list(
        context.get(
            "hidden_priorities",
            []
        )
    )

    validated["concerns"] = list(
        context.get(
            "concerns",
            []
        )
    )

    validated["goals"] = list(
        context.get(
            "goals",
            []
        )
    )

    return validated
