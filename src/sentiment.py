from textblob import TextBlob

news = [
    "Reliance Industries reports strong quarterly earnings",
    "Reliance stock gains after positive market outlook",
    "Analysts expect revenue growth in coming quarters"
]

score = 0

for article in news:
    polarity = TextBlob(article).sentiment.polarity
    score += polarity

avg_score = score / len(news)

print("Sentiment Score:", round(avg_score, 2))

if avg_score > 0:
    print("Positive Sentiment")
elif avg_score < 0:
    print("Negative Sentiment")
else:
    print("Neutral Sentiment")