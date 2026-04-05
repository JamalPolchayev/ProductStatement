import asyncio
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_driverless.types.webelement import NoSuchElementException


async def safe_text(el) -> str:
    try:
        text = await el.text
        return text.strip()
    except Exception:
        return ""


async def click_if_exists(driver: webdriver.Chrome, xpaths: List[str], timeout: int = 3) -> bool:
    for xpath in xpaths:
        try:
            # el = WebDriverWait(driver, timeout).until(
            #     EC.element_to_be_clickable((By.XPATH, xpath))
            # )
            el = await driver.find_element(By.XPATH, xpath)
            await driver.execute_script("arguments[0].click();", el)
            await asyncio.sleep(2)
            return True
        except Exception:
            continue
    return False


async def scroll_page(driver: webdriver.Chrome, pause: float = 1.5, steps: int = 6) -> None:
    for _ in range(steps):
        await driver.execute_script("window.scrollBy(0, 1200);")
        await asyncio.sleep(pause)


async def get_main_name(driver: webdriver.Chrome) -> Optional[str]:
    xpaths = [
        '//h1',
        '//main//h1',
        '//div[contains(@class,"pv-text-details__left-panel")]//h1',
    ]

    for xpath in xpaths:
        try:
            el = await driver.find_element(By.XPATH, xpath)
            text = await safe_text(el)
            if text:
                return text
        except NoSuchElementException:
            pass
    return None


async def find_section_by_heading(driver: webdriver.Chrome, heading_variants: List[str]):
    """
    Ищем section, внутри которого есть заголовок Experience / Education.
    """
    xpath_conditions = " or ".join(
        [
            f'.//*[self::h2 or self::span or self::div][contains(translate(normalize-space(.), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{h.lower()}")]'
            for h in heading_variants]
    )

    xpaths = [
        f'//section[{xpath_conditions}]',
        f'//div[{xpath_conditions}]',
    ]

    for xpath in xpaths:
        try:
            return await driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            continue
    return None


async def extract_experience(driver: webdriver.Chrome) -> List[Dict]:
    results = []

    # Пытаемся раскрыть полный список опыта
    await click_if_exists(driver, [
        '//a[contains(@href, "/details/experience/")]',
        '//span[contains(text(),"Show all")]/ancestor::a[contains(@href, "experience")]',
        '//a[contains(., "experience")]',
    ])

    await asyncio.sleep(2)
    await scroll_page(driver, pause=1, steps=3)

    exp_section = await find_section_by_heading(driver, ["experience", "опыт", "təcrübə"])
    if not exp_section:
        return results

    items = await exp_section.find_elements(By.XPATH, './/li')
    if not items:
        items = await exp_section.find_elements(By.XPATH, './/div[contains(@class, "pvs-entity")]')

    seen = set()

    for item in items:
        text = await safe_text(item)
        if not text or len(text) < 8:
            continue

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            continue

        title = lines[0] if len(lines) > 0 else ""
        company = lines[1] if len(lines) > 1 else ""
        duration = ""
        location = ""

        for line in lines[2:]:
            low = line.lower()
            if any(word in low for word in ["yr", "mos", "month", "year", "г", "лет", "il", "ay"]):
                duration = line
            elif not location:
                location = line

        key = (title, company, duration)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "title": title,
            "company": company,
            "duration": duration,
            "location": location,
            "raw": text
        })

    return results


async def extract_education(driver: webdriver.Chrome) -> List[Dict]:
    results = []

    # Пытаемся раскрыть полный список образования
    await click_if_exists(driver, [
        '//a[contains(@href, "/details/education/")]',
        '//span[contains(text(),"Show all")]/ancestor::a[contains(@href, "education")]',
        '//a[contains(., "education")]',
    ])

    await asyncio.sleep(2)
    await scroll_page(driver, pause=1, steps=3)

    edu_section = await find_section_by_heading(driver, ["education", "образование", "təhsil"])
    if not edu_section:
        return results

    items = await edu_section.find_elements(By.XPATH, './/li')
    if not items:
        items = await edu_section.find_elements(By.XPATH, './/div[contains(@class, "pvs-entity")]')

    seen = set()

    for item in items:
        text = await safe_text(item)
        if not text or len(text) < 8:
            continue

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            continue

        school = lines[0] if len(lines) > 0 else ""
        degree = lines[1] if len(lines) > 1 else ""
        period = ""

        for line in lines[2:]:
            low = line.lower()
            if any(ch.isdigit() for ch in line) and ("-" in line or "–" in line or "to" in low):
                period = line
                break

        key = (school, degree, period)
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "school": school,
            "degree": degree,
            "period": period,
            "raw": text
        })

    return results


def extract_from_search_cards(driver: webdriver.Chrome) -> List[Dict]:
    """
    Фоллбек для случая, когда открыт не профиль, а список людей.
    """
    cards_data = []

    cards = driver.find_elements(By.XPATH, '//a[contains(@href, "/in/")]')
    seen = set()

    for card in cards:
        try:
            href = card.get_attribute("href")
            text = safe_text(card)
            if not href or "/in/" not in href or not text:
                continue

            lines = [x.strip() for x in text.split("\n") if x.strip()]
            if not lines:
                continue

            name = lines[0]
            headline = lines[1] if len(lines) > 1 else ""

            key = (name, href)
            if key in seen:
                continue
            seen.add(key)

            cards_data.append({
                "name": name,
                "headline": headline,
                "profile_url": href
            })
        except Exception:
            continue

    return cards_data


async def parse_linkedin_profile(driver , url: str) -> Dict:
    await driver.get(url)
    await asyncio.sleep(5)

    await scroll_page(driver)

    name = await get_main_name(driver)
    experience = await extract_experience(driver)
    education = await extract_education(driver)

    data = {
        "name": name,
        "experience": experience,
        "education": education
    }

    # Если это не профиль, а список карточек



    return data

#
# async def parse_profile(driver: webdriver.Chrome, url: str) -> Dict:
#
#
#
#     try:
#         result = parse_linkedin_profile(driver, PROFILE_URL)
#
#         print(json.dumps(result, ensure_ascii=False, indent=2))

#         with open("linkedin_profile_data.json", "w", encoding="utf-8") as f:
#             json.dump(result, f, ensure_ascii=False, indent=2)
#
#     finally:
#         driver.quit()
