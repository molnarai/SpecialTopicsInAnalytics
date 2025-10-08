#!/usr/bin/env python
TITLE = r"""
   ____                           _         ____             _       _     
  / ___| ___ _ __   ___ _ __ __ _| |_ ___  / ___|  ___   ___(_) __ _| |    
 | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \ \___ \ / _ \ / __| |/ _` | |    
 | |_| |  __/ | | |  __/ | | (_| | ||  __/  ___) | (_) | (__| | (_| | |    
  \____|\___|_| |_|\___|_|  \__,_|\__\___| |____/ \___/ \___|_|\__,_|_|    
 | \ | | ___| |___      _____  _ __| | __  / ___|_ __ __ _ _ __ | |__  ___ 
 |  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ / | |  _| '__/ _` | '_ \| '_ \/ __|
 | |\  |  __/ |_ \ V  V / (_) | |  |   <  | |_| | | | (_| | |_) | | | \__ \
 |_| \_|\___|\__| \_/\_/ \___/|_|  |_|\_\  \____|_|  \__,_| .__/|_| |_|___/
                                                          |_|              
"""
import pandas as pd
import numpy as np
import networkx as nx
import random
from collections import defaultdict

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

DEFAULT_CATEGORIES_FILE = "social_network_categories.json"
DEFAULT_VERTICES_FILE = "social_network_vertices.csv"
DEFAULT_EDGES_FILE = "social_network_edges.csv"
DEFAULT_NUMBER_OF_VERTICES = 2000

# Define categories for each consumer property
categories = {
    'music': ["R&B", "Hip Hop", "Jazz", "Blues", "Rock"],
    'sports': ["track and field", "football", "baseball", "basketball", "hockey", "soccer", "tennis"],
    'vehicle': ["muscle car", "pickup truck", "SUV", "sedan", "off-road"],
    'food': ["american", "mexican", "thai", "french"],
    'vacation': ["beach", "mountains", "city", "desert"]
}

def generate_consumer_social_network(n_consumers=500, avg_degree=8, preference_correlation=0.3):
    """
    Generate a social network of consumers with categorical preferences.
    
    Parameters:
    - n_consumers: Number of consumer nodes
    - avg_degree: Average number of connections per consumer
    - preference_correlation: Probability that connected consumers share similar preferences
    """
    
    # Generate social network using Barabási-Albert model (realistic social network structure)
    m = avg_degree // 2  # Number of edges to attach from new node
    G = nx.barabasi_albert_graph(n_consumers, m, seed=42)
    
    # Initialize consumer preferences randomly
    consumers = []
    for node_id in range(n_consumers):
        consumer = {
            'id': f'user_{node_id}',
            'music': np.random.choice(categories['music']),
            'sports': np.random.choice(categories['sports']),
            'vehicle': np.random.choice(categories['vehicle']),
            'food': np.random.choice(categories['food']),
            'vacation': np.random.choice(categories['vacation'])
        }
        consumers.append(consumer)
    
    # Add preference correlation - friends are more likely to share preferences
    for edge in G.edges():
        node1, node2 = edge
        
        # For each preference domain, there's a chance friends will influence each other
        for domain in categories.keys():
            if np.random.random() < preference_correlation:
                # Randomly pick one consumer to influence the other
                if np.random.random() < 0.5:
                    consumers[node2][domain] = consumers[node1][domain]
                else:
                    consumers[node1][domain] = consumers[node2][domain]
    
    return G, consumers


def main(args):
    print(TITLE)
    print("Generating social network graph data...")
    print(f"Number of consumers: {args.n_consumers}")
    print(f"Average degree: {args.avg_degree}")
    print(f"Preference correlation: {args.preference_correlation}")
    print(f"Categories file: {args.categories_file}")
    print(f"Vertices file: {args.vertices_file}")
    print(f"Edges file: {args.edges_file}")

    # Generate the dataset
    network, consumer_data = generate_consumer_social_network(n_consumers=args.n_consumers, avg_degree=args.avg_degree, preference_correlation=args.preference_correlation)

    # Create vertices and edges DataFrames for GraphFrames
    vertices_df = pd.DataFrame(consumer_data)
    edges_data = []
    for edge in network.edges():
        edges_data.append({
            'src': f'user_{edge[0]}',
            'dst': f'user_{edge[1]}',
            'relationship': 'friend'
        })
    edges_df = pd.DataFrame(edges_data)

    # Save datasets
    vertices_df.to_csv(args.vertices_file, index=False)
    edges_df.to_csv(args.edges_file, index=False)

    # Save categories
    import json
    with open(args.categories_file, 'w') as f:
        json.dump(categories, f)

    print("Done!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate social network graph data for consumers.")
    parser.add_argument("--n_consumers", type=int, default=DEFAULT_NUMBER_OF_VERTICES, help="Number of consumer nodes")
    parser.add_argument("--avg-degree", type=int, default=8, help="Average number of connections per consumer")
    parser.add_argument("--preference-correlation", type=float, default=0.3, help="Probability that connected consumers share similar preferences")
    parser.add_argument("--categories-file", type=str, default=DEFAULT_CATEGORIES_FILE, help="Output JSON file for categories")
    parser.add_argument("-v", "--vertices-file", type=str, default=DEFAULT_VERTICES_FILE, help="Output CSV file for vertices")
    parser.add_argument("-e", "--edges-file", type=str, default=DEFAULT_EDGES_FILE, help="Output CSV file for edges")

    args = parser.parse_args()
    main(args)

# # Generate the dataset
# network, consumer_data = generate_consumer_social_network(n_consumers=500, avg_degree=8, preference_correlation=0.3)

# # Create vertices and edges DataFrames for GraphFrames
# vertices_df = pd.DataFrame(consumer_data)
# edges_data = []
# for edge in network.edges():
#     edges_data.append({
#         'src': f'user_{edge[0]}',
#         'dst': f'user_{edge[1]}',
#         'relationship': 'friend'
#     })
# edges_df = pd.DataFrame(edges_data)

# # Save datasets
# vertices_df.to_csv('consumer_vertices.csv', index=False)
# edges_df.to_csv('consumer_edges.csv', index=False)
