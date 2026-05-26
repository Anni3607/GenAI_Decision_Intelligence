
def generate_fact_summary(
    ranked_results
):

    best = ranked_results.iloc[0]

    summary = {}

    # =====================================
    # SCORE MAPPING
    # =====================================

    def score_label(value):

        if value >= 0.8:
            return "Very High"

        elif value >= 0.6:
            return "High"

        elif value >= 0.4:
            return "Moderate"

        elif value >= 0.2:
            return "Low"

        return "Very Low"

    # =====================================
    # BUILD FACT SUMMARY
    # =====================================

    for column in ranked_results.columns:

        if column not in [
            "name",
            "final_score"
        ]:

            summary[column] = score_label(
                best[column]
            )

    return summary
