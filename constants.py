# Config
QUERY_RETURN_SIZE = 10
INDEX_NAME = "reviews"
DATA_DIR_NAME = "data"
RESTAURANT_DB_PATH = "./{}/restaurant_db.json".format(DATA_DIR_NAME)

# Sentiment model
SENTIMENT_MODEL_URL = 'http://127.0.0.1:8000/predict'
NOT_EXIST_SENTIMENT = 0
BAD_SENTIMENT = 1
NEUTRAL_SENTIMENT = 2
POSITIVE_SENTIMENT = 3

# Elastic Search Constants
AND_OPERATOR = "and"
OR_OPERATOR = "or"
AUTO_FUZZY = "AUTO"
HIGHLIGHT_PRE_TAG = "<strong>"
HIGHLIGHT_POST_TAG = "</strong>"

# Suggester
SUGGEST_PRE_TAG = "<strong>"
SUGGEST_POST_TAG = "</strong>"

# Sentiment Analysis
SENTIMENT_BAD = 0
SENTIMENT_NEUTRAL = 1
SENTIMENT_POSTIVE = 2
