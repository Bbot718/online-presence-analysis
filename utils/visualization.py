import pandas as pd
import matplotlib.pyplot as plt

def plot_comparison_chart(data, filename="comparison_chart.png"):
    """
    Creates a bar chart for competitor comparison.

    Parameters:
        data (dict): Comparison data structured as {metric: {url: value}}.
        filename (str): File path to save the chart image.

    Returns:
        str: Path to the saved chart image.
    """
    df = pd.DataFrame(data).T  # Convert to DataFrame for easier plotting
    df.plot(kind="bar")
    plt.title("Competitor Comparison")
    plt.xlabel("Metrics")
    plt.ylabel("Scores")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename
