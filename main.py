import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from config import INDEX_NAME  # Örneğin: "world_population_data"
from elastic.elastic_client import (
    get_elastic_client, 
    send_to_elastic, 
    create_index_with_mapping, 
    update_current_snapshot
)
from scraper.world_population import scrape_world_population
from scraper.country_population import scrape_country_population
def process_data():
    es = get_elastic_client()
    if not es:
        print("Elasticsearch bağlantı hatası!")
        return None

    try:
        # İndeks mevcut değilse oluştur (mapping uygulanır)
        create_index_with_mapping(es, INDEX_NAME)

        # Yeni kazıma çalışması için ortak timestamp belirleyin.
        # (Bu timestamp, yeni dokümanlara eklenecek ve aktif snapshot olarak işaretlenecek.)
        sync_timestamp = datetime.now(timezone.utc).isoformat()

        # Paralel scraping işlemleri
        with ThreadPoolExecutor(max_workers=2) as executor:
            world_future = executor.submit(scrape_world_population)
            country_future = executor.submit(scrape_country_population)

            world_data = world_future.result()
            country_data = country_future.result()

            if not world_data or not country_data:
                print("Eksik veri - World Data:", bool(world_data), "Country Data:", bool(country_data))
                return None

            # Yeni world verisini oluşturup, is_current alanını false olarak ekleyelim.
            world_doc = {
                "@timestamp": sync_timestamp,
                "type": "world",
                "is_current": False,  # Varsayılan olarak false; scraping tamamlandıktan sonra update ile true yapılacak.
                "world": {
                    "current_population": world_data.get("current_population", 0),
                    "births_today": world_data.get("births_today", 0),
                    "deaths_today": world_data.get("deaths_today", 0),
                    "growth_today": world_data.get("growth_today", 0)
                }
            }
            send_to_elastic(INDEX_NAME, world_doc)

            # Ülke verilerini de aynı şekilde ekleyelim.
            country_docs = []
            for country in country_data:
                country_doc = {
                    "@timestamp": sync_timestamp,
                    "type": "country",
                    "is_current": False,  # İlk etapta false
                    "country": country["country"],
                    "current_population": country["current_population"],
                    "yearly_change": country["yearly_change"],
                    "net_change": country["net_change"],
                    "migrants": country["migrants"]
                }
                country_docs.append(country_doc)
            
            send_to_elastic(INDEX_NAME, country_docs)
            print("Yeni veriler başarıyla indekslendi.")

            # Yeni veriler tamamen indekslendikten sonra, eski snapshot dokümanlarıyla karışmaması için
            # tüm verilerdeki is_current alanını güncelleyelim:
            # Bu işlem ile @timestamp değeri yeni sync_timestamp olanlar aktif (true), diğerleri pasif (false) olacak.
            update_current_snapshot(es, INDEX_NAME, sync_timestamp)

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
