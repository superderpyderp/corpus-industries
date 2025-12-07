from auth import *
import requests

BASE_URL = "https://api.warframe.market/v2/"
async def place_order(id: str,  jwt: str, type: str, plat: int = 1):
    session = requests.Session()
    body = {
        "itemId":id,
        "type":type,
        "platinum":plat,
        "quantity":1,
        "visible":False
    }
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {jwt}"
        }
    url = f"{BASE_URL}order"
    request = session.post(url, json=body, headers=headers)
    print(request.json())


    