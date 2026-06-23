from portfolio_recommendation import recommend_portfolio

portfolio = [
    {
        "stock": "RELIANCE.NS",
        "quantity": 100,
        "buy_price": 1500
    },
    {
        "stock": "TCS.NS",
        "quantity": 10,
        "buy_price": 3500
    }
]

print(recommend_portfolio(portfolio))

from sentiment_analysis import analyze_sentiment

print(
    analyze_sentiment(
        "Reliance stock is performing very well"
    )
)