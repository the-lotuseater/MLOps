# NLP-TextSummarization-MLOps
An end to end text summarization nlp project

## TextSummarizer using Hugging Face model

# You may find the model research and setup in the text_summarization.ipynb file


### Here is the general workflow 

1. Config.yml
2. Params.yml
3. Config entity
4. Configuration Manager
5. Update the components - Data Ingestion Trainer
6. Create our pipeline - Trainging pipeline
7. Front end - APIs, Training APIs, Batch Prediction APIs


###
Step 1 Data Ingestion
Curl from remote data repo and save in artifacts. For this you need a config specifying where to download the data from, where to download it to and where to unzip it to.

Step 1 Data Transformation
Ingest downloaded data and transform it.