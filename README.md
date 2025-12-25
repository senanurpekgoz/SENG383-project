# Veri Yapıları ve Algoritmalar - Dönem Projeleri

Bu repository, **Veri Yapıları ve Algoritmalar** dersi kapsamında geliştirilen projelerin kaynak kodlarını, teknik dokümantasyonlarını ve test raporlarını içermektedir.

Repository içerisinde iki ana proje (**BeePlan** ve **KidTask**) `src` klasörü altında bağımsız olarak yapılandırılmıştır.

---

## 📂 Proje Listesi

### 1. 🧒 [KidTask (Final Projesi)](./src/kidTask)
**Çocuk Görev ve Dilek Yönetim Sistemi**
* **Geliştirici:** Sena Nur Pekgöz (Analist/Tester: Ceren Kızılay)
* **Teknoloji:** Python (GUI & File Handling)
* **Açıklama:** Çocukların günlük görevlerini takip etmesini sağlayan, görev tamamladıkça puan kazandıran ve seviye atlatan oyunlaştırılmış (gamified) yönetim sistemi.
* **Detaylar:** Proje içi teknik detaylar için [KidTask README dosyasını](./src/kidTask/README2.md) inceleyebilirsiniz.

### 2. 🐝 [BeePlan (Vize Projesi)](./src/BeePlan)
**Kısıt Tabanlı Ders Programı Oluşturucu**
* **Geliştirici:** Ceren Kızılay (Analist/Tester: Sena Nur Pekgöz)
* **Teknoloji:** Python (Constraint Satisfaction Algorithm)
* **Açıklama:** Ders, hoca, sınıf ve zaman kısıtlarını dikkate alarak çakışmasız ders programı hazırlayan algoritma.
* **Detaylar:** Algoritma mantığı için [BeePlan README dosyasını](./src/BeePlan/README1.md) inceleyebilirsiniz.

---

## 📁 Repository Klasör Yapısı

Proje dosyaları, kaynak kodlar (`src`) ve dokümantasyon (`docs`) olarak ayrıştırılmıştır. Aşağıdaki ağaç yapısı, repository'nin güncel durumunu yansıtmaktadır:

```text
SENG383-project/
├── README.md                           # (Şu an okuduğunuz genel giriş dosyası)
│
├── docs/                               # Proje Raporları ve Test Dokümanları
│   ├── Final Proje Raporu_ KidTask.pdf # Final Projesi Teknik Raporu
│   ├── Week 11 Output...pdf            # Test Senaryoları ve Versiyon Takibi
│   ├── AI Tool Evaluation Form...      # AI Kullanım Analizi
│   └── EVALUATION_REPORT_SENA.md       # Değerlendirme Notları
│
├── video/                              # Sunum Materyalleri
│   └── BeePlan-Akilli-Zaman...         # Proje Tanıtım Dosyaları
│   └── KidTask-Eglenceli-ve-Puanli...  # Proje Tanıtım Dosyaları
│
└── src/                                # Kaynak Kodlar (Source Code)
    │
    ├── kidTask/                        # FINAL PROJESİ (Student A)
    │   ├── README2.md                  # KidTask Özel Kurulum Dosyası
    │   ├── main_gui.py                 # Arayüz Başlatıcı
    │   ├── kidtask_app.py              # Uygulama Yöneticisi
    │   ├── controller.py               # Mediator (Business Logic)
    │   ├── setup_data.py               # Veri Tabanı Kurulum Scripti
    │   ├── child.py                    # Model: Çocuk ve Seviye Sistemi
    │   ├── task.py                     # Model: Görev Yapısı
    │   ├── user.py                     # Model: Kullanıcı Rolleri
    │   ├── wish.py                     # Model: Dilek Sistemi
    │   ├── requirements.txt            # Gerekli Kütüphaneler
    │   └── data/                       # JSON Veri Klasörü
    │
    └── BeePlan/                        # VIZE PROJESİ
        ├── README1.md                  # BeePlan Özel Dokümantasyonu
        ├── main_gui.py                 # Algoritma Arayüzü
        ├── scheduler.py                # Çizelgeleme Algoritması
        ├── test_run.py                 # Test Scripti
        └── university_schedule...json  # Test Verisi
