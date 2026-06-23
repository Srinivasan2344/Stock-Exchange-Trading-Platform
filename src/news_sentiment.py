from newsapi import NewsApiClient
from textblob import TextBlob

API_KEY = "0d595a249f21494994cb13a28a83318f"

newsapi = NewsApiClient(
    api_key=API_KEY
)

def analyze_stock_news(company):

    news = newsapi.get_everything(
        q=company,
        language="en",
        sort_by="publishedAt",
        page_size=10
    )

    sentiments = []

    for article in news["articles"]:

        title = article["title"]

        score = (
            TextBlob(title)
            .sentiment
            .polarity
        )

        sentiments.append(score)

    if len(sentiments) == 0:

        return {
            "company": company,
            "sentiment": "No News"
        }

    avg_score = (
        sum(sentiments)
        / len(sentiments)
    )

    if avg_score > 0:

        sentiment = "Positive"

    elif avg_score < 0:

        sentiment = "Negative"

    else:

        sentiment = "Neutral"

    return {
        "company": company,
        "sentiment": sentiment,
        "score": round(avg_score, 2)
    }