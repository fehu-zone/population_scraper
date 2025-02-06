import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from config import INDEX_NAME
from elastic.elastic_client import get_elastic_client, send_to_elastic, create_index_with_mapping
from scraper.world_population import scrape_world_population
from scraper.country_population import scrape_country_population

# main.py'deki process_data fonksiyonunu güncelle
def process_data():
    es = get_elastic_client()
    if not es:
        print("Elasticsearch bağlantı hatası!")
        return None

    try:
        create_index_with_mapping(es, INDEX_NAME)
        sync_timestamp = datetime.now(timezone.utc).isoformat()

        with ThreadPoolExecutor(max_workers=2) as executor:
            world_future = executor.submit(scrape_world_population)
            country_future = executor.submit(scrape_country_population)

            world_data = world_future.result()
            country_data = country_future.result()

            if not world_data or not country_data:
                print("Eksik veri - World Data:", bool(world_data), "Country Data:", bool(country_data))
                return None

            # Dünya verisini ayrı bir döküman olarak gönder
            world_doc = {
                "@timestamp": sync_timestamp,
                "type": "world",
                "world": {
                    "current_population": world_data.get("current_population", 0),
                    "births_today": world_data.get("births_today", 0),
                    "deaths_today": world_data.get("deaths_today", 0),
                    "growth_today": world_data.get("growth_today", 0)
                }
            }
            send_to_elastic(INDEX_NAME, world_doc)

            # Her ülkeyi ayrı döküman olarak gönder
            country_docs = []
            for country in country_data:
                country_doc = {
                    "@timestamp": sync_timestamp,
                    "type": "country",
                    "country": country["country"],
                    "current_population": country["current_population"],
                    "yearly_change": country["yearly_change"],
                    "net_change": country["net_change"],
                    "migrants": country["migrants"]
                }
                country_docs.append(country_doc)
            
            send_to_elastic(INDEX_NAME, country_docs)  # Liste olarak gönder

            print("Veri başarıyla gönderildi")
            return True

    except Exception as e:
        print(f"Veri işleme hatası: {str(e)}")
        return None

def main():
    while True:
        try:
            start_time = time.time()
            process_data()
            elapsed = time.time() - start_time
            sleep_time = max(300 - elapsed, 60)  # Minimum 1 dakika bekle
            print(f"Sonraki çekim için bekleniyor: {sleep_time:.0f}s")
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            print("Program sonlandırılıyor...")
            break
        except Exception as e:
            print(f"Kritik hata: {str(e)}")
            time.sleep(600)  # Büyük hata durumunda 10 dakika bekle

if __name__ == "__main__":
    main()
