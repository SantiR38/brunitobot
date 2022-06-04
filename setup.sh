#!/bin/bash

# Environment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
mkdir src/database/
python ./src/jw_news/models/migrations.py

# Running bot tasks
python ./src/brunito_bot.py
