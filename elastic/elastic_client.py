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
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body=mapping)
