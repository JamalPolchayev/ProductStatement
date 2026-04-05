import os

from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio

title = "Python developer"

async def main():
    options = webdriver.ChromeOptions()
    path = os.path.join(os.getcwd(), 'api_userdata', f"account")
    options.add_argument(f'--user-data-dir={path}')
    options._auto_clean_dirs = False
    async with webdriver.Chrome(options=options) as driver:
        users = []
        for i in range(3):
            await driver.get(f'https://www.linkedin.com/search/results/people/?keywords={title}&origin=SWITCH_SEARCH_VERTICAL&page={i+1}', wait_load=True)

            cards = await driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')
            for card in cards:
                user_link = await card.find_element(By.CSS_SELECTOR, ':scope > div p a[href^="https://www.linkedin.com/in/"]')
                user_link = await user_link.execute_script("return obj.getAttribute('href');")
                users.append(user_link)

            await asyncio.sleep(3)

        print(users)


asyncio.run(main())