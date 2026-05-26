
import pandas as pd

class DecisionEngine:

    def __init__(
        self,
        options,
        weights,
        benefit_criteria,
        cost_criteria
    ):

        self.options = options
        self.weights = weights
        self.benefit_criteria = benefit_criteria
        self.cost_criteria = cost_criteria

    def normalize_benefit(self, series):

        return (
            (series - series.min())
            /
            (series.max() - series.min())
        )

    def normalize_cost(self, series):

        return (
            (series.max() - series)
            /
            (series.max() - series.min())
        )

    def normalize_scores(self):

        df = pd.DataFrame(self.options)

        # BENEFIT CRITERIA
        for criterion in self.benefit_criteria:

            df[criterion] = self.normalize_benefit(
                df[criterion]
            )

        # COST CRITERIA
        for criterion in self.cost_criteria:

            df[criterion] = self.normalize_cost(
                df[criterion]
            )

        return df

    def calculate_weighted_scores(self):

        df = self.normalize_scores()

        final_scores = []

        for _, row in df.iterrows():

            total = 0

            for criterion, weight in self.weights.items():

                total += row[criterion] * weight

            final_scores.append(round(total, 4))

        df["final_score"] = final_scores

        return df

    def rank_options(self):

        df = self.calculate_weighted_scores()

        ranked_df = df.sort_values(
            by="final_score",
            ascending=False
        )

        ranked_df.reset_index(drop=True, inplace=True)

        return ranked_df
