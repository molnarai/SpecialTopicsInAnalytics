+++
date = '2025-09-17'
draft = false
title = 'Apache Spark & Advanced DataFrames'
weight = 40
numsession = 4
+++
This session covers Apache Spark, its architecture, and various components, providing a comprehensive overview of the unified analytics engine.
<!-- more -->

We discuss how Apache Spark offers in-memory processing and supports a wide range of data sources, enabling it to handle large-scale datasets by distributing computations across multiple nodes in the cluster. We also explore its key features, including high-level APIs, streaming capabilities, and advanced data processing techniques.

We compare Spark to Pandas, highlighting their respective strengths and use cases. We show how Spark is particularly suited for big data analytics and distributed computing, whereas Pandas excels at in-memory computing with smaller datasets. The choice between the two ultimately depends on the specific requirements of a project.

In this session, we introduce Spark DataFrames, covering various aspects such as schema, loading data, and inspecting DataFrames. We demonstrate how to create a DataFrame from different sources like CSV files, JSON, or databases, and explain how to manipulate DataFrames using methods provided by the API.

We also cover advanced operations on DataFrames, including column and row manipulations, filtering and conditional logic, aggregations, joins, window functions, handling missing data, and integrating with SQL queries. Throughout this session, we provide various techniques for optimizing performance and ensuring efficient computation.





<!-- "What is Apache Spark? Architecture & Components (RDDs, DataFrames, Spark SQL)
Spark vs Pandas: Why and when to use Spark
Introduction to Spark DataFrames: Schema, loading data, inspecting DataFrames
Distributed computing basics in Spark: Partitions and transformations
Advanced DataFrame operations:
Column and row manipulations
Complex filtering and conditional logic
GroupBy, aggregations
Joins and window functions
Handling missing data and data types
Integrating with SQL: Using Spark SQL queries with Python" -->




## Required Reading and Listening
<!-- Listen to the [podcast](../../podcasts/podcast-04-fine-tuning/): -->
Listen to the podcast:

 <audio controls>
    <source src="https://insight-gsu-edu-msa8700-public-files-us-east-1.s3.us-east-1.amazonaws.com/podcast/From_SQL_to_Spark__Navigating_the_Data_Deluge_and_Unpacking_Big.mp4" type="audio/mp4">
    Your browser does not support the audio element.
</audio>

Read the following:
1. Summary Page: [Big Data Processing Evolution](https://www.perplexity.ai/page/big-data-processing-evolution-3ebHS_CfRuCrqxvXdRt1tA)
2. Textbook: [Part I](https://go.oreilly.com/georgia-state-university/library/view/data-analysis-with/9781617297205/OEBPS/Text/p1.htm) in Jonathan Rioux, [Data Analysis with Python and PySpark](https://go.oreilly.com/georgia-state-university/library/view/data-analysis-with/9781617297205/)  O'Reilly Media Inc., 2022. 




<!-- Content URL:
Syntax: https://go.oreilly.com/{CONNECTION_STRING}{CONTENT_PATH}
Example: https://go.oreilly.com/georgia-state-university/library/view/building-microservices/9781491950340/
Another example: https://go.oreilly.com/georgia-state-university/library/view/the-fast-forward/9781119700760/ -->



## Study Guide - Questions
- What is Apache Spark? Architecture & Components (RDDs, DataFrames, Spark SQL)
- Spark vs Pandas: Why and when to use Spark
- Introduction to Spark DataFrames: Schema, loading data, inspecting DataFrames
- Distributed computing basics in Spark: Partitions and transformations
- Advanced DataFrame operations:
    - Column and row manipulations
    - Complex filtering and conditional logic
    - GroupBy, aggregations
    - Joins and window functions
- Handling missing data and data types
- Integrating with SQL: Using Spark SQL queries with Python

## Links
- [ARCTIC Callisto]( https://callisto.rs.gsu.edu) Access Jypyter Notebooks and Spark Cluster

## Additional Resources
- [Getting Started with PySpark](https://spark.apache.org/docs/latest/api/python/getting_started/index.html) 
- [PySpark USer Guide](https://spark.apache.org/docs/latest/api/python/user_guide/index.html)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/index.html)
- [How to submit a Spark job on ARCTIC](https://arcwiki.rs.gsu.edu/en/Spark)

