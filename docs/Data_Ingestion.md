#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
# 📊 Data Ingestion Pipeline Spec (XAU)

This document describes the automated ingestion pipeline for Precious Metal (XAU Gold) rates.

## Scraper Execution (`get_gold_price.py`)
- Scheduled via Cron inside the backend container at `7,37 * * * *`.
- Scheduled via Airflow BashOperator at `22,52 * * * *`.
- Fetches pricing datasets from Spuerkeess API and stores them in JSON format.

## Loader Execution (`load_xau.py`)
- Scheduled via Cron inside the backend container at `10,40 * * * *`.
- Scheduled via Airflow BashOperator at `25,55 * * * *`.
- Automatically parses the latest JSON file, validates price ratios, and inserts records into the `Rate` database table.
