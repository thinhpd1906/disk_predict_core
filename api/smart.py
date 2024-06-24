import requests
import getpass
import json

def create_smart(token, data):
    url = "http://localhost:8080/api/v1/smart"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"insert smart data fail, please re sign in")
    except Exception as err:
        print(f"some thinh went wrong")
    return None

