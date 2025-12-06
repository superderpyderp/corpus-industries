import requests
import json

def login(user_email: str, user_password: str, platform: str = "pc", language: str = "en"):
    headers = {
        "Content-Type": "application/json; utf-8",
        "Accept": "application/json",
        "Authorization": "JWT",
        "platform": platform,
        "language": language,
    }
    content = {"email": user_email, "password": user_password, "auth_type": "header"}
    response = requests.post("https://api.warframe.market/v1/auth/signin", data=json.dumps(content), headers=headers)
    if response.status_code != 200:
        return None, None
    return (response.json()["payload"]["user"]["ingame_name"], response.headers["Authorization"])


def main():
    if __name__ == "__main__.py":
        pass
main()
