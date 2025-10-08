import plotly.graph_objects as go
import json

# Data for the pipeline stages
data = {
    "stages": [
        {"name": "Read SEC Filings from S3", "description": "Load text files using spark.read.text()"},
        {"name": "Beautiful Soup Cleaning", "description": "Remove HTML tags and extract plain text"},
        {"name": "NLTK Preprocessing", "description": "Tokenization and sentence segmentation"},
        {"name": "SpaCy NER", "description": "Extract named entities (PERSON, ORG, GPE)"},
        {"name": "Paragraph Extraction", "description": "Find paragraphs containing entities"},
        {"name": "Save to S3", "description": "Store processed results"}
    ]
}

# Create figure
fig = go.Figure()

# Define colors for stages
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C', '#B4413C']

# Create boxes and text for each stage
box_width = 0.8
box_height = 0.6
y_center = 0

# Truncate stage names and descriptions to fit character limits
stage_info = []
for stage in data['stages']:
    name = stage['name']
    desc = stage['description']
    
    # Truncate names to 15 characters
    if len(name) > 15:
        if 'S3' in name:
            if 'Read' in name:
                name = "Read from S3"
            else:
                name = "Save to S3"
        elif 'Beautiful Soup' in name:
            name = "HTML Clean"
        elif 'NLTK' in name:
            name = "NLTK Process"
        elif 'SpaCy' in name:
            name = "SpaCy NER"
        elif 'Paragraph' in name:
            name = "Para Extract"
    
    # Truncate descriptions to 15 characters
    if len(desc) > 15:
        desc = desc[:12] + "..."
    
    stage_info.append({'name': name, 'desc': desc})

# Add rectangular shapes for each stage
for i, (stage, color) in enumerate(zip(stage_info, colors)):
    x_center = i * 1.5
    
    # Add rectangle shape
    fig.add_shape(
        type="rect",
        x0=x_center - box_width/2,
        y0=y_center - box_height/2,
        x1=x_center + box_width/2,
        y1=y_center + box_height/2,
        fillcolor=color,
        opacity=0.9,
        line=dict(color="#13343B", width=2)
    )
    
    # Add stage name text (larger, bold, black)
    fig.add_trace(go.Scatter(
        x=[x_center],
        y=[y_center + 0.12],
        text=f"<b>{stage['name']}</b>",
        mode='text',
        textfont=dict(size=12, color='black'),
        showlegend=False,
        hovertemplate=f"<b>{stage['name']}</b><br>{data['stages'][i]['description']}<extra></extra>"
    ))
    
    # Add stage description text (smaller, black)
    fig.add_trace(go.Scatter(
        x=[x_center],
        y=[y_center - 0.12],
        text=stage['desc'],
        mode='text',
        textfont=dict(size=10, color='black'),
        showlegend=False,
        hovertemplate=f"<b>{stage['name']}</b><br>{data['stages'][i]['description']}<extra></extra>"
    ))

# Add arrows between stages using line shapes
for i in range(len(stage_info) - 1):
    x_start = i * 1.5 + box_width/2
    x_end = (i + 1) * 1.5 - box_width/2
    
    # Arrow line (thicker)
    fig.add_shape(
        type="line",
        x0=x_start,
        y0=y_center,
        x1=x_end - 0.15,
        y1=y_center,
        line=dict(color="#13343B", width=4)
    )
    
    # Arrow head (triangle, larger)
    fig.add_shape(
        type="path",
        path=f"M {x_end},{y_center} L {x_end-0.15},{y_center-0.08} L {x_end-0.15},{y_center+0.08} Z",
        fillcolor="#13343B",
        line=dict(color="#13343B")
    )

# Update layout
fig.update_layout(
    title="Spark SEC Pipeline",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        range=[-0.5, (len(stage_info) - 1) * 1.5 + 0.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        range=[-1, 1]
    ),
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode='closest'
)

# Apply cliponaxis
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

fig.show()