from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_HOSTS, ELASTIC_PASSWORD

# Elasticsearch bağlantısı
def get_elastic_client():
    """Cluster'daki düğümlerle bağlantı kurar."""
    return Elasticsearch(
        ELASTICSEARCH_HOSTS,
        basic_auth=("elsatic", ELASTIC_PASSWORD),
        verify_certs=False,  # Sertifika doğrulamasını devre dışı bırak
    )

def send_to_elastic(index_name, data):
    """
    Elasticsearch'e veri gönderir.
    
    Args:
        index_name (str): Gönderilecek indeksin adı.
        data (list/dict): Gönderilecek veri. Liste ise toplu, dict ise tekil veri gönderilir.
    """
    es = get_elastic_client()
    if isinstance(data, list):  # Listeyse toplu gönderim
        for record in data:
            es.index(index=index_name, document=record)
        print(f"Toplu veri {index_name} indeksine gönderildi.")
    elif isinstance(data, dict):  # Tek bir veri gönderimi
        es.index(index=index_name, document=data)
        print(f"Tekil veri {index_name} indeksine gönderildi.")
    else:
        print("Geçersiz veri tipi. Veri, liste veya sözlük olmalıdır.")
