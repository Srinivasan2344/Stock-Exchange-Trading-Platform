def recommend_portfolio(portfolio):

    recommendations = []

    total = sum(
        stock["quantity"] * stock["buy_price"]
        for stock in portfolio
    )

    if total == 0:
        return ["No portfolio data found"]

    for stock in portfolio:

        allocation = (
            stock["quantity"]
            * stock["buy_price"]
        ) / total * 100

        if allocation > 50:
            recommendations.append(
                f"Reduce exposure to {stock['stock']}"
            )

    if not recommendations:
        recommendations.append(
            "Portfolio is well diversified"
        )

    return recommendations