import plotly.graph_objects as go
import json

# Parse the project structure data
data = {
    "project_structure": {
        "name": "sec-filing-processor", 
        "type": "folder", 
        "children": [
            {
                "name": "Application Code", 
                "type": "category", 
                "children": [
                    {
                        "name": "sec_filing_processor.py", 
                        "type": "file", 
                        "description": "Main Spark application with NLP processing"
                    }
                ]
            }, 
            {
                "name": "Deployment", 
                "type": "category", 
                "children": [
                    {
                        "name": "deploy_spark_k8s.sh", 
                        "type": "file", 
                        "description": "Kubernetes deployment and job submission script"
                    }, 
                    {
                        "name": "Dockerfile", 
                        "type": "file", 
                        "description": "Multi-stage Docker build with NLP dependencies"
                    }, 
                    {
                        "name": "pod-template.yaml", 
                        "type": "file", 
                        "description": "Advanced Kubernetes pod configuration"
                    }
                ]
            }, 
            {
                "name": "Configuration", 
                "type": "category", 
                "children": [
                    {
                        "name": "config.yaml", 
                        "type": "file", 
                        "description": "Application and infrastructure settings"
                    }, 
                    {
                        "name": "requirements.txt", 
                        "type": "file", 
                        "description": "Python dependencies with pinned versions"
                    }
                ]
            }, 
            {
                "name": "Documentation", 
                "type": "category", 
                "children": [
                    {
                        "name": "README.md", 
                        "type": "file", 
                        "description": "Complete usage guide and documentation"
                    }
                ]
            }
        ]
    }
}

# Prepare data for sunburst chart
ids = []
labels = []
parents = []
values = []
colors = []

# Brand colors
category_colors = {
    "Application Code": "#1FB8CD",  # Strong cyan
    "Deployment": "#DB4545",       # Bright red  
    "Configuration": "#2E8B57",    # Sea green
    "Documentation": "#5D878F"     # Cyan
}

# Root node
ids.append("root")
labels.append("sec-filing-processor")
parents.append("")
values.append(1)
colors.append("#13343B")  # Dark cyan for root

# Add categories
for category in data["project_structure"]["children"]:
    cat_name = category["name"]
    cat_id = cat_name.replace(" ", "_").lower()
    
    ids.append(cat_id)
    labels.append(cat_name)
    parents.append("root")
    values.append(len(category["children"]))
    colors.append(category_colors[cat_name])
    
    # Add files in each category
    for file_item in category["children"]:
        file_name = file_item["name"]
        file_id = f"{cat_id}_{file_name.replace('.', '_').replace('-', '_')}"
        
        ids.append(file_id)
        labels.append(file_name)
        parents.append(cat_id)
        values.append(1)
        # Use a slightly lighter shade for files
        colors.append(category_colors[cat_name])

# Create sunburst chart
fig = go.Figure(go.Sunburst(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    branchvalues="total",
    marker=dict(colors=colors),
    hovertemplate='<b>%{label}</b><br>Type: %{customdata}<extra></extra>',
    maxdepth=3
))

fig.update_layout(
    title="SEC Filing Processor Structure",
    font_size=12
)

# Save as both PNG and SVG
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

fig.show()