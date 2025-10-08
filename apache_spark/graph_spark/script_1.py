# Create sample code examples and datasets information

# Scala basics examples for Python developers
scala_examples = {
    'Concept': [
        'Variable Declaration',
        'Function Definition',
        'Anonymous Function',
        'Collections - List',
        'Collections - Map',
        'Pattern Matching',
        'Case Classes',
        'Higher Order Functions'
    ],
    'Python_Code': [
        'x = 42\ny = "hello"',
        'def add(x, y):\n    return x + y',
        'lambda x, y: x + y',
        'numbers = [1, 2, 3, 4, 5]',
        'person = {"name": "Alice", "age": 30}',
        '# No direct equivalent\nif x == 1:\n    result = "one"\nelif x == 2:\n    result = "two"',
        'class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age',
        'numbers.map(lambda x: x * 2)'
    ],
    'Scala_Code': [
        'val x = 42\nval y = "hello"',
        'def add(x: Int, y: Int): Int = x + y',
        '(x: Int, y: Int) => x + y',
        'val numbers = List(1, 2, 3, 4, 5)',
        'val person = Map("name" -> "Alice", "age" -> 30)',
        'val result = x match {\n  case 1 => "one"\n  case 2 => "two"\n  case _ => "other"\n}',
        'case class Person(name: String, age: Int)',
        'numbers.map(_ * 2)'
    ]
}

# GraphFrames algorithms overview
graph_algorithms = {
    'Algorithm': [
        'PageRank',
        'Connected Components',
        'Strongly Connected Components', 
        'Triangle Count',
        'Label Propagation',
        'Shortest Paths',
        'Breadth First Search',
        'Motif Finding'
    ],
    'Description': [
        'Ranks vertices by importance using link structure',
        'Finds weakly connected components in undirected graphs',
        'Finds strongly connected components in directed graphs',
        'Counts triangles each vertex participates in',
        'Community detection through label propagation',
        'Computes shortest paths from source vertices',
        'Traverses graph level by level from source',
        'Finds structural patterns in graphs using SQL-like syntax'
    ],
    'Use_Cases': [
        'Web page ranking, social influence, protein importance',
        'Social communities, network components, data deduplication',
        'Web structure analysis, citation networks',
        'Network clustering coefficient, social cohesion',
        'Community detection, clustering, recommendation',
        'Navigation systems, network routing, six degrees',
        'Social network exploration, dependency analysis',
        'Fraud detection, recommendation patterns, anomaly detection'
    ],
    'Complexity': [
        'O(V + E) per iteration',
        'O(V + E)',
        'O(V + E)',
        'O(V * d²) where d=degree',
        'O(V + E) per iteration',
        'O(V + E) for BFS',
        'O(V + E)',
        'Depends on pattern complexity'
    ],
    'GraphFrames_API': [
        'g.pageRank.resetProbability(0.15).maxIter(10).run()',
        'g.connectedComponents.run()',
        'g.stronglyConnectedComponents.maxIter(10).run()',
        'g.triangleCount.run()',
        'g.labelPropagation.maxIter(5).run()',
        'g.shortestPaths.landmarks(["a", "b"]).run()',
        'g.bfs.fromExpr("id = \'a\'").toExpr("id = \'b\'").run()',
        'g.find("(a)-[e]->(b); (b)-[e2]->(c)")'
    ]
}

# Dataset information
datasets_info = {
    'Dataset': [
        'Facebook Ego Networks',
        'CiteSeer Citation Network',
        'Stanford Web Graph',
        'Amazon Co-purchasing',
        'Collaboration Networks'
    ],
    'Nodes': [4039, 3312, 281903, 334863, 227320],
    'Edges': [88234, 4732, 2312497, 925872, 814134],
    'Type': ['Social', 'Citation', 'Web', 'Co-purchase', 'Collaboration'],
    'Format': [
        'Edge list, node features',
        'Edge list with categories', 
        'Edge list',
        'Edge list with product info',
        'Edge list'
    ],
    'Best_For': [
        'Social network analysis, community detection',
        'Citation analysis, academic influence',
        'Web structure, PageRank demonstration',
        'Recommendation systems',
        'Scientific collaboration patterns'
    ]
}

# Create DataFrames and save
scala_df = pd.DataFrame(scala_examples)
algorithms_df = pd.DataFrame(graph_algorithms)
datasets_df = pd.DataFrame(datasets_info)

scala_df.to_csv('scala_python_comparison.csv', index=False)
algorithms_df.to_csv('graph_algorithms_reference.csv', index=False)
datasets_df.to_csv('graph_datasets_info.csv', index=False)

print("Scala-Python Comparison:")
print("="*50)
print(scala_df[['Concept', 'Python_Code', 'Scala_Code']].head(3).to_string(index=False))

print("\n\nGraph Algorithms Summary:")
print("="*50)
print(algorithms_df[['Algorithm', 'Description', 'Use_Cases']].head(3).to_string(index=False))

print("\n\nRecommended Datasets:")
print("="*50)
print(datasets_df[['Dataset', 'Nodes', 'Edges', 'Type', 'Best_For']].to_string(index=False))