import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample dataset (replace this with reading from a CSV file if needed)
data = {
    "http_status": [
        "SSL Errors", "Status Code: 200", "Connection Errors", "Status Code: 403",
        "Timeout Errors", "Dismatch", "Self signed certificate", "Status Code: 404"
    ],
    "Count": [5522, 2499, 748, 575, 170, 95, 50, 45],
    "Average TTL": [1202, 1121, 1398, 574, 1762, 1898, 2233, 668]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Create pivot table for heatmap
df_pivot = df.pivot(index="http_status", columns="Average TTL", values="Count")

# Set plot size
plt.figure(figsize=(10, 6))

# Create heatmap
sns.heatmap(df_pivot, annot=True, fmt=".0f", cmap="Blues", linewidths=0.5)

# Labels and title
plt.xlabel("Average TTL")
plt.ylabel("HTTP Status / Error Type")
plt.title("Heatmap of HTTP Status/Error Types vs. Average TTL")

# Show plot
plt.show()
