
"""
SEC Filing Processing Pipeline with Apache Spark 4.0.1
Processing SEC filings with Beautiful Soup, NLTK, and SpaCy for entity extraction
"""

import os
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, collect_list, explode, lit
from pyspark.sql.types import StringType, ArrayType, StructType, StructField
from pyspark import SparkContext
import nltk
import spacy
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SECFilingProcessor:
    """
    Main processor class for SEC filings analysis
    """

    def __init__(self, app_name="SEC-Filing-Processor"):
        """Initialize Spark session and NLP models"""
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()

        # Set log level
        self.spark.sparkContext.setLogLevel("INFO")

        # Initialize NLP models (will be loaded on each worker)
        self._init_nlp_models()

    def _init_nlp_models(self):
        """Initialize NLTK and SpaCy models"""
        # Download required NLTK data if not present
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')

    def clean_html_text(self, html_content):
        """
        Clean HTML content using Beautiful Soup
        """
        if not html_content:
            return ""

        try:
            soup = BeautifulSoup(html_content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text and clean whitespace
            text = soup.get_text()

            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()

            return text
        except Exception as e:
            logger.error(f"Error cleaning HTML: {str(e)}")
            return html_content

    def extract_entities_and_paragraphs(self, text):
        """
        Extract named entities and paragraphs containing those entities
        """
        if not text or len(text.strip()) == 0:
            return []

        try:
            # Load SpaCy model (will be cached per executor)
            nlp = spacy.load("en_core_web_sm")

            # Process text with SpaCy
            doc = nlp(text)

            # Extract entities
            entities = []
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'GPE', 'MONEY', 'PERCENT']:
                    entities.append({
                        'text': ent.text,
                        'label': ent.label_,
                        'start': ent.start_char,
                        'end': ent.end_char
                    })

            # Split text into sentences using NLTK
            sentences = nltk.sent_tokenize(text)

            # Group sentences into paragraphs (simple heuristic)
            paragraphs = []
            current_para = []

            for sentence in sentences:
                current_para.append(sentence)
                # End paragraph on double newline or if paragraph gets too long
                if '\n\n' in sentence or len(' '.join(current_para)) > 1000:
                    paragraphs.append(' '.join(current_para))
                    current_para = []

            if current_para:
                paragraphs.append(' '.join(current_para))

            # Find paragraphs containing entities
            result = []
            for entity in entities:
                entity_text = entity['text']
                for i, paragraph in enumerate(paragraphs):
                    if entity_text.lower() in paragraph.lower():
                        result.append({
                            'entity_text': entity_text,
                            'entity_label': entity['label'],
                            'paragraph_id': i,
                            'paragraph_text': paragraph,
                            'entity_start': entity['start'],
                            'entity_end': entity['end']
                        })

            return result

        except Exception as e:
            logger.error(f"Error processing text: {str(e)}")
            return []

    def process_sec_filings(self, s3_input_path, s3_output_path):
        """
        Main processing pipeline
        """
        logger.info(f"Starting SEC filing processing from {s3_input_path}")

        # Read text files from S3
        raw_df = self.spark.read.text(s3_input_path)
        logger.info(f"Loaded {raw_df.count()} files")

        # Add filename column
        raw_df = raw_df.withColumn("filename", 
                                   col("value").substr(1, 100))  # Simple filename extraction

        # Define UDF for HTML cleaning
        clean_html_udf = udf(self.clean_html_text, StringType())

        # Clean HTML content
        cleaned_df = raw_df.withColumn("clean_text", clean_html_udf(col("value")))

        # Define UDF for entity extraction
        extract_entities_udf = udf(self.extract_entities_and_paragraphs, 
                                   ArrayType(StructType([
                                       StructField("entity_text", StringType()),
                                       StructField("entity_label", StringType()),
                                       StructField("paragraph_id", StringType()),
                                       StructField("paragraph_text", StringType()),
                                       StructField("entity_start", StringType()),
                                       StructField("entity_end", StringType())
                                   ])))

        # Extract entities and paragraphs
        entities_df = cleaned_df.withColumn("entities", 
                                            extract_entities_udf(col("clean_text")))

        # Explode entities array to separate rows
        final_df = entities_df.select(
            col("filename"),
            explode(col("entities")).alias("entity_info")
        ).select(
            col("filename"),
            col("entity_info.entity_text"),
            col("entity_info.entity_label"),
            col("entity_info.paragraph_id"),
            col("entity_info.paragraph_text"),
            col("entity_info.entity_start"),
            col("entity_info.entity_end")
        )

        # Cache results for better performance
        final_df.cache()

        logger.info(f"Extracted {final_df.count()} entity-paragraph pairs")

        # Write results to S3
        final_df.coalesce(10).write \
            .mode("overwrite") \
            .option("header", "true") \
            .csv(s3_output_path)

        logger.info(f"Results saved to {s3_output_path}")

        # Show sample results
        logger.info("Sample results:")
        final_df.show(20, truncate=False)

        return final_df

    def get_processing_stats(self, df):
        """Get processing statistics"""
        return {
            'total_records': df.count(),
            'unique_entities': df.select('entity_text').distinct().count(),
            'entity_types': df.select('entity_label').distinct().collect(),
            'avg_paragraph_length': df.selectExpr('avg(length(paragraph_text))').collect()[0][0]
        }

    def stop(self):
        """Stop Spark session"""
        self.spark.stop()

def main():
    """Main execution function"""
    # Configuration
    S3_INPUT_PATH = "s3a://your-sec-filings-bucket/input/"
    S3_OUTPUT_PATH = "s3a://your-sec-filings-bucket/output/"

    # Initialize processor
    processor = SECFilingProcessor()

    try:
        # Process filings
        results_df = processor.process_sec_filings(S3_INPUT_PATH, S3_OUTPUT_PATH)

        # Get statistics
        stats = processor.get_processing_stats(results_df)
        print("\nProcessing Statistics:")
        for key, value in stats.items():
            print(f"{key}: {value}")

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise
    finally:
        processor.stop()

if __name__ == "__main__":
    main()
