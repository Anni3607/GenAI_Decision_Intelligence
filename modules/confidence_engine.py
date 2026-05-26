
def calculate_confidence(

    context,
    conflicts,
    questions,
    user_input
):

    confidence = 1.0

    # =====================================
    # INPUT LENGTH
    # =====================================

    word_count = len(
        user_input.split()
    )

    if word_count < 10:

        confidence -= 0.25

    elif word_count < 20:

        confidence -= 0.15


    # =====================================
    # PRIORITY RICHNESS
    # =====================================

    priorities = context.get(
        "priorities",
        {}
    )

    num_priorities = len(
        priorities
    )

    if num_priorities <= 1:

        confidence -= 0.25

    elif num_priorities <= 2:

        confidence -= 0.15


    # =====================================
    # CONFLICT PENALTY
    # =====================================

    num_conflicts = len(
        conflicts
    )

    confidence -= (
        num_conflicts * 0.08
    )


    # =====================================
    # TOO MANY QUESTIONS
    # =====================================

    if len(questions) >= 4:

        confidence -= 0.10


    # =====================================
    # EMPTY STYLE INPUTS
    # =====================================

    weak_patterns = [

        "...",
        "idk",
        "anything",
        "good career"
    ]

    lower_input = user_input.lower()

    for pattern in weak_patterns:

        if pattern in lower_input:

            confidence -= 0.25


    # =====================================
    # CLAMP
    # =====================================

    confidence = max(
        0.1,
        min(confidence, 0.95)
    )

    return round(
        confidence,
        2
    )
