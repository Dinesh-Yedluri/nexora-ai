import json
import random

with open("data/tools.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

for tool in tools:
    rating = tool.get("rating", 4.0)
    if rating >= 4.5:
        count = random.randint(8000, 50000)
    elif rating >= 4.0:
        count = random.randint(1000, 8000)
    else:
        count = random.randint(50, 1000)
    tool["reviews"] = count

with open("data/tools.json", "w", encoding="utf-8") as f:
    json.dump(tools, f, indent=2, ensure_ascii=False)

print("Done. reviews field added to", len(tools), "tools.")