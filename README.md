# ChatDB: DSCI 551 Project

## Environment and Requirements
- Python: 3.12.7
- MySQL: 8.4.3
- MongoDB: 8.0.8
- MongoSh: 2.5.0
- Python Packages: See Requirements

## Install Requirements
Open Windows Powershell
```bash
pip install -r requirements.txt --upgrade
```
Install MySQL and MongoDB

## Dataset
[Kaggle - Gaming Profile 2025](https://www.kaggle.com/datasets/artyomkruglov/gaming-profiles-2025-steam-playstation-xbox)

1. Run `datasets/get_dataset.py` to get datasets
2. Move the datasets folders into /datasets
3. Run `/database/mysql_init.sql` to create MySQL tables
4. Run `/database/mysql_import_data.py` and `/database/mongodb_import_data.py` to import data into MySQL and MongoDB

## Database
- **MySQL**: PlayStation: Games, Achievements, Prices
- **MongoDB**: Steam: Games, Players, Reviews
- Database configs are in `/database/db_config.py`, change to your own database config 

## LLM
Put your API Key in `/llm/llm_config.py`, we use **DeepSeek-V3** and **Gemini-2.0-Flash-Lite** in our code as example

## Run Project
After installing all requirements and databases, downloading datasets and importing data, setting LLM API Key

Start ChatDB by running `main.py`

## TODO
1. User Permission and Authentication
2. Redis as Query Result Cache
3. Backend and Frontend
4. MultiThread Implementation
5. Prompt Evaluation and Improvement

## Task Completed
1. SQL & MQL Result to Text
2. Create, Read, Update, Delete
3. Multi DB Aggregation by Classifier
4. Data Cleansing
5. Prompt Generation