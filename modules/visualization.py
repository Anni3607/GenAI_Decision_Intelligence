
import matplotlib.pyplot as plt

def plot_scores(options, scores):

    plt.figure(figsize=(8,5))

    plt.bar(options, scores)

    plt.xlabel("Options")
    plt.ylabel("Scores")
    plt.title("Decision Scores")

    plt.show()
