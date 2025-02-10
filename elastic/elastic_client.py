# C:\Users\Fehu\Desktop\population_scraper\elastic\elastic_client.py

from elasticsearch import Elasticsearch, helpers
from config import ELASTICSEARCH_HOSTS, ELASTIC_PASSWORD

def get_elastic_client():
    return Elasticsearch(
        ELASTICSEARCH_HOSTS,
        basic_auth=("elastic", ELASTIC_PASSWORD),
        verify_certs=False,
        ssl_show_warn=False
    )

def send_to_elastic(index_name, data):
    es = get_elastic_client()
    if not es.ping():
        print("Elasticsearch bağlantı hatası!")
        return

    try:
        if isinstance(data, list):
            actions = [{"_index": index_name, "_source": record} for record in data]
            helpers.bulk(es, actions)
            print(f"{len(data)} kayıt {index_name} indeksine gönderildi.")
        elif isinstance(data, dict):
            es.index(index=index_name, document=data)
            print(f"1 kayıt {index_name} indeksine gönderildi.")
        else:
            raise ValueError("Geçersiz veri tipi: dict veya list olmalı")
    except Exception as e:
        print(f"Elasticsearch gönderim hatası: {str(e)}")

def create_index_with_mapping(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "@timestamp": {"type": "date"},
                "type": {"type": "keyword"},  # Döküman tipi (world/country)
                "is_current": {"type": "boolean"},  # Aktif snapshot mu?
                "world": {  # Sadece type:world dökümanlarında kullanılır
                    "properties": {
                        "current_population": {"type": "long"},
                        "births_today": {"type": "long"},
                        "deaths_today": {"type": "long"},
                        "growth_today": {"type": "long"}
                    }
                },
                # Aşağıdakiler type:country dökümanlarında kullanılır
                "country": {"type": "keyword"},
                "current_population": {"type": "long"},
                "yearly_change": {"type": "float"},
                "net_change": {"type": "long"},
                "migrants": {"type": "long"}
            }
        }
    }

    if es.indices.exists(index=index_name):
        print(f"{index_name} indeksi zaten mevcut. Mapping güncellemesi yapılmadı.")
        return

    es.indices.create(index=index_name, body=mapping)
    print(f"{index_name} indeksi oluşturuldu.")


# Aşağıdaki fonksiyonu ekleyin:
def update_current_snapshot(es, index_name, new_snapshot):
    """
    İndeksteki tüm dökümanlarda:
      - @timestamp değeri new_snapshot olanlara is_current=true,
      - diğerlerine is_current=false
    ayarlanır.
    """
    # 1. Tüm dökümanları false yapalım:
    response1 = es.update_by_query(
        index=index_name,
        body={
            "query": {"match_all": {}},
            "script": {"source": "ctx._source.is_current = false", "lang": "painless"}
        },
        refresh=True  # Değişikliklerin hemen sorgulanabilir olmasını sağlar.
    )
    print("Tüm dökümanlarda is_current false yapıldı:", response1)

    # 2. Yeni snapshot'a ait dökümanlarda is_current'u true yapalım:
    response2 = es.update_by_query(
        index=index_name,
        body={
            "query": {"term": {"@timestamp": new_snapshot}},
            "script": {"source": "ctx._source.is_current = true", "lang": "painless"}
        },
        refresh=True
    )
    print("Yeni snapshot için is_current true yapıldı:", response2)
