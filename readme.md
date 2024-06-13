# Project Workflow and Challenges Report

## Project Overview

This project involves automating data extraction, transformation, and storage using Apache Airflow, with data versioning handled by DVC and storage on Google Drive. The data sources include the homepages of `dawn.com` and `bbc.com`.

## Workflow

### 1. Data Extraction

- **Tools Used**: Python, requests, BeautifulSoup
- **Process**: Script extracts relevant HTML tags (paragraphs and headers) from the specified web pages.

### 2. Data Transformation

- **Tools Used**: Python, pandas
- **Process**: Cleans and formats the extracted text data by removing newlines and extra spaces, and organizes it into a structured CSV format.

### 3. Data Storage and Versioning

- **Tools Used**: Google Drive, DVC
- **Process**: The transformed data is uploaded to Google Drive and tracked using DVC, which also handles version control.

## Challenges Encountered

1. **Data Extraction Reliability**:
   - Challenge: Frequent changes in the HTML structure of the source websites caused the extraction scripts to fail.
   - Solution: Implemented more robust and flexible parsing logic that can handle variations in the website layouts.

2. **API Rate Limiting**:
   - Challenge: Initial implementations made too many requests to the source websites, hitting rate limits.
   - Solution: Added caching mechanisms and refined the frequency and timing of requests.

3. **DVC Integration with Airflow**:
   - Challenge: Integrating DVC commands directly into the Airflow DAG posed issues with environment and path configurations.
   - Solution: Created a separate script for DVC operations and called it from the Airflow task using system commands.

## Conclusion

This project showcased the powerful capabilities of automating complex workflows with Apache Airflow, alongside the robust data versioning features of DVC. Despite the challenges, the solutions implemented provided a reliable and scalable system for data processing tasks.
