# Worldometer Veri İzleme ve Görselleştirme Sistemi 🌍📊  

*Python, Selenium, Elasticsearch & Kibana ile Gerçek Zamanlı Veri Analizi*  

## Proje Genel Bakış / Project Overview 🚀  

<div align="center">  
  <svg xmlns="http://www.w3.org/2000/svg" height="100" viewBox="0 96 960 960" width="100" fill="#B22222">  
    <path d="M480 976q-33 0-56.5-23.5T400 896q0-33 23.5-56.5T480 816q33 0 56.5 23.5T560 896q0 33-23.5 56.5T480 976Zm0-200-120-120-120 120H80l120-320V336h80v120l120 320h80l120-320V336h80v120l120 320h-160l-120-120-120 120Z"/>  
  </svg>  
  <br>  
  <em>Veri Akış Mimarisi: Scraping → Elasticsearch → Kibana → Web Arayüzü</em>  
</div>  

---

### 🌟 Temel Özellikler
- **Akıllı Web Scraping:** Worldometer'dan anlık nüfus verilerini yakalayan optimize edilmiş Selenium botu  
- **Veri Bütünlüğü Kontrolü:** Eksik/korrupt verileri otomatik tespit eden doğrulama katmanı  
- **Elasticsearch Entegrasyonu:** Zaman serisi verileri için özel tasarlanmış indeks haritalaması  
- **Kibana Dashboardları:** Nüfus artışı ve demografik trendler için interaktif görseller  
- **Self-Hosted Web Arayüzü:** [population-data-app](https://github.com/fehu-zone/population-data-app) ile özelleştirilebilir veri sunumu  

---

## Teknoloji Stack'i 🛠️  

<div align="center">  
  <a href="https://www.python.org/" target="_blank">  
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python" alt="Python 3.10+">  
  </a>  
  <a href="https://www.selenium.dev/" target="_blank">  
    <img src="https://img.shields.io/badge/Selenium-4.8+-43B02A?logo=selenium" alt="Selenium 4.8+">  
  </a>  
  <a href="https://www.elastic.co/elasticsearch/" target="_blank">  
    <img src="https://img.shields.io/badge/Elasticsearch-8.7-005571?logo=elasticsearch" alt="Elasticsearch 8.7">  
  </a>  
  <a href="https://www.elastic.co/kibana/" target="_blank">  
    <img src="https://img.shields.io/badge/Kibana-8.7-005571?logo=kibana" alt="Kibana 8.7">  
  </a>  
  <a href="https://github.com/fehu-zone/population-data-app" target="_blank">  
    <img src="https://img.shields.io/badge/Web_Arayüzü-Vue.js-4FC08D?logo=vue.js" alt="Vue.js Web Arayüzü">  
  </a>  
</div>  

---

## Sistem Mimarisi 🏗️  

<details>
    <summary>Mermaid Diyagramı</summary>
   ```mermaid
  graph TD
      A[Worldometer] -->|Selenium Bot| B(Data Scraping)
      B --> C{Data Validation}
      C -->|Valid| D[Elasticsearch]
      C -->|Invalid| E[Error Management]
      D --> F[Kibana Dashboard]
      D --> G[Web Interface]
      G --> H[User Interaction]

</details>

 
