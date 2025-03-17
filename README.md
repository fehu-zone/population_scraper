# Worldometer Veri İzleme ve Görselleştirme Sistemi 🌍📊

**Türkçe | [English](#english-version)**  
*Python, Selenium, Elasticsearch & Kibana ile Gerçek Zamanlı Veri Analizi*

---

## Proje Genel Bakış / Project Overview 🚀

<div align="center">
  <img src="https://via.placeholder.com/800x400.png?text=Worldometer+Data+Pipeline+Architecture" alt="Sistem Mimarisi" width="80%">
  <br>
  <em>Veri Akış Mimarisi: Scraping → Elasticsearch → Kibana → Web Arayüzü</em>
</div>

---

### 🌟 Temel Özellikler
- **Akıllı Web Scraping:** Worldometer'dan anlık nüfus verilerini yakalayan optimize edilmiş Selenium botu
- **Veri Bütünlüğü Kontrolü:** Eksik/korupte verileri otomatik tespit eden validation layer
- **Elasticsearch Entegrasyonu:** Zaman serisi verileri için özel tasarlanmış index mapping
- **Kibana Dashboardları:** Nüfus Artışı ve Demografik Trendler için interaktif görseller
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

```mermaid
graph TD
    A[Worldometer] -->|Selenium Bot| B(Veri Kazıma)
    B --> C{Veri Validation}
    C -->|Valid| D[Elasticsearch]
    C -->|Invalid| E[Hata Yönetimi]
    D --> F[Kibana Dashboard]
    D --> G[Web Arayüzü]
    G --> H[Kullanıcı Etkileşimi]
