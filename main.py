import requests
import json
import asyncio
import time
from auth import *
from initialization import *
import os




async def main():
    await volume_check()

if __name__ == "__main__":
    asyncio.run(main())