# KidTask - Task and Wish Management Application

Python (PyQt5) GUI Application for managing tasks, wishes, and tracking points/levels.

## Özellikler

### 1. Kullanıcı Rolleri
- **Child (Çocuk)**: Görevleri görüntüleyip tamamlayabilir, dilek ekleyebilir
- **Parent (Ebeveyn)**: Görev ve dilek ekleyebilir, onaylayabilir, ilerlemeyi takip edebilir
- **Teacher (Öğretmen)**: Okul görevleri ekleyebilir, tamamlanan görevleri değerlendirebilir

### 2. Görev Yönetimi
- Görev ekleme (başlık, açıklama, bitiş tarihi, puan)
- Günlük/haftalık filtreleme
- Görev tamamlama (Child)
- Görev onaylama ve puanlama (Parent/Teacher)
- Otomatik puan ve seviye güncelleme

### 3. Dilek Yönetimi
- Dilek ekleme (ürün veya aktivite)
- Seviye bazlı görünürlük (çocuk sadece kendi seviyesine uygun dilekleri görür)
- Dilek onaylama/reddetme (Parent/Teacher)

### 4. Puan ve Seviye Takibi
- Toplam puan gösterimi
- Seviye hesaplama (ortalama puanlara göre)
- Progress bar ile görsel gösterim
- Tamamlanan görevlerin listesi

### 5. Veri Kalıcılığı
- JSON formatında dosya tabanlı veri saklama
- Otomatik kaydetme/yükleme
- `data/` klasöründe saklanır:
  - `tasks.json`
  - `wishes.json`
  - `users.json`

## Kurulum

### Gereksinimler
- Python 3.6+
- PyQt5

### Adımlar

1. Repository'yi klonlayın:
```bash
git clone <repository-url>
cd kidTask
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

### 1. Örnek Verileri Oluşturma
```bash
python3 setup_data.py
```

Bu komut şu örnek kullanıcıları oluşturur:
- **Çocuk**: ali / 1234
- **Çocuk**: ayse / 1234
- **Ebeveyn**: parent1 / 1234
- **Öğretmen**: teacher1 / 1234

### 2. Uygulamayı Çalıştırma
```bash
python3 main_gui.py
```

## Kullanıcı Arayüzü

### Login Ekranı
- Kullanıcı adı ve şifre ile giriş

### Ana Sayfa (Dashboard)
- Kullanıcı rolüne göre özelleştirilmiş dashboard
- Puan ve seviye bilgileri
- Son görevler/istatistikler

### Görevler Sekmesi
- Görev listesi (tablo formatında)
- Filtreleme: Tümü, Günlük, Haftalık
- Görev ekleme (Parent/Teacher)
- Görev tamamlama (Child)
- Görev onaylama ve puanlama (Parent/Teacher)

### Dilekler Sekmesi
- Dilek listesi
- Dilek ekleme (Child)
- Dilek onaylama/reddetme (Parent/Teacher)
- Seviye bazlı görünürlük

### İlerleme Sekmesi
- Puan ve seviye detayları
- Progress bar
- Tamamlanan görevler listesi
- Çocukların ilerlemeleri (Parent/Teacher için)

## Seviye Hesaplama

Çocukların seviyeleri, tamamlanan görevlerin ortalama puanlarına göre belirlenir:

- **Level 1**: Ortalama 0-40
- **Level 2**: Ortalama 41-70
- **Level 3**: Ortalama 71-100

## Dosya Yapısı

```
kidTask/
├── main_gui.py          # Ana GUI uygulaması (Python)
├── kidtask_app.py       # Uygulama mantığı ve veri yönetimi
├── user.py              # User sınıfı ve rolleri
├── task.py              # Task sınıfı
├── wish.py              # Wish sınıfı
├── child.py             # Child sınıfı (eski, User ile birleştirildi)
├── setup_data.py        # Örnek veri oluşturma scripti
├── requirements.txt     # Python bağımlılıkları
├── README.md            # Bu dosya
├── .gitignore           # Git ignore dosyası
├── data/                # Veri dosyaları (otomatik oluşturulur)
│   ├── tasks.json
│   ├── wishes.json
│   └── users.json
└── src/                 # Java implementasyonu (alternatif)
    └── main/
        └── java/
            └── kidtask/
                ├── KidTaskApp.java
                ├── data/
                ├── gui/
                └── models/
```

## Teknik Detaylar

- **GUI Framework**: PyQt5
- **Veri Formatı**: JSON
- **Python Versiyonu**: 3.6+
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Alternatif Implementasyon**: Java versiyonu `src/` klasöründe mevcuttur

## Geliştirici Notları

- Tüm veriler `data/` klasöründe JSON formatında saklanır
- Uygulama kapanırken otomatik olarak veriler kaydedilir
- Her kullanıcı rolü için özel dashboard ve yetkiler vardır

