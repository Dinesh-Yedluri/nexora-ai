# recommender.py

import difflib


# Map common words/synonyms to canonical keywords.
# Add more entries here anytime as you notice gaps.
SYNONYMS = {
    "ppt": ["presentation", "slides", "slide deck"],
    "presentation": ["ppt", "slides", "slide deck"],
    "slides": ["ppt", "presentation", "slide deck"],
    "video": ["movie", "clip", "footage"],
    "image": ["picture", "photo", "graphic", "visual"],
    "picture": ["image", "photo", "graphic"],
    "photo": ["image", "picture", "graphic"],
    "write": ["writing", "content", "text", "article"],
    "article": ["blog", "content", "write", "writing"],
    "code": ["coding", "programming", "developer"],
    "voice": ["audio", "speech", "voiceover"],
    "audio": ["voice", "sound", "music"],
    "design": ["graphic design", "graphics", "visual design"],
}


MIN_RESULTS = 10


def expand_query(query):
    """
    Expand the user query with synonym words,
    so 'slides' also matches tools tagged with 'ppt'.
    """
    words = query.split()
    expanded = set(words)

    for word in words:
        for synonym in SYNONYMS.get(word, []):
            expanded.add(synonym)

    return expanded


def fuzzy_contains(query, keyword, threshold=0.8):
    """
    Check if the keyword appears in the query,
    tolerating small typos using fuzzy matching.
    """
    if keyword in query:
        return True

    words = query.split()

    for word in words:
        similarity = difflib.SequenceMatcher(
            None, word, keyword
        ).ratio()

        if similarity >= threshold:
            return True

    return False


def recommend_tools(user_query, tools, min_results=MIN_RESULTS):
    """
    Recommend AI tools based on the user's query.
    Returns a list of (tool, relevance) tuples,
    where relevance is a value between 0 and 1.

    Always returns at least `min_results` tools when available,
    filling remaining slots with other tools at low relevance
    so the user always sees a good number of options.
    """

    query = user_query.lower()
    expanded_words = expand_query(query)
    expanded_query = query + " " + " ".join(expanded_words)

    matched = []
    matched_names = set()

    for tool in tools:
        score = 0
        max_score = 0

        # Check keywords / use_cases (with synonyms + fuzzy match)
        for keyword in tool.get("use_cases", []):
            max_score += 2
            keyword_lower = keyword.lower()

            if fuzzy_contains(expanded_query, keyword_lower):
                score += 2

        # Check category (with fuzzy match too)
        max_score += 1
        category = tool.get("category", "").lower()

        if category and fuzzy_contains(expanded_query, category):
            score += 1

        if score > 0:
            relevance = score / max_score if max_score > 0 else 0
            matched.append((tool, relevance))
            matched_names.add(tool["name"])

    # Highest relevance first
    matched.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # If we don't have enough matches, fill remaining slots
    # with the best of the leftover tools (low relevance).
    if len(matched) < min_results:
        leftover = [
            tool for tool in tools
            if tool["name"] not in matched_names
        ]

        # Best leftover tools first, by rating + efficiency
        leftover.sort(
            key=lambda t: (
                t.get("rating", 0) + t.get("efficiency", 0)
            ),
            reverse=True
        )

        needed = min_results - len(matched)

        for tool in leftover[:needed]:
            matched.append((tool, 0.05))

    return matched