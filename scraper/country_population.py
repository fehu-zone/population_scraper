from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scraper.utils import format_number
from datetime import datetime, timezone

# Ülke isimlerinde yapılacak düzeltmeleri burada belirtebilirsiniz.
# country_population.py'deki mapping
COUNTRY_NAME_MAPPING = {
    "United States": "USA",
    "Congo": "DR Congo",
    "Iran (Islamic Republic of)": "Iran",
    "Viet Nam": "Vietnam",
    "Czechia": "Czech Republic",
    # Diğer tutarsızlıklar için eklemeler yapın
}

def scrape_country_population():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # GUI olmadan çalışma
        driver = webdriver.Chrome(options=options)
        
        print(f"Ülke verileri için URL'ye erişiliyor: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        table = wait.until(EC.presence_of_element_located((By.ID, "example2")))

        # 📌 Sıralama butonuna tıklayarak nüfusu en yüksekten en küçüğe sıralayalım
        sorting_button = driver.find_element(By.XPATH, "//th[@aria-label='#: activate to sort column descending']")
        sorting_button.click()  # İlk tıklama ascending (küçükten büyüğe) sıralar
        sorting_button.click()  # İkinci tıklama descending (büyükten küçüğe) sıralar
        
        print("📌 Nüfusa göre sıralama tamamlandı!")

        # 📌 Güncellenmiş tabloyu tekrar bekleyelim
        wait.until(EC.presence_of_element_located((By.ID, "example2")))

        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        country_data = []

        for index, row in enumerate(rows, 1):
            try:
                cells = row.find_elements(By.TAG_NAME, "td")
                # Minimum 8 sütun olması gerektiğinden kontrol ediyoruz (index 7'ye kadar veri var mı)
                if len(cells) < 8:
                    print(f"[Satır {index}] Atlandı: Yetersiz sütun")
                    continue

                # Ülke ismi standardizasyonu
                raw_country = cells[1].text.strip()
                country_name = COUNTRY_NAME_MAPPING.get(raw_country, raw_country)
                
                # İlgili sütunlardan veriyi çekiyoruz:
                population = format_number(cells[2].text)
                yearly_change = float(cells[3].text.replace('%', '').strip() or 0)
                net_change = format_number(cells[4].text)
                # Burada index 7, 'Migrants (net)' sütunu
                migrants = format_number(cells[7].text)

                # Veri kalite kontrolü: Zorunlu alanlarda veri yoksa satırı atla
                if None in [population, net_change, migrants]:
                    print(f"[{country_name}] Eksik veri içeren satır atlandı")
                    continue

                country_data.append({
                    "country": country_name,
                    "current_population": population,  # population -> current_population
                    "yearly_change": round(yearly_change, 2),
                    "net_change": net_change,
                    "migrants": migrants
                })

                print(f"[{index}] {country_name} verisi işlendi")

            except Exception as row_error:
                print(f"Satır {index} işleme hatası: {str(row_error)}")
                continue

        print(f"📌 Başarıyla alınan ülke sayısı: {len(country_data)}")
        return country_data  # Fonksiyon bir liste döndürsün ki diğer işlemlerde kullanabilelim.

    except Exception as e:
        print(f"❌ Ülke verisi çekme hatası: {str(e)}")
        return None
    finally:
        if driver:
            driver.quit()


