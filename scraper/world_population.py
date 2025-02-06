from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.utils import extract_number_from_element  # Assuming this is your utility function
from datetime import datetime, timezone

WORLD_DATA_ELEMENTS = {
    "current_population": "//div[@class='maincounter-number']/span[@rel='current_population']",
    "births_today": "//span[@rel='births_today']",
    "deaths_today": "//span[@rel='dth1s_today']",
    "growth_today": "//span[@rel='absolute_growth']"
}

def scrape_world_population():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)

        print("Dünya nüfus verileri alınıyor...")
        driver.get("https://www.worldometers.info/world-population/")

        wait = WebDriverWait(driver, 15)
        world_data = {}

        for key, xpath in WORLD_DATA_ELEMENTS.items():
            try:
                element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                value = extract_number_from_element(element)
                print(f"{key} için bulunan değer: {value}")
                world_data[key] = value or 0
            except Exception as e:
                print(f"{key} verisi alınamadı, xpath: {xpath}, hata: {str(e)}")
                world_data[key] = 0  # Assign 0 if data retrieval fails

        # Veri kalite kontrolü
        if world_data["current_population"] < 7000000000:
            raise ValueError("Anormal nüfus değeri")

        print("Dünya verileri başarıyla alındı")
        return world_data

    except Exception as e:
        print(f"Dünya verisi çekme hatası: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()