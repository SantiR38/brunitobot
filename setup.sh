#!/bin/bash

# Environment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
python ./src/jw_news/models/migrations.py

# Running bot tasks
cd src
nohup python brunito_bot.py &
