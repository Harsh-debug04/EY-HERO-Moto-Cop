import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os

def generate_sensor_anomaly_chart(output_path):
    # Simulate data: Normal operation then a spike
    time_steps = np.arange(0, 60, 1)  # 60 minutes
    temp_data = np.random.normal(loc=90, scale=2, size=60)  # Normal temp ~90C

    # Introduce anomaly at minute 45
    temp_data[45:] = temp_data[45:] + np.linspace(0, 30, 15) # Spike to ~120C

    plt.figure(figsize=(10, 6))
    plt.plot(time_steps, temp_data, label='Engine Temperature (°C)', color='blue', linewidth=2)

    # Highlight anomaly zone
    plt.axvspan(45, 60, color='red', alpha=0.2, label='Anomaly Detected')
    plt.axhline(y=110, color='red', linestyle='--', label='Critical Threshold (110°C)')

    plt.title('Real-Time Sensor Telematics: Engine Overheat Event', fontsize=14)
    plt.xlabel('Time (Minutes)', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated {output_path}")

def generate_knowledge_graph(output_path):
    G = nx.DiGraph()

    # Define Nodes
    nodes = [
        ("DTC_P0300", {"label": "DTC P0300\n(Code)", "color": "#FFCDD2"}), # Red-ish
        ("Misfire", {"label": "Cylinder Misfire\n(Symptom)", "color": "#FFF9C4"}), # Yellow-ish
        ("SparkPlug", {"label": "Bad Spark Plug\n(Component)", "color": "#BBDEFB"}), # Blue-ish
        ("SupplierX", {"label": "Supplier Batch #992\n(Root Cause)", "color": "#C8E6C9"}), # Green-ish
        ("Recall", {"label": "Recall Action\n(Outcome)", "color": "#E1BEE7"})  # Purple-ish
    ]

    for node_id, attrs in nodes:
        G.add_node(node_id, label=attrs["label"], color=attrs["color"])

    # Define Edges
    edges = [
        ("DTC_P0300", "Misfire", "Indicates"),
        ("Misfire", "SparkPlug", "Caused By"),
        ("SparkPlug", "SupplierX", "Sourced From"),
        ("SupplierX", "Recall", "Triggers")
    ]

    for u, v, label in edges:
        G.add_edge(u, v, label=label)

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G, seed=42)

    # Draw Nodes
    node_colors = [G.nodes[n]["color"] for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=node_colors, edgecolors="black")

    # Draw Labels
    labels = {n: G.nodes[n]["label"] for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")

    # Draw Edges
    nx.draw_networkx_edges(G, pos, width=2, arrowsize=20)
    edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title('Manufacturing Agent: Root Cause Analysis (Knowledge Graph)', fontsize=14)
    plt.axis("off")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Generated {output_path}")

if __name__ == "__main__":
    output_dir = "visual_assets"
    os.makedirs(output_dir, exist_ok=True)

    generate_sensor_anomaly_chart(os.path.join(output_dir, "data_anomaly_chart.png"))
    generate_knowledge_graph(os.path.join(output_dir, "data_knowledge_graph.png"))
