import requests
import json
import asyncio
import time
import os
import math

BASE_URL = "https://api.warframe.market/v2/"

def save_json(data: json, path: str):
    with open(path, "w") as file:
       json.dump(data, file, indent=4)   

def load_json(path: str):
    with open(path, "r") as file:
       return json.load(file)

async def CreatingCache():
    print("this Ran")
    tags = ["arcane_enhancement","rare","mod","prime","set","blueprint","weapon","augment","legendary"]
    Chosen_list = {}
    url= BASE_URL +"items"
    response =  requests.get(url)
    data = response.json()["data"]
    for Item in data:
        for tag in Item["tags"]:
            if tag in tags:
                if not(Item["slug"] in Chosen_list):
                    Chosen_list[Item["slug"]]= data.index(Item)     
                    break
    return Chosen_list

async def volume_check():
    Chosen_List = await CreatingCache()
    session = requests.Session()
    filtered_list = {}
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
            filtered_list[Chosen_Item] = Chosen_List[Chosen_Item]
            save_json(filtered_list,"flipable_items.json")
            continue
        
    session.close() 
    return filtered_list



async def PlatStats():
    FlipableList = load_json("flipable_items.json")
    FullList = load_json("data.json")["data"]
    
    InfoList = {}
    session = requests.Session()
    url = BASE_URL + "orders/item/" 
    for Item in FlipableList:
        result = next((item for item in FullList if item.get("slug") == Item), None)
        if result.get("maxRank") != None:
            response = session.get(f"{url}{Item}/top?rank={result.get("maxRank")}")
            response = Rate_check(f"{url}{Item}/top?rank={result.get("maxRank")}", response, session)
        else:
            response = session.get(f"{url}{Item}/top")
            response = Rate_check(f"{url}{Item}/top", response, session)
        
        Item_Orders = response.json()["data"]
        if len(Item_Orders["buy"]) == 0 or len(Item_Orders["sell"]) == 0:
            continue
        
        MinPlatSale = Item_Orders["sell"][0]["platinum"]
        MinPlatBuy = Item_Orders["buy"][0]["platinum"]
        MinProfitMargin = MinPlatSale - MinPlatBuy
        AvgPlatSale = math.floor(sum_of_orders(Item_Orders,"sell")/len(Item_Orders["sell"]))
        AvgPlatBuy = math.floor(sum_of_orders(Item_Orders,"buy")/len(Item_Orders["buy"]))
        AvgPlatProfit = AvgPlatSale-AvgPlatBuy

        InfoList[Item] = {}
        InfoList[Item]["Id"] = FullList[FlipableList[Item]]["id"] 
        InfoList[Item]["PlatStats"] = {
            "MinPlatBuy":MinPlatBuy,
            "MinPlatSale":MinPlatSale, 
            "MinProfitMargin":MinProfitMargin, 
            "AvgPlatBuy": AvgPlatBuy, 
            "AvgPlatSale": AvgPlatSale, 
            "AvgProfitMargin": AvgPlatProfit
            }
        InfoList[Item]["Tags"] = {"Tags": FullList[FlipableList[Item]]["tags"]}
            
        save_json(InfoList,"plat_stats.json")
    session.close()
    return InfoList

def sum_of_orders(item_orders: str, order_type: str) -> int:
    return sum(item_orders[order_type][order]["platinum"] for order in range(len(item_orders[order_type])))

def Rate_check(url: str,response: requests.Response, session : requests.Session) -> requests.Response:
    while response.status_code != 200:
        response = session.get(url)
        print("get yo ahh rated")
        time.sleep(0.2)
    return response





async def main():
    if __name__ == "__main__":
        pass
asyncio.run(main())




