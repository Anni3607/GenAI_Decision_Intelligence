
def map_priorities_to_weights(priorities):

    # =====================================
    # TEXT PRIORITY MAPPING
    # =====================================

    text_mapping = {
        "very high": 1.0,
        "high": 0.8,
        "medium": 0.5,
        "low": 0.3,
        "very low": 0.1
    }

    raw_weights = {}

    # =====================================
    # HANDLE BOTH:
    # - text priorities
    # - numeric priorities
    # =====================================

    for criterion, importance in priorities.items():

        # CASE 1: STRING
        if isinstance(importance, str):

            raw_weights[criterion] = text_mapping.get(
                importance.lower(),
                0.5
            )

        # CASE 2: NUMBER
        elif isinstance(importance, (int, float)):

            raw_weights[criterion] = float(importance)

        # FALLBACK
        else:

            raw_weights[criterion] = 0.5

    # =====================================
    # NORMALIZE
    # =====================================

    total = sum(raw_weights.values())

    normalized_weights = {}

    for criterion, value in raw_weights.items():

        normalized_weights[criterion] = round(
            value / total,
            4
        )

    return normalized_weights
