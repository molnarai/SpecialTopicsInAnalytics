# Create a comprehensive lesson plan structure and save to CSV for the Apache Spark graph algorithms session

import pandas as pd
from datetime import datetime, timedelta

# Create lesson plan structure
lesson_plan = {
    'Module': [
        'Introduction & Setup',
        'Scala Basics for Python Developers',
        'Scala-PySpark Interoperability',
        'Graph Theory Fundamentals',
        'Apache Spark Graph Processing',
        'GraphX vs GraphFrames',
        'Graph Algorithms Overview',
        'Break',
        'Hands-on Setup',
        'Data Preparation',
        'Graph Construction',
        'Algorithm Implementation',
        'PageRank Analysis',
        'Connected Components',
        'Practical Applications',
        'Performance & Optimization'
    ],
    'Duration_Minutes': [15, 30, 20, 25, 20, 15, 25, 15, 20, 25, 30, 35, 25, 20, 20, 15],
    'Type': [
        'Theory', 'Theory', 'Theory', 'Theory', 'Theory', 'Theory', 'Theory', 'Break',
        'Hands-on', 'Hands-on', 'Hands-on', 'Hands-on', 'Hands-on', 'Hands-on', 'Hands-on', 'Hands-on'
    ],
    'Key_Topics': [
        'Course objectives, prerequisites, tools setup',
        'Syntax comparison, functions, collections, pattern matching',
        'UDF creation, JAR integration, Py4j bridge',
        'Vertices, edges, directed/undirected graphs, properties',
        'GraphX architecture, RDD-based processing',
        'DataFrame vs RDD, API differences, performance',
        'PageRank, Connected Components, Triangle Counting, Shortest Path',
        'Coffee break and Q&A',
        'Environment setup, dataset download, Spark configuration',
        'Facebook ego-networks data cleaning and transformation',
        'Creating GraphFrame from vertices and edges DataFrames',
        'Implementing graph algorithms with real data',
        'Ranking influential nodes in social network',
        'Finding communities and isolated subgraphs',
        'Social network analysis, recommendation systems',
        'Memory tuning, partitioning strategies, caching'
    ],
    'Learning_Outcomes': [
        'Understanding session structure and expectations',
        'Ability to read and write basic Scala code',
        'Knowledge of using Scala functions in PySpark',
        'Solid foundation in graph concepts and terminology',
        'Understanding of Spark\'s graph processing capabilities',
        'Ability to choose appropriate graph API',
        'Knowledge of available algorithms and use cases',
        'Refreshed and ready for hands-on work',
        'Working Spark environment with GraphFrames',
        'Clean, analysis-ready graph dataset',
        'Functional graph data structure in Spark',
        'Practical experience with graph algorithms',
        'Understanding centrality and influence metrics',
        'Experience with community detection',
        'Real-world applications of graph analytics',
        'Performance optimization techniques'
    ]
}

# Create DataFrame
df = pd.DataFrame(lesson_plan)

# Calculate cumulative time
df['Start_Time'] = 0
df['End_Time'] = 0

current_time = 0
for i in range(len(df)):
    df.loc[i, 'Start_Time'] = current_time
    current_time += df.loc[i, 'Duration_Minutes']
    df.loc[i, 'End_Time'] = current_time

# Add session phases
df['Phase'] = ['Theory' if i < 8 else 'Hands-on' for i in range(len(df))]

# Save to CSV
df.to_csv('spark_graph_algorithms_lesson_plan.csv', index=False)

print("Lesson Plan Overview:")
print("="*50)
print(f"Total Duration: {df['Duration_Minutes'].sum()} minutes ({df['Duration_Minutes'].sum()/60:.1f} hours)")
print(f"Theory Phase: {df[df['Phase']=='Theory']['Duration_Minutes'].sum()} minutes")
print(f"Hands-on Phase: {df[df['Phase']=='Hands-on']['Duration_Minutes'].sum()} minutes")
print("\nDetailed Schedule:")
print(df[['Module', 'Duration_Minutes', 'Type', 'Start_Time', 'End_Time']].to_string(index=False))