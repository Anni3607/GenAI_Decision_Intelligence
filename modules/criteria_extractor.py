
def extract_criteria(user_input):

    keywords = [
        "salary",
        "growth",
        "work-life balance",
        "flexibility",
        "learning",
        "location"
    ]

    found = []

    text = user_input.lower()

    for k in keywords:
        if k in text:
            found.append(k)

    return found
