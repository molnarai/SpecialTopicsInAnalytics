# Create practical code examples for the hands-on session

# GraphFrames setup and basic usage examples
graphframes_code_examples = """
# GRAPHFRAMES SETUP AND EXAMPLES FOR APACHE SPARK SESSION

## 1. Environment Setup
```bash
# Install GraphFrames package
pip install graphframes-py==0.9.3

# Start PySpark with GraphFrames
pyspark --packages io.graphframes:graphframes-spark3_2.12:0.9.3
```

## 2. Scala UDF in PySpark Example
```scala
// Scala UDF to calculate node importance score
import org.apache.spark.sql.functions.udf

val calculateImportance = udf((degree: Int, triangles: Int) => {
  if (degree == 0) 0.0
  else (triangles.toDouble / degree) * Math.log(degree + 1)
})

spark.udf.register("importance_score", calculateImportance)
```

```python
# Using the Scala UDF in PySpark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# The Scala UDF is now available in Python
df_with_importance = vertices_df.withColumn(
    "importance", 
    spark.sql("SELECT importance_score(degree, triangles) as score").collect()[0][0]
)
```

## 3. Facebook Ego Networks Data Preparation
```python
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from graphframes import GraphFrame

spark = SparkSession.builder \\
    .appName("GraphAlgorithmsDemo") \\
    .getOrCreate()

# Load Facebook combined edges (download from SNAP)
edges_df = spark.read.text("facebook_combined.txt") \\
    .selectExpr("split(value, ' ') as edge") \\
    .selectExpr("cast(edge[0] as int) as src", "cast(edge[1] as int) as dst") \\
    .withColumn("relationship", lit("friend"))

# Create vertices from unique node IDs
vertices_df = edges_df.select("src").union(edges_df.select("dst")) \\
    .distinct() \\
    .withColumnRenamed("src", "id") \\
    .withColumn("name", concat(lit("User_"), col("id"))) \\
    .withColumn("age", (rand() * 50 + 18).cast("int"))

# Create GraphFrame
g = GraphFrame(vertices_df, edges_df)
```

## 4. Graph Algorithm Implementations
```python
# PageRank - Find most influential users
print("Running PageRank...")
pagerank_result = g.pageRank(resetProbability=0.15, maxIter=10)
top_influencers = pagerank_result.vertices \\
    .select("id", "name", "pagerank") \\
    .orderBy(col("pagerank").desc()) \\
    .limit(10)
top_influencers.show()

# Connected Components - Find communities
print("Finding connected components...")
components = g.connectedComponents()
community_sizes = components.groupBy("component") \\
    .count() \\
    .orderBy(col("count").desc())
community_sizes.show()

# Triangle Count - Measure clustering
print("Counting triangles...")
triangle_counts = g.triangleCount()
clustering_metrics = triangle_counts \\
    .join(g.degrees, "id") \\
    .withColumn("clustering_coeff", 
                when(col("degree") <= 1, 0.0)
                .otherwise(col("count") * 2.0 / (col("degree") * (col("degree") - 1))))
clustering_metrics.show()

# Motif Finding - Find mutual friends pattern
print("Finding motif patterns...")
motifs = g.find("(a)-[e1]->(b); (b)-[e2]->(a); (b)-[e3]->(c); (c)-[e4]->(b)") \\
    .filter("a.id != c.id")
mutual_friends = motifs.select("a.name", "b.name", "c.name") \\
    .withColumnRenamed("a.name", "user1") \\
    .withColumnRenamed("b.name", "mutual_friend") \\
    .withColumnRenamed("c.name", "user2")
mutual_friends.show(20)
```

## 5. Performance Optimization Examples
```python
# Caching frequently used DataFrames
g.vertices.cache()
g.edges.cache()

# Partitioning strategy for better performance
edges_partitioned = edges_df.repartition(200, "src")
vertices_partitioned = vertices_df.repartition(50, "id")

# Checkpoint for iterative algorithms
spark.sparkContext.setCheckpointDir("/tmp/graphframes-checkpoints")
g.connectedComponents().checkpoint()

# Memory optimization
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

## 6. Scala Function Integration
```scala
// Create a JAR with custom graph functions
object GraphAnalytics {
  def communityScore(degree: Int, triangles: Int, componentSize: Long): Double = {
    val density = if (degree > 0) triangles.toDouble / degree else 0.0
    val normalization = Math.log(componentSize + 1)
    density * normalization
  }
  
  def influenceSpread(pagerank: Double, degree: Int): Double = {
    pagerank * Math.sqrt(degree)
  }
}
```

```python
# Use the JAR in PySpark
spark.sparkContext.addPyFile("graph-analytics.jar")

# Register as UDF
spark.udf.registerJavaFunction("community_score", 
                               "GraphAnalytics.communityScore",
                               "double")
```
"""

# Save the code examples
with open('graphframes_code_examples.py', 'w') as f:
    f.write(graphframes_code_examples)

# Create hands-on exercises
hands_on_exercises = {
    'Exercise': [
        'Environment Setup',
        'Data Loading & Exploration', 
        'Basic Graph Construction',
        'PageRank Analysis',
        'Community Detection',
        'Triangle Counting',
        'Motif Finding',
        'Performance Optimization'
    ],
    'Objective': [
        'Set up Spark with GraphFrames package',
        'Load Facebook dataset and explore structure',
        'Create GraphFrame from vertices and edges',
        'Identify top influential nodes using PageRank',
        'Find communities using Connected Components',
        'Calculate clustering coefficients',
        'Find interesting graph patterns',
        'Optimize performance for large graphs'
    ],
    'Expected_Output': [
        'Working Spark session with GraphFrames',
        'Dataset statistics and sample data',
        'Functional GraphFrame object',
        'Top 10 most influential users',
        'Community size distribution',
        'Clustering coefficient statistics',
        'Friendship recommendation patterns',
        'Performance metrics before/after optimization'
    ],
    'Difficulty': ['Easy', 'Easy', 'Medium', 'Medium', 'Medium', 'Hard', 'Hard', 'Advanced'],
    'Time_Minutes': [15, 20, 25, 20, 25, 20, 30, 20]
}

exercises_df = pd.DataFrame(hands_on_exercises)
exercises_df.to_csv('hands_on_exercises.csv', index=False)

print("Code Examples and Exercises Created!")
print("="*50)
print("Files generated:")
print("- graphframes_code_examples.py")
print("- hands_on_exercises.csv")
print("\nHands-on Exercises Overview:")
print(exercises_df[['Exercise', 'Objective', 'Difficulty', 'Time_Minutes']].to_string(index=False))