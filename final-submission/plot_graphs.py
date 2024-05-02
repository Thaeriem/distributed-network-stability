import matplotlib.pyplot as plt

# Data for each graph
graph_data = {
    "Graph 4 100%": {"nodes": 10876, "edges": 39994, "scc": 6560, "random_nodes": 214, "high_deg_nodes": 23, "betweeness_nodes": 17, "avg_nhbr_nodes": 697, "failure_random": 119.0, "failure_high_deg": 139.3, "failure_betweeness": 158.0, "failure_avg_nhbr": 124.0},
    "Graph 4 70%": {"nodes": 7596, "edges": 24069, "scc": 3280, "random_nodes": 164, "high_deg_nodes": 17, "betweeness_nodes": 43, "avg_nhbr_nodes": 805, "failure_random": 178.5, "failure_high_deg": 167.9, "failure_betweeness": 71.0, "failure_avg_nhbr": 264.0},
    "Graph 4 60%": {"nodes": 6502, "edges": 21734, "scc": 2186, "random_nodes": 157, "high_deg_nodes": 17, "betweeness_nodes": 50, "avg_nhbr_nodes": 600, "failure_random": 207.4, "failure_high_deg": 173.9, "failure_betweeness": 70.0, "failure_avg_nhbr": 262.0},
    "Graph 4 55%": {"nodes": 5956, "edges": 20896, "scc": 1640, "random_nodes": 198, "high_deg_nodes": 17, "betweeness_nodes": 47, "avg_nhbr_nodes": 602, "failure_random": 163.7, "failure_high_deg": 174.7, "failure_betweeness": 59.0, "failure_avg_nhbr": 262.0},
    "Graph 5 100%": {"nodes": 8846, "edges": 31839, "scc": 5613, "random_nodes": 143, "high_deg_nodes": 42, "betweeness_nodes": 3, "avg_nhbr_nodes": 256, "failure_random": 145.2, "failure_high_deg": 115.4, "failure_betweeness": 47.0, "failure_avg_nhbr": 129.0},
    "Graph 5 68%": {"nodes": 6039, "edges": 18408, "scc": 2806, "random_nodes": 128, "high_deg_nodes": 50, "betweeness_nodes": 106, "avg_nhbr_nodes": 232, "failure_random": 132.8, "failure_high_deg": 143.3, "failure_betweeness": 31.0, "failure_avg_nhbr": 115.0},
    "Graph 5 58%": {"nodes": 5104, "edges": 16313, "scc": 1871, "random_nodes": 184, "high_deg_nodes": 47, "betweeness_nodes": 91, "avg_nhbr_nodes": 233, "failure_random": 162.2, "failure_high_deg": 237.8, "failure_betweeness": 215.0, "failure_avg_nhbr": 321.0},
    "Graph 5 52%": {"nodes": 4636, "edges": 15546, "scc": 1403, "random_nodes": 156, "high_deg_nodes": 47, "betweeness_nodes": 86, "avg_nhbr_nodes": 133, "failure_random": 117.4, "failure_high_deg": 237.3, "failure_betweeness": 139.0, "failure_avg_nhbr": 321.0},
    "Graph 6 100%": {"nodes": 8717, "edges": 31525, "scc": 5492, "random_nodes": 222, "high_deg_nodes": 53, "betweeness_nodes": 56, "avg_nhbr_nodes": 262, "failure_random": 118.5, "failure_high_deg": 102.4, "failure_betweeness": 173.0, "failure_avg_nhbr": 60.0},
    "Graph 6 68%": {"nodes": 5971, "edges": 18408, "scc": 2746, "random_nodes": 144, "high_deg_nodes": 47, "betweeness_nodes": 74, "avg_nhbr_nodes": 263, "failure_random": 91.6, "failure_high_deg": 98.7, "failure_betweeness": 60.0, "failure_avg_nhbr": 60.0},
    "Graph 6 58%": {"nodes": 5055, "edges": 16383, "scc": 1830, "random_nodes": 142, "high_deg_nodes": 46, "betweeness_nodes": 81, "avg_nhbr_nodes": 258, "failure_random": 134.2, "failure_high_deg": 134.7, "failure_betweeness": 109.0, "failure_avg_nhbr": 100.0},
    "Graph 6 53%": {"nodes": 4598, "edges": 15557, "scc": 1373, "random_nodes": 184, "high_deg_nodes": 46, "betweeness_nodes": 79, "avg_nhbr_nodes": 428, "failure_random": 139.6, "failure_high_deg": 167.2, "failure_betweeness": 121.0, "failure_avg_nhbr": 60.0}
}

# Calculate repair types
for graph, data in graph_data.items():
    data["repair_random"] = data["failure_random"] + data["failure_avg_nhbr"]
    data["repair_high_deg"] = data["failure_high_deg"] + \
        data["failure_avg_nhbr"]
    data["repair_betweeness"] = data["failure_betweeness"] + \
        data["failure_avg_nhbr"]

# Metrics for nodes part
node_metrics = ["random_nodes", "high_deg_nodes",
                "betweeness_nodes", "avg_nhbr_nodes"]

# Metrics for failure part
failure_metrics = ["failure_random", "failure_high_deg",
                   "failure_betweeness", "failure_avg_nhbr"]

# Metrics for repair part
repair_metrics = ["repair_random", "repair_high_deg",
                  "repair_betweeness"]

# Plotting nodes part
plt.figure(figsize=(12, 16))
plt.subplot(3, 1, 1)

for metric in node_metrics:
    plt.plot(graph_data.keys(), [data[metric]
             for data in graph_data.values()], label=metric)

plt.ylabel("Value")
plt.title("Nodes Robustness Comparison for Different Graphs")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45, ha='right')

# Plotting failure part
plt.subplot(3, 1, 2)

for metric in failure_metrics:
    plt.plot(graph_data.keys(), [data[metric]
             for data in graph_data.values()], label=metric)

plt.ylabel("Value")
plt.title("Sequential Failure Metrics Comparison for Different Graphs")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45, ha='right')

# Plotting repair part
plt.subplot(3, 1, 3)

for metric in repair_metrics:
    plt.plot(graph_data.keys(), [data[metric]
             for data in graph_data.values()], label=metric)
plt.xlabel("Graph")
plt.ylabel("Value")
plt.title("Repair Metrics Comparison for Different Graphs")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()
