+++
date = '2025-01-06T18:20:46-05:00'
due_date = "2025-10-15"
draft = false
title = 'Apache Spark Project'
subject = 'spark'
weight = 10
status = 'Posted'
+++

For your Spark programming project, you will explore a large, real-world public dataset using PySpark and transform complex data into actionable insights, culminating in professional visualizations. The goal is to simulate a practical data analytics workflow akin to those found in industry: you will acquire and preprocess the data at scale using Spark, define and compute three significant business or analytical insights, and present each insight through well-crafted static plots. This project challenges you not only to harness distributed computing for big data processing, but also to bridge the gap between large-scale computation and clear, impactful communication of findings, preparing your analyses as compelling visual reports ready for BI or decision-making audiences. Through this assignment, you'll develop the core skills of data wrangling, scalable analysis, and effective storytelling with data—making your technical results accessible and persuasive to both technical and non-technical stakeholders.

<!-- more -->


## Objective
Write a PySpark program that analyzes one large public dataset, generates at least three different business insights, and produces results as static plots using matplotlib or any other library capable of creating static (non-interactive) visualizations.
## Steps

1. Select Your Dataset
   Choose one of:
   -	NYC Yellow Taxi Trip Data (Kaggle or NYC official data portal)
   -	MovieLens Movie Ratings (GroupLens/Kaggle)
   -	COVID-19 Open Data (Johns Hopkins CSSE, Our World in Data, or Google COVID-19 Open Data)
2. Define Three Insights
   Pick and clearly describe three insights (see the dataset-insight matrix in the previous instructions). Each should be significant and suitable for visual representation (e.g., trends, comparisons, distributions).
3. Data Processing and Analysis
   -	Ingest and process the dataset using PySpark DataFrames and/or SQL.
   -	Perform cleaning, type conversions, and any necessary preprocessing.
   -	Carefully compute your chosen insights.
4. Visualization Requirement (REVISED)
   -	For each insight, generate at least one static plot using matplotlib, seaborn, or any comparable static visualization package.
      - Each plot must be meaningful: Examples include time series charts, bar plots, histograms, heatmaps, scatter plots, or maps.
      - You may convert Spark DataFrames to Pandas (using .toPandas()) before plotting if needed, but only after the spark-based processing is complete.
-	Plots should be saved as PNG, JPG, or PDF images and displayed within the notebook/script.
5. Output for BI Visualization
   -	Clearly display and save each generated plot.
   -	For each insight, include:
   - A title and caption/legend explaining what is being shown
   - A markdown cell with:
      - The objective of the insight
      - 	The business or analytical value
6. Deliverables
   -	Well-commented PySpark notebook or script (.ipynb or .py) that produces and saves the required plots.
   -	Short README (markdown) that covers:
      - Data source and description
      - The three insights and why they were chosen
      - How to run the program (Spark and plotting requirements)
      -	Resulting plot files (if submitting outside notebook format), or embedded plots if using Jupyter.
7. (Optional) Extension
   -	You may go further by adding additional advanced Spark features (MLlib, GraphFrames, etc.), as desired.
   
Additional Guidelines
-	Use Spark for heavy data processing—only use Pandas for small dataframes and plotting.
-	Keep visualizations clear and professional.
-	Label axes, include legends where necessary, and provide descriptive titles for all plots.
-	Save plot images in a designated output folder or display inline within the notebook.
This ensures students not only practice Spark data analysis but also learn to communicate results visually using static plots appropriate for BI reporting.
