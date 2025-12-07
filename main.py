import requests
import json
import asyncio
import time
from auth import *
from initialization import *
import os
from orders import *


JWT = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJNM09pREpoVmdVcllqZHRjY0NoSnR3ZDIzSEt5b1dVTSIsImNzcmZfdG9rZW4iOiJmNjFlYzY3YzU0OTA1ZjNlZjlkMzhhNmU0NGI1YmM0Y2YxYWZiZGMwIiwiZXhwIjoxNzcwMzMxNjA0LCJpYXQiOjE3NjUxNDc2MDQsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6dHJ1ZSwiand0X2lkZW50aXR5IjoicFhHRjZoZHFmbHo2T1lUYzh1SWhUOXk2NGlyTjVGSHQiLCJsb2dpbl91YSI6ImInTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6MTQ1LjApIEdlY2tvLzIwMTAwMTAxIEZpcmVmb3gvMTQ1LjAnIiwibG9naW5faXAiOiJiJzUuMTUxLjEzMy4xMzEnIn0.3oWytFZwGnmQsdFYJsdTuUTwB2bLuPy9et48HkT3Bsc"


async def main():
    data = load_json("data.json")["data"]
    for item in data:
        await place_order(item["id"],JWT,"sell")

if __name__ == "__main__":
    asyncio.run(main())