virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

python ./src/jw_news/models/migrations.py
