import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Load the data
data = {
    "modules": ["Introduction & Setup", "Scala Basics for Python Developers", "Scala-PySpark Interoperability", "Graph Theory Fundamentals", "Apache Spark Graph Processing", "GraphX vs GraphFrames", "Graph Algorithms Overview", "Break", "Hands-on Setup", "Data Preparation", "Graph Construction", "Algorithm Implementation", "PageRank Analysis", "Connected Components", "Practical Applications", "Performance & Optimization"],
    "duration_minutes": [15, 30, 20, 25, 20, 15, 25, 15, 20, 25, 30, 35, 25, 20, 20, 15],
    "type": ["Theory", "Theory", "Theory", "Theory", "Theory", "Theory", "Theory", "Break", "Hands-on", "Hands-on", "Hands-on", "Hands-on", "Hands-on", "Hands-on", "Hands-on", "Hands-on"],
    "start_time": [0, 15, 45, 65, 90, 110, 125, 150, 165, 185, 210, 240, 275, 300, 320, 340],
    "end_time": [15, 45, 65, 90, 110, 125, 150, 165, 185, 210, 240, 275, 300, 320, 340, 355]
}

df = pd.DataFrame(data)

# Truncate module names to 15 characters
df['short_modules'] = df['modules'].apply(lambda x: x[:12] + '...' if len(x) > 15 else x)

# Define colors for each type
color_map = {
    'Theory': '#1FB8CD',
    'Hands-on': '#DB4545', 
    'Break': '#D2BA4C'
}

# Create the figure
fig = go.Figure()

# Add bars for each module
for i, row in df.iterrows():
    fig.add_trace(go.Bar(
        x=[row['duration_minutes']],
        y=[row['short_modules']],
        orientation='h',
        name=row['type'],
        marker_color=color_map[row['type']],
        base=row['start_time'],
        showlegend=True if i == 0 or (i > 0 and row['type'] != df.iloc[i-1]['type']) else False,
        hovertemplate=f"<b>{row['modules']}</b><br>Type: {row['type']}<br>Duration: {row['duration_minutes']} min<br>Time: {row['start_time']}-{row['end_time']} min<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title='Spark Graph Algo Session',
    xaxis_title='Time (minutes)',
    yaxis_title='Modules',
    xaxis=dict(range=[0, 360]),
    barmode='overlay',
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Update y-axis to show modules in reverse order (top to bottom chronologically)
fig.update_yaxes(categoryorder='array', categoryarray=df['short_modules'].tolist()[::-1])

# Save the chart
fig.write_image("timeline_chart.png")
fig.write_image("timeline_chart.svg", format="svg")