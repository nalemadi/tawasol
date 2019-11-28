from tawasol_reporter import TawasolReporter
from __init__ import tweets_collections_dict, users, REDIS_DB, results_channels

# Tawasol Analyzer
tawasol_analyzer_worker = TawasolReporter(tweets_collections_dict, users, REDIS_DB, results_channels)
tawasol_analyzer_worker.start()
