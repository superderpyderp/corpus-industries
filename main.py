import requests
import json
import asyncio
import firebase_admin
from firebase_admin import credentials, app_check

app = firebase_admin.initialize_app(credential=None, options=None, name='Corpus Industries')

def save_json(data: json, path: str):
    with open(path, "w") as file:
       json.dump(data, file, indent=4)   

def load_json(path: str):
    with open(path, "r") as file:
        return json.load(file)

BASE_URL = "https://api.warframe.market/v2/"

async def get_auth_tokens() -> dict:
    url = BASE_URL + "/oauth/authorize"
    body = {
    }
    headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJSdjNDaHh0bHR4bDhSOTA1eWM4ZUk4YWdkM0UyWWJ3UyIsImNzcmZfdG9rZW4iOiJhYTZhYzM2OTNiNzFjODExMWM4Yzk4NWVlNmZkN2ZhZDhjNzdiZDk4IiwiZXhwIjoxNzcwMDY5NzMxLCJpYXQiOjE3NjQ4ODU3MzEsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6ZmFsc2UsImxvZ2luX3VhIjoiYidNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjoxNDUuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8xNDUuMCciLCJsb2dpbl9pcCI6ImInNS4xNTEuMTMzLjEzMSciLCJqd3RfaWRlbnRpdHkiOiJZTFc3aXhkRUlua2pZNjEwNGZtQUJaU1pYZE9CVm9OaCJ9.3QiLsMK-wt85iL_O_qcrpCwu1BcZ36oaNJ15-xfzjgE"}
    response = requests.post(url, json=body, headers=headers)
    print(response.json())

async def place_order():
    url = BASE_URL + "order"
    body = {
	"itemId": "54aae292e7798909064f1575",
	"type": "sell",
	"platinum": 2,
	"quantity": 12,
	"visible": True,
	"perTrade": 6,
	"rank": 5,
	"charges": 3,
	"subtype": "blueprint",
    }
    headers = {"Content-Type":"application/json","Platform":"pc","Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJSdjNDaHh0bHR4bDhSOTA1eWM4ZUk4YWdkM0UyWWJ3UyIsImNzcmZfdG9rZW4iOiJhYTZhYzM2OTNiNzFjODExMWM4Yzk4NWVlNmZkN2ZhZDhjNzdiZDk4IiwiZXhwIjoxNzcwMDY5NzMxLCJpYXQiOjE3NjQ4ODU3MzEsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6ZmFsc2UsImxvZ2luX3VhIjoiYidNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0OyBydjoxNDUuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC8xNDUuMCciLCJsb2dpbl9pcCI6ImInNS4xNTEuMTMzLjEzMSciLCJqd3RfaWRlbnRpdHkiOiJZTFc3aXhkRUlua2pZNjEwNGZtQUJaU1pYZE9CVm9OaCJ9.3QiLsMK-wt85iL_O_qcrpCwu1BcZ36oaNJ15-xfzjgE"}
    response = requests.post(url, body, headers=headers)
    print(response.json())


async def CreatingCache():
    tags = ["arcane_enhancement","rare","mod","prime","set","blueprint","weapon","augment","legendary"]
    Chosen_list = []
    url= BASE_URL +"items"
    response =  requests.get(url)
    data = response.json()["data"]
    for a in data:
        for tag in a["tags"]:
            if tag in tags:
                # if not(a["slug"] in Chosen_list):
                    Chosen_list.append(a["slug"])        
                    break
    Chosen_list.append(len(Chosen_list))
    return Chosen_list




async def main():
    if __name__ == "__main__":
        await place_order()
        sigmas = await CreatingCache()
        print(sigmas)
asyncio.run(main())