# Tawasol
TAWASOL is a dashboard that continuously tracks different social media channels in order to capture any relevant feedback related to the public transportation system and events in Qatar. Given the unique multinational and multicultural nature of Qatar residents, TAWASOL will support all major spoken languages in the world, with a special emphasis on the ones used in Qatar such as Arabic, Urdu, Tagalog, Baloshi as well as some regional dialects.

# Deployment
1. Create virtualenv: `virtualenv venv`
2. Start it: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run Frontend: `sh start_tawasol_website_gunicorn.sh`
5. Run Backend: `python run_twitter_crawler.py`

### Observation:
We need to install nltk: `pip install nltk`
then, start python and type:
`import nltk
nltk.download('stopwords')`