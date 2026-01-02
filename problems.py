import random
import requests
import json

BASE_URL = "https://codeforces.com/api/problemset.problems?tags=dp"

# try:
#     response = requests.get(BASE_URL)
#     response.raise_for_status()
#     data = response.json()

#     problems = data["result"]["problems"]

#     filtered_problems = [
#         {
#             "contestId": p["contestId"],
#             "index": p["index"],
#             "name": p["name"],
#             "rating": p["rating"]
#         }
#         for p in problems
#         if "rating" in p
#     ]

#     with open("data/dp_problems.json", "w", encoding="utf-8") as f:
#         json.dump(filtered_problems, f, indent=2, ensure_ascii=False)

#     print(f"Saved {len(filtered_problems)} problems with ratings to dp_problems.json")

# except requests.exceptions.RequestException as e:
#     print(f"Request error: {e}")
# except KeyError as e:
#     print(f"Unexpected response format: missing {e}")



import json
import random

def get_problem(ratings=[1100,1300]):
    """
    ratings: list of player ratings, e.g., [1100, 1200]
    Returns a problem whose rating is the smallest available rating 
    that is >= average rating (i.e., slightly harder than average).
    """
    if not ratings:
        return None

    avg_rating = sum(ratings) / len(ratings)

    with open('data/dp_problems.json', 'r', encoding='utf-8') as f:
        problems = json.load(f)

    available_ratings = sorted({p["rating"] for p in problems})

    higher_ratings = [r for r in available_ratings if r >= avg_rating]
    if higher_ratings:
        chosen_rating = min(higher_ratings)
    else:
        chosen_rating = max(available_ratings)

    filtered = [p for p in problems if p["rating"] == chosen_rating]

    return random.choice(filtered) if filtered else None


problem = get_problem([1100,1300])
print(problem)