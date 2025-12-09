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

async def grab_market_database():
    url= f"{BASE_URL}items"
    response =  requests.get(url)
    data: list[dict] = response.json()["data"]
    save_json(data,"market_database.json")

async def create_cache():
    tags = ["arcane_enhancement","rare","mod","prime","set","blueprint","weapon","augment","legendary"]
    chosenList = {}
    market_database: list[dict] = load_json("market_database.json")
    for item in market_database:
        if any(tag in tags for tag in item["tags"]) and item["slug"] not in chosenList:
            chosenList[item["slug"]]= market_database.index(item)  
            continue
    print("Cache created")
    save_json(chosenList,"items_of_interest.json")

async def volume_check(orderType: list = ["buy","sell"]):
    chosenList = load_json("items_of_interest.json")
    session = requests.Session()
    useableItems = {}
    orderThresholds = {
            "buy":3,"sell":5
            }
    for chosenItem in chosenList:
        url = f"{BASE_URL}orders/item/{chosenItem}"
        response = rate_check(url, session)
        itemData = response.json()["data"]
        passed = True
        ingameOrders = [order for order in itemData if order["user"]["status"] == "ingame"]
        for t in orderType:
            count = sum(1 for order in ingameOrders if order["type"] == t)
            if count < orderThresholds[t]:
                passed = False
                break
        if passed:
            useableItems[chosenItem] = chosenList[chosenItem]
    save_json(useableItems, "useable_items.json")
    session.close()
    print("useable list complete")
    return useableItems

        
async def plat_stats_for_useables():
    useableList = load_json("useable_items.json")
    marketDatabase = load_json("market_database.json")
    infoList = {}
    session = requests.Session()
    url = f"{BASE_URL}orders/item/"
    for item in useableList:
        result: dict = next((entry for entry in marketDatabase if entry["slug"] == item), None)
        if result.get("maxRank") != None:
            response = rate_check(f"{url}{item}/top?rank={result.get("maxRank")}", session)
        else: 
            response = rate_check(f"{url}{item}/top", session)
        itemOrders = response.json()["data"]
        if len(itemOrders["buy"]) == 0 or len(itemOrders["sell"]) == 0:
            continue

        MinPlatSale = itemOrders["sell"][0]["platinum"]
        MaxPlatBuy = itemOrders["buy"][0]["platinum"]
        MinProfitMargin = MinPlatSale - MaxPlatBuy

        AvgPlatSale = math.floor(sum_of_orders(itemOrders,"sell")/len(itemOrders["sell"]))
        AvgPlatBuy = math.floor(sum_of_orders(itemOrders,"buy")/len(itemOrders["buy"]))
        AvgPlatProfit = AvgPlatSale-AvgPlatBuy

        infoList[item] = {}
        itemSlug = useableList[item]
        infoList[item]["id"] = marketDatabase[itemSlug]["id"] 
        infoList[item]["plat_stats"] = {
            "min_plat_buy":MaxPlatBuy,
            "min_plat_sale":MinPlatSale, 
            "min_profit_margin":MinProfitMargin, 
            "avg_plat_buy": AvgPlatBuy, 
            "avg_plat_sale": AvgPlatSale, 
            "avg_profit_margin": AvgPlatProfit
            }
        infoList[item]["tags"] = [marketDatabase[itemSlug]["tags"]]
        print(f"calculated for {item}")
        save_json(infoList,"plat_stats.json")
    session.close()
    return infoList


# async def plat_stats():
#     FlipableList = await volume_check()
#     FullList = load_json("data.json")["data"]
#     InfoList = {}
#     session = requests.Session()
#     url = BASE_URL + "orders/item/" 
#     for Item in FlipableList:
#         result = next((item for item in FullList if item.get("slug") == Item), None)
#         if result.get("maxRank") != None:
#             response = session.get(f"{url}{Item}/top?rank={result.get("maxRank")}")
#             response = Rate_check(f"{url}{Item}/top?rank={result.get("maxRank")}", response, session)
#         else:
#             response = session.get(f"{url}{Item}/top")
#             response = Rate_check(f"{url}{Item}/top", response, session)
        
#         Item_Orders = response.json()["data"]
#         if len(Item_Orders["buy"]) == 0 or len(Item_Orders["sell"]) == 0:
#             continue
        
#         MinPlatSale = Item_Orders["sell"][0]["platinum"]
#         MinPlatBuy = Item_Orders["buy"][0]["platinum"]
#         MinProfitMargin = MinPlatSale - MinPlatBuy
#         AvgPlatSale = math.floor(sum_of_orders(Item_Orders,"sell")/len(Item_Orders["sell"]))
#         AvgPlatBuy = math.floor(sum_of_orders(Item_Orders,"buy")/len(Item_Orders["buy"]))
#         AvgPlatProfit = AvgPlatSale-AvgPlatBuy

#         InfoList[Item] = {}
#         InfoList[Item]["Id"] = FullList[FlipableList[Item]]["id"] 
#         InfoList[Item]["PlatStats"] = {
#             "MinPlatBuy":MinPlatBuy,
#             "MinPlatSale":MinPlatSale, 
#             "MinProfitMargin":MinProfitMargin, 
#             "AvgPlatBuy": AvgPlatBuy, 
#             "AvgPlatSale": AvgPlatSale, 
#             "AvgProfitMargin": AvgPlatProfit
#             }
#         InfoList[Item]["Tags"] = [FullList[FlipableList[Item]]["tags"]]
            
#         save_json(InfoList,"plat_stats.json")
#     session.close()
#     return InfoList

async def sort_plat_stats(Dict:dict ) -> list:
    if len(Dict) <= 1:
        return Dict
    def checkValue(ItemData:dict):
        return ItemData["plat_stats"]["min_profit_margin"]
    Lower_Sorting_Dict = {}
    Upper_Sorting_Dict = {}
    Pivot_Sorting_Dict = {}
    PivotKey = list(Dict.keys())[int((len(Dict)/2))]
    pivot = checkValue(Dict[PivotKey])
    # Lower_Sorting_List = [{Key: Values} for Key, Values in Dict if checkValue(Dict[Key])  < pivot]
    # Upper_Sorting_List = [{Key: Values} for Key,Values in Dict if checkValue(Dict[Key])  > pivot]
    # Equal_Sorting_List= [{Key: Values} for Key,Values in Dict if checkValue(Dict[Key])  == pivot]
    
    
    # Fix code, change everything to a dict
    for Key in Dict:
        if(checkValue(Dict[Key])< pivot):
            Upper_Sorting_Dict[Key] = Dict[Key]
        elif (checkValue(Dict[Key])>pivot):
            Lower_Sorting_Dict[Key]= Dict[Key]
        else:
            Pivot_Sorting_Dict[Key] = Dict[Key]
    
    
    return {**await sort_plat_stats(Lower_Sorting_Dict), **Pivot_Sorting_Dict, **await sort_plat_stats(Upper_Sorting_Dict)}
    
    


def sum_of_orders(item_orders: str, order_type: str) -> int:
    return sum(item_orders[order_type][order]["platinum"] for order in range(len(item_orders[order_type])))

def rate_check(url: str, session : requests.Session) -> requests.Response:
    response = session.get(url)
    while response.status_code != 200:
        response = session.get(url)
        time.sleep(0.2)
    return response





async def main():
    if __name__ == "__main__":
        pass
asyncio.run(main())




