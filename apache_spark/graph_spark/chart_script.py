import plotly.graph_objects as go
import json

# Load the provided data
data = {
    "features": ["Language Support", "Abstraction", "API Style", "Performance", "Use Cases", "Vertex ID Type", "Attributes", "Return Types", "SQL Integration", "Motif Finding", "Status", "Learning Curve"],
    "GraphX": ["Scala only", "RDD-based", "Functional, low-level", "High for iterative", "Algorithms only", "Long only", "Any type (VD, ED)", "Graph[VD,ED]/RDDs", "Limited", "No", "Maintenance", "Steep"],
    "GraphFrames": ["Scala, Python, Java, R", "DataFrame-based", "Declarative, high-level", "Catalyst optimized", "Algorithms, queries, motifs", "Any Catalyst type", "DataFrame columns", "GraphFrames/DataFrames", "Full Spark SQL", "Yes", "Active development", "Moderate"]
}

# Abbreviate text to meet 15-character limit
features_abbrev = ["Lang Support", "Abstraction", "API Style", "Performance", "Use Cases", "Vertex ID Type", "Attributes", "Return Types", "SQL Integration", "Motif Finding", "Status", "Learning Curve"]

graphx_abbrev = [
    "Scala only",
    "RDD-based", 
    "Functional/low",
    "High iterative",
    "Algorithms only",
    "Long only",
    "Any type VD/ED",
    "Graph/RDDs",
    "Limited",
    "No",
    "Maintenance",
    "Steep"
]

graphframes_abbrev = [
    "Scala/Py/Java/R",
    "DataFrame-based",
    "Declarative/hi",
    "Catalyst optim",
    "Algo/queries",
    "Any Catalyst",
    "DataFrame cols",
    "GraphFrames/DF", 
    "Full Spark SQL",
    "Yes",
    "Active dev",
    "Moderate"
]

# Create the table
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Feature</b>', '<b>GraphX</b>', '<b>GraphFrames</b>'],
        fill_color='#1FB8CD',
        font=dict(color='white', size=14),
        align='left',
        height=40
    ),
    cells=dict(
        values=[features_abbrev, graphx_abbrev, graphframes_abbrev],
        fill_color=[['#f8f9fa']*len(features_abbrev), 
                   ['#ffebee']*len(graphx_abbrev), 
                   ['#e8f5e8']*len(graphframes_abbrev)],
        font=dict(color='black', size=12),
        align='left',
        height=35
    )
)])

fig.update_layout(
    title='GraphX vs GraphFrames Comparison',
    font=dict(family="Arial, sans-serif")
)

# Save as PNG and SVG
fig.write_image("comparison_chart.png")
fig.write_image("comparison_chart.svg", format="svg")