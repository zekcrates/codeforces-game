import math

K = 16

def get_correct_k():
    pass 

def calculate_ratings(p1_rating, p1_score, p2_rating, p2_score):
    p1_expected = 1 / (1 + math.pow(10, (p2_rating - p1_rating) / 400))
    p2_expected = 1 / (1 + math.pow(10, (p1_rating - p2_rating) / 400))

    p1_new = p1_rating + K * (p1_score - p1_expected)
    p2_new = p2_rating + K * (p2_score - p2_expected)

    return int(p1_new), int(p2_new)

