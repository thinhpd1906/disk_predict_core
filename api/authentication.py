import requests
import getpass
import json

class Authentication:
    def authenticate(self, username, password):
        url = "http://localhost:8080/api/v1/auth/authenticate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": username,
            "password": password
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.exceptions.HTTPError as err:
            print(f"email or password is incorrect")
        except Exception as err:
            print(f"some thinh went wrong")
        return None


    def get_user_credentials(self):
        username = input("Enter email: ")
        password = getpass.getpass("Enter password: ")
        return username, password