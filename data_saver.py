import os

from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,3000")

path = os.path.join(os.getcwd(), 'api_userdata', f"account")
options.add_argument(f'--user-data-dir={path}')
options._auto_clean_dirs = False

async def main():
    async with webdriver.Chrome(options=options) as dr:
        await dr.get("https://www.linkedin.com/")
        while True:
             await asyncio.sleep(1)

asyncio.run(main())