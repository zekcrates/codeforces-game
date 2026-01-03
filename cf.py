import requests

USER_INFO_URL = "https://codeforces.com/api/user.info?handles="

CHECK_SOLUTION_URL = "https://codeforces.com/api/user.status?handle=Fefer_Ivan&from=1&count=3"
def user_exists(handle):
    response = requests.get(USER_INFO_URL + handle)
    data = response.json()

    return data["status"] == "OK"


def check_solution(handle, problem_index, contest_id):
    """
    Checks if the user has an accepted submission for the problem.
    Stops checking as soon as one is found.
    """
    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=10"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return False

    for submission in data["result"]:
        problem = submission["problem"]
        verdict = submission.get("verdict")

        if problem["contestId"] == contest_id and problem["index"] == problem_index:
            if verdict == "OK":
                return True  

    return False
