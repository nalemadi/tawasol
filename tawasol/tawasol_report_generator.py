from app.data_analyzer.tawasol_analyzer import TawasolAnalyzer
from app import tweets_collection, users, REDIS_DB, results_channels


# Tawasol Analyzer
tawasol_analyzer_worker = TawasolAnalyzer(tweets_collection, users, REDIS_DB, results_channels)
tawasol_analyzer_worker.start()
