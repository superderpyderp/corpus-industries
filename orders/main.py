from auth import *
import requests

BASE_URL = "https://api.warframe.market/v2/"

async def place_order(slug: str,  jwt: str, plat: int = 1):
    session = requests.Session()
    body = {
        
    }
    session.post()

    