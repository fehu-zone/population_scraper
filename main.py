import time
from elasticsearch import Elasticsearch
from scraper.world_population import scrape_world_population
from scraper.country_population import scrape_country_population
from config import ELASTICSEARCH_HOSTS, INDEX_NAME_WORLD, INDEX_NAME_COUNTRIES, ELASTIC_PASSWORD


def connect_to_elastic(elastic_hosts):
    try:
        es = Elasticsearch(
            elastic_hosts,
            basic_auth=("elastic", ELASTIC_PASSWORD),
            ssl_show_warn=False,
            verify_certs=False,  # Sertifika doğrulamasını devre dışı bırak
        )
        if es.ping():
            print("Elasticsearch bağlantısı başarılı.")
            return es
        else:
            print("Elasticsearch bağlantısı başarısız.")
            return None
    except Exception as e:
        print(f"Elasticsearch bağlantısı sırasında hata: {e}")
        return None




def send_to_elastic(es, index_name, data):
    try:
        # Veriyi Elasticsearch'e gönder
        if isinstance(data, list):  # Çoklu veri gönderimi
            for doc in data:
                es.index(index=index_name, document=doc)
        elif isinstance(data, dict):  # Tekil veri gönderimi
            es.index(index=index_name, document=data)
        print(f"{len(data) if isinstance(data, list) else 1} veri {index_name} indeksine başarıyla gönderildi.")
    except Exception as e:
        print(f"{index_name} indeksine veri gönderimi sırasında hata: {e}")


def main():
    es = connect_to_elastic(ELASTICSEARCH_HOSTS)
    if not es:
        print("Elasticsearch bağlantısı kurulamadı. Program sonlanıyor.")
        return

    while True:
        try:
            # Dünya nüfusu verilerini çek ve Elasticsearch'e gönder
            world_data = scrape_world_population()
            if world_data:
                send_to_elastic(es, INDEX_NAME_WORLD, world_data)
                print(f"{INDEX_NAME_WORLD} indeksi başarıyla tamamlandı.")

            # Ülke nüfus verilerini çek ve Elasticsearch'e gönder
            country_data = scrape_country_population()
            if country_data:
                send_to_elastic(es, INDEX_NAME_COUNTRIES, country_data)
                print(f"{len(country_data)} ülke verisi başarıyla {INDEX_NAME_COUNTRIES} indeksine gönderildi.")

            time.sleep(60)  # 60 saniye bekle
        except KeyboardInterrupt:
            print("Program sonlandırıldı.")
            break
        except Exception as e:
            print(f"Hata: {e}")


if __name__ == "__main__":
    main()
