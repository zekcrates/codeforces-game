import requests

USER_INFO_URL = "https://codeforces.com/api/user.info?handles="

def user_exists(handle):
    response = requests.get(USER_INFO_URL + handle)
    data = response.json()

    return data["status"] == "OK"


def check_solution(username, problem_name):
    pass 

    