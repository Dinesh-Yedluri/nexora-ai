def calculate_score(tool, relevance):
    """
    Calculate the NEXORA score.

    Higher score = better recommendation.
    """

    rating_score = (tool.get("rating", 0) / 5) * 30
    efficiency_score = (tool.get("efficiency", 0) / 10) * 25
    relevance_score = relevance * 45

    total_score = (
        rating_score
        + efficiency_score
        + relevance_score
    )

    return round(total_score, 2)


def rank_tools(tools, relevance_scores):
    """
    Rank tools from highest to lowest NEXORA score.
    """

    ranked_tools = []

    for tool in tools:

        relevance = relevance_scores.get(
            tool["name"],
            0
        )

        score = calculate_score(
            tool,
            relevance
        )

        tool_copy = tool.copy()
        tool_copy["overall_score"] = score

        ranked_tools.append(tool_copy)

    # Priority-style ranking:
    # highest score comes first
    ranked_tools.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )

    return ranked_tools