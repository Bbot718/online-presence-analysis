import matplotlib.pyplot as plt

def plot_social_media_metrics(data, filename="social_media_metrics.png"):
    platforms = list(data.keys())
    metrics = {}

    # Collect metrics for each platform
    for platform, details in data.items():
        if "Error" not in details:  # Skip platforms with errors
            for metric, value in details.items():
                if isinstance(value, (int, float)):  # Only numerical data
                    metrics.setdefault(metric, []).append(value)

    x = range(len(platforms))
    for i, (metric, values) in enumerate(metrics.items()):
        plt.bar([p + i * 0.2 for p in x], values, width=0.2, label=metric)

    plt.xticks([p + 0.2 * (len(metrics) - 1) / 2 for p in x], platforms)
    plt.title("Social Media Metrics")
    plt.xlabel("Platforms")
    plt.ylabel("Values")
    plt.legend(title="Metrics")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename