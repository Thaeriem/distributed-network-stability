import matplotlib.pyplot as plt

# Data for each graph
graph_data = {
    "Graph 4 100%": {"nodes": 10876, "edges": 39994, "scc": 6560, "random_nodes": 157, "high_deg_nodes": 23, "betweeness_nodes": 17, "avg_nhbr_nodes": 697, "failure_random": 126.7, "failure_high_deg": 139.3, "failure_betweeness": 158.0, "failure_avg_nhbr": 124.0},
    "Graph 4 70%": {"nodes": 7596, "edges": 24069, "scc": 3280, "random_nodes": 108, "high_deg_nodes": 17, "betweeness_nodes": 43, "avg_nhbr_nodes": 805, "failure_random": 174.6, "failure_high_deg": 167.9, "failure_betweeness": 71.0, "failure_avg_nhbr": 264.0},
    "Graph 4 60%": {"nodes": 6502, "edges": 21734, "scc": 2186, "random_nodes": 143, "high_deg_nodes": 17, "betweeness_nodes": 50, "avg_nhbr_nodes": 600, "failure_random": 171.6, "failure_high_deg": 173.9, "failure_betweeness": 70.0, "failure_avg_nhbr": 262.0},
    "Graph 4 55%": {"nodes": 5956, "edges": 20896, "scc": 1640, "random_nodes": 217, "high_deg_nodes": 17, "betweeness_nodes": 47, "avg_nhbr_nodes": 602, "failure_random": 155.0, "failure_high_deg": 174.7, "failure_betweeness": 59.0, "failure_avg_nhbr": 262.0}
}

# Metrics for nodes part
node_metrics = ["random_nodes", "high_deg_nodes",
                "betweeness_nodes", "avg_nhbr_nodes"]

# Metrics for failure part
failure_metrics = ["failure_random", "failure_high_deg",
                   "failure_betweeness", "failure_avg_nhbr"]

# Plotting nodes part
plt.figure(figsize=(12, 16))
plt.subplot(2, 1, 1)

for metric in node_metrics:
    plt.plot(graph_data.keys(), [data[metric]
             for data in graph_data.values()], label=metric)

plt.ylabel("Value")
plt.title("Nodes Robustness Comparison for Different Graphs")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45, ha='right')

# Plotting failure part
plt.subplot(2, 1, 2)

for metric in failure_metrics:
    plt.plot(graph_data.keys(), [data[metric]
             for data in graph_data.values()], label=metric)

plt.xlabel("Graph")
plt.ylabel("Value")
plt.title("Sequential Failure Metrics Comparison for Different Graphs")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()
