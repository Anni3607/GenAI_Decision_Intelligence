
def detect_hallucination_risk(
    narrative
):

    risky_patterns = [

        "low stress",

        "very flexible",

        "zero stress",

        "perfect fit"
    ]

    detected = []

    lower_text = narrative.lower()

    for pattern in risky_patterns:

        if pattern in lower_text:

            detected.append(
                pattern
            )

    return detected
