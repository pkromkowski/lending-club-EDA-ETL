# Lending Club EDA & ETL

This repository is dedicated to the accepted loans dataset from LendingClub, sourced from [Kaggle](https://www.kaggle.com/wordsforthewise/lending-club). Exploratory data analysis was performed to analyze and find the top 20 features in the dataset. This was then used to build a fully automated ETL pipeline. 

### The Data

LendingClub was an American peer-to-peer lending company, headquartered in San Francisco, California. It was the first peer-to-peer lender to register its offerings as securities with the Securities and Exchange Commission, and to offer loan trading on a secondary market. The data set is comprised of loans that were accepted on LendingClub's platform from 2017 to 2018 Q4. The data is point-in-time and offers the current status of the loan, recent history, and initial application data. 

## Exploratory Data Analysis

 - Data Clean & EDA
   - Data_Clean.ipynb (Data Cleaning)
   - Data_EDA.ipynb (Data Analysis)

When data has too many features it can become hard to analyze and get a general understanding. Trends are unrecognizable and the daunting task of figuring out what lies between the rows can become overwhelming. Further down the process, too many features can also negatively affect the way our model develops. This part of the project aimed to reduce the feature space of the data by identifying the top 20 most helpful features. 

During cleaning, steps were taken to fix the irregularities without making any assumptions about what the clean data should be used for. At the same time, cleaning focused on formatting all of the features to the best possible representation of their data. This mainly involved changing the data type of columns.

During the Data Analysis phase, correlation testing, class imbalance, variance threshold testing, and density differences among the feature space were carried out to identify features that were providing very little or duplicated information. The hardest part of this step was, that even though the tests and ideas were very similar, the analysis that had to be done on each set of data type features (objects, numeric, datetime) had to be carried out separately and uniquely for that datatype. 

This resulting smaller dataset saves on storage space, query times, and aggregation functions. But most importantly, it reduces a lot of noise that was initially present so that clear patterns and relationships can be extracted to support model development and hypothesis formation. 

It is clear that this may not be the best dataset for every problem. Some problems may need the removal of columns that contain information that is in the future of what they are trying to predict. Other problems may be focused on just one part of the application process, such as secondary applicant statistics. But this process can be used to reduce the feature space for any problem and give the modeler a sense of how strong the subset of data they are working on is. 

With more time, a specific purpose statement, and a client's goal in mind, analysis of all columns should be completed. In the future, proper vetting should include studying look ahead bias, correcting data imputations errors, analyzing selection bias, and outlier detection.  

## Extract, Transform, & Loud Pipeline

- Data ETL 
  - main.py (run python main.py --yaml 'config.yaml' --demo ON)
    - config.yaml
    - data_extraction.py
    - data_transformation.py
    - manage_db.py
  - requirements.txt
  - Data ("on prem" data warehouse")
   
A fully automated data pipeline was built using sqlite3 as the database. This was chosen to increase the reproducibility of this project and due to the simplicity of navigating sqlite3. The data is not nearly large enough to create any problems or efficiency issues for a considerable amount of the pipeline's life. But if it were to grow and be used in production it would be best to eventually transfer the data to a cloud-based database and the raw files that are saved to a bucketed file warehouse, such as s3, so that a collaborative environment is created to give many people access to the cleaned data. 

The pipeline is comprised of three steps that makes sure the data is ready to be queried and analyzed at the end of the process. Most of the specifics of the pipeline are controlled by the config.yaml file and can be easily altered to fit the needs of data management.

 - Extraction: the data is pulled from Kaggle, LendingClub API, or local source (after being downloaded from Kaggle).
 - Transformation: the data is formatted and cleaned according to what was discovered during EDA. The fully cleaned data is saved as a pkl file and the data is split into a "top 20 features" dataset and a dataset containing the rest of the features. 
 - Load: Each dataset is loaded into the database separately. Data management has an option to control what data is kept after every pull (only unique values, everything, or just the new information). 
 
Currently, the pipeline is scheduled and automated using scheduler. A production implementation of this pipeline should utilize a more robust product such as Airflow, an open-source workflow management platform, initially designed by Airbnb, to automate and track the many tasks required to complete the pipeline.

In the future, regression tests and model performance tracking should be carried out to make sure the pipeline is still performing as needed. 
