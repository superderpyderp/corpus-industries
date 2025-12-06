import requests
import json
import asyncio
import time
import os

BASE_URL = "https://api.warframe.market/v2/"

def save_json(data: json, path: str):
    with open(path, "w") as file:
       json.dump(data, file, indent=4)   

def load_json(path: str):
    with open(path, "r") as file:
       return json.load(file)

async def CreatingCache():
    tags = ["arcane_enhancement","rare","mod","prime","set","blueprint","weapon","augment","legendary"]
    Chosen_list = []
    url= BASE_URL +"items"
    response =  requests.get(url)
    data = response.json()["data"]
    for a in data:
        for tag in a["tags"]:
            if tag in tags:
                if not(a["slug"] in Chosen_list):
                    Chosen_list.append(a["slug"])        
                    break
    return Chosen_list

async def volume_check():
    Chosen_List = await CreatingCache()
    session = requests.Session()
    filtered_list = []
    for Chosen_Item in Chosen_List:
        # Avoiding rate limits
        url = BASE_URL + "orders/item/" + Chosen_Item
        response = session.get(url)
        while response.status_code != 200:
            response = session.get(url)
            time.sleep(0.2)
        data = response.json()["data"]
        ingame_orders = [Order for Order in data if Order["user"]["status"] == "ingame"]
        if sum(1 for Order in ingame_orders if Order["type"] == "buy") >= 3 and sum(1 for Order in ingame_orders if Order["type"] == "sell") >= 5:
            filtered_list.append(Chosen_Item)
            save_json(filtered_list,"flipable_items.json")
            continue
    session.close() 
    return filtered_list

async def PlatStats():
    FlipableList = load_json("flipable_items.json")
    InfoList = {}
    session = requests.Session()
    url = BASE_URL + "orders/item/" 
    for Item in FlipableList:
        response = session.get(url+Item+"/top")
        while response.status_code != 200:
            response = session.get(url+Item+"/top")
            time.sleep(0.2)
        data = response.json()["data"]
        MinPlatSale = data["sell"][0]["platinum"]
        MinPlatBuy = data["buy"][0]["platinum"]
        MinProfitMargin = MinPlatSale - MinPlatBuy
        AvgPlatSale = sum(data["sell"][order]["platinum"] for order in range(len(data["sell"])))/len(data["sell"])
        AvgPlatBuy = sum(data["buy"][order]["platinum"] for order in range(len(data["buy"])))/len(data["buy"])
        AvgPlatProfit = AvgPlatSale-AvgPlatBuy
        InfoList[Item] = {}
        InfoList[Item]["PlatStats"] = {"MinPlatBuy":MinPlatBuy,"MinPlatSale":MinPlatSale, "MinProfitMargin":MinProfitMargin, "AvgPlatBuy": AvgPlatBuy, "AvgPlatSale": AvgPlatSale, "AvgProfitMargin": AvgPlatProfit}
        save_json(InfoList,"plat_stats.json")
    session.close()
    return InfoList

async def main():
    if __name__ == "__main__":
        pass
asyncio.run(main())




