import os
import re
import asyncio

from selenium_driverless import webdriver
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument("--window-size=1920,3000")

path = os.path.join(os.getcwd(), "api_userdata", "account")
options.add_argument(f"--user-data-dir={path}")
options._auto_clean_dirs = False


def get_minified_source(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")

    TAGS_TO_REMOVE = ["script", "style", "svg", "img", "iframe", "noscript"]
    ATTRS_TO_REMOVE = [
        "class", "style", "id", "data-testid", "data-test-id",
        "data-view-name", "data-qa", "nonce", "integrity", "crossorigin",
    ]

    # Удалить ненужные теги
    for tag in soup.find_all(TAGS_TO_REMOVE):
        tag.decompose()

    # Удалить ненужные атрибуты
    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if (
                attr in ATTRS_TO_REMOVE
                or attr.startswith("data-")
                or attr.startswith("aria-")
            ):
                del tag[attr]

    html = str(soup)

    # Минификация
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"\s{2,}", " ", html)
    html = re.sub(r"\n+", "", html)

    return html.strip()


async def main():
    async with webdriver.Chrome(options=options) as dr:
        await dr.get("https://www.linkedin.com/in/fazil-askerov-8b5803151/")
        await asyncio.sleep(5)  # подождать загрузку

        await dr.execute_script("window.scrollBy(0, 1200);")
        await asyncio.sleep(3)

        raw_html = await dr.page_source  # получить HTML через селениум

        minified_html = get_minified_source(raw_html)  # обработать через bs4

        with open("linkedin_minified.html", "w", encoding="utf-8") as f:
            f.write(minified_html)

        print("Сохранено в linkedin_minified.html")
        print(minified_html[:2000])

        while True:
            await asyncio.sleep(1)


asyncio.run(main())