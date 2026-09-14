import json

with open("data/tools.json", "r", encoding="utf-8") as f:
    tools = json.load(f)

missing_use_cases = [t["name"] for t in tools if not t.get("use_cases")]
missing_category = [t["name"] for t in tools if not t.get("category")]
missing_rating = [t["name"] for t in tools if "rating" not in t]

print("Total tools:", len(tools))
print("Missing use_cases:", missing_use_cases)
print("Missing category:", missing_category)
print("Missing rating:", missing_rating)