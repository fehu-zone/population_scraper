from elasticsearch import Elasticsearch
from datetime import datetime

def add_timestamp(data):
    """Veriye zaman damgası ekler."""
    if isinstance(data, list):
        for doc in data:
            if "timestamp" not in doc or not doc["timestamp"]:
                doc["timestamp"] = datetime.now().isoformat()
    elif isinstance(data, dict):
        if "timestamp" not in data or not data["timestamp"]:
            data["timestamp"] = datetime.now().isoformat()

def connect_to_elastic(hosts):
    """Elasticsearch cluster'ına bağlanır."""
    try:
        es = Elasticsearch(hosts)
        if es.ping():
            print("Cluster bağlantısı başarılı.")
            return es
        else:
            print("Cluster bağlantısı başarısız.")
            return None
    except Exception as e:
        print(f"Cluster bağlantısı sırasında hata oluştu: {e}")
        return None

def send_to_elastic(es, index_name, data):
    """Veriyi Elasticsearch'e gönderir."""
    if not es or not data:
        print(f"Elasticsearch bağlantısı veya {index_name} verisi eksik.")
        return

    # Zaman damgası ekleme
    add_timestamp(data)

    success_count = 0
    fail_count = 0

    if isinstance(data, list):
        for item in data:
            try:
                es.index(index=index_name, document=item)
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"Veri gönderim hatası: {e}, Veri: {item}")
    else:
        try:
            es.index(index=index_name, document=data)
            success_count += 1
        except Exception as e:
            fail_count += 1
            print(f"Veri gönderim hatası: {e}, Veri: {data}")

    print(f"{index_name} indeksine gönderim tamamlandı. "
          f"{success_count} başarıyla gönderildi, {fail_count} başarısız oldu.")

# Örnek kullanım
if __name__ == "__main__":
    HOSTS = ["http://localhost:9200"]
    INDEX_NAME = "example-index"

    # Elasticsearch bağlantısı
    es_client = connect_to_elastic(HOSTS)

    # Örnek veri
    example_data = [
        {"name": "John Doe", "age": 30},
        {"name": "Jane Doe", "age": 25, "timestamp": "2025-01-01T12:00:00"},
    ]

    # Veriyi Elasticsearch'e gönder
    send_to_elastic(es_client, INDEX_NAME, example_data)
