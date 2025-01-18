from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from scraper.utils import extract_number_from_element

def scrape_world_population():
    url = "https://www.worldometers.info/world-population/"             
    driver = webdriver.Chrome()
    try:
        print(f"URL'ye erişiliyor: {url}")
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Dünya nüfusu
        print("Dünya nüfusu verisi alınıyor...")
        current_population = extract_number_from_element(
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='maincounter-number']/span[@rel='current_population']")
            ))
        )
        print(f"-> Güncel Nüfus: {current_population}")

        # Bugünkü doğumlar
        print("Bugünkü doğumlar verisi alınıyor...")
        births_today = extract_number_from_element(
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[@class='rts-counter' and @rel='births_today']")
            ))
        )
        print(f"-> Bugünkü Doğumlar: {births_today}")

        # Bugünkü ölümler
        print("Bugünkü ölümler verisi alınıyor...")
        try:
            deaths_today = extract_number_from_element(
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//span[@class='rts-counter' and @rel='dth1s_today']")
                ))
            )
            print(f"-> Bugünkü Ölümler: {deaths_today}")
        except Exception as e:
            deaths_today = None
            print(f"Hata: Ölümler verisi alınamadı. {e}")

        # Bugünkü nüfus artışı
        print("Bugünkü nüfus artışı verisi alınıyor...")
        growth_today = extract_number_from_element(
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//span[@class='rts-counter' and @rel='absolute_growth']")
            ))
        )
        print(f"-> Bugünkü Nüfus Artışı: {growth_today}")

        data = {
            "current_population": current_population,
            "births_today": births_today,
            "deaths_today": deaths_today,
            "growth_today": growth_today,
            "timestamp": datetime.now().isoformat()
        }

        print("Dünya nüfusu verileri başarıyla alındı.")
        return data

    except Exception as e:
        print(f"scrape_world_population Hata: {e}")
        return None

    finally:
        print("Tarayıcı kapatılıyor...")
        driver.quit()
