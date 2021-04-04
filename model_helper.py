from constants import NOT_EXIST_SENTIMENT, BAD_SENTIMENT, NEUTRAL_SENTIMENT, POSITIVE_SENTIMENT


def convert_sentiment_from_str(sentiment_str):
    if sentiment_str == "negative":
        return BAD_SENTIMENT
    if sentiment_str == "neutral":
        return NEUTRAL_SENTIMENT
    if sentiment_str == "positive":
        return POSITIVE_SENTIMENT

    return NOT_EXIST_SENTIMENT


def get_sentiment_from_aspect_score(score):
    if 0.5 <= score < 1.5:
        return BAD_SENTIMENT
    if 1.5 <= score < 2.5:
        return NEUTRAL_SENTIMENT
    if 2.5 <= score <= 3.5:
        return POSITIVE_SENTIMENT

    return NOT_EXIST_SENTIMENT
