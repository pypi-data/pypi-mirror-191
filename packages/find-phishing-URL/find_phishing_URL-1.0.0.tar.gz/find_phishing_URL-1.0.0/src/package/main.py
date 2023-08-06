import requests


def phishing_or_not(inp):
    """From API call, it will fetch required info.
    To check whether the URL is phishing URL or not

    Args:
        response : json file
    """
    try:
        response = requests.post(
            "https://checkurl.phishtank.com/checkurl/index.php",
            data={"url": inp, "format": "json"},
            verify=False)
        response = response.json()
        if (response["results"]["in_database"]):
            if (response["results"]["valid"]):
                return "no"
            else:
                return "yes"
        else:
            return "unknown"
    except Exception as e:
        print("\nError Occurred !!!\nDisplaying Error : ")
        print(e)
