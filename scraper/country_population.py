from selenium import webdriver
from selenium.webdriver.common.by import By
from scraper.utils import format_number

def scrape_country_population():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    driver = webdriver.Chrome()
    try:
        print(f"URL'ye erişiliyor: {url}")
        driver.get(url)
        driver.implicitly_wait(5)

        print("Tablo verileri çekiliyor...")
        table = driver.find_element(By.ID, "example2")
        rows = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")

        country_data = []
        print(f"{len(rows)} satır bulundu. Veri işleniyor...")
        for index, row in enumerate(rows, start=1):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 6:
                print(f"[Satır {index}] Atlandı: Beklenen sütun sayısı eksik.")
                continue

            yearly_change_str = cells[3].text
            try:
                yearly_change = float(yearly_change_str.replace('%', '').strip())
            except ValueError:
                yearly_change = None
                print(f"[Satır {index}] Yıllık değişim verisi dönüştürülemedi: {yearly_change_str}")

            country_info = {
                "country": cells[1].text,
                "population": format_number(cells[2].text),
                "yearly_change": yearly_change,
                "net_change": format_number(cells[4].text),
                "migrants": format_number(cells[5].text)
            }
            print(f"[Satır {index}] Veri işlendi: {country_info}")

            country_data.append(country_info)

        print(f"\nToplam {len(country_data)} ülke verisi başarıyla işlendi.")
        return country_data

    except Exception as e:
        print(f"scrape_country_population Hata: {e}")
        return None

    finally:
        print("Tarayıcı kapatılıyor...")
        driver.quit()
