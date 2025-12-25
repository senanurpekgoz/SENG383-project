# BeePlan - Çankaya Üniversitesi Ders Programı Hazırlama Sistemi

BeePlan, Çankaya Üniversitesi için otomatik ders programı oluşturma ve yönetim sistemidir. Backtracking algoritması kullanarak çakışmasız ders programları üretir.

## Özellikler

### 1. Otomatik Program Oluşturma
- Backtracking algoritması ile çakışmasız program üretimi
- Kısıtlamalara uygun zamanlama
- Çoklu şube desteği

### 2. Kısıtlamalar ve Kurallar
- **Günlük Sınır**: Bir öğretim elemanı günde en fazla 4 saat teorik ders verebilir
- **Cuma Kısıtı**: Cuma günleri 13:20-15:10 arası "Ortak Sınavlar" için ayrılmıştır
- **Lab Sıralama**: Lab dersleri teorik derslerden sonra planlanmalı ve ardışık 2 saat olmalıdır
- **Çakışma Önleme**: Aynı sınıf seviyesindeki zorunlu dersler ve aynı hocanın farklı dersleri çakışmamalıdır
- **Kapasite**: Lab derslerinde bir şube 40 öğrenciyi geçemez
- **Seçmeli Dersler**: CENG ve SENG seçmeli derslerinin çakışmaması önceliği

### 3. Ders Seçimi
- Öğrenciler için sınıf bazlı ders seçimi
- Teori ve lab derslerinin otomatik eşleştirilmesi
- Seçilen derslerle program oluşturma

### 4. Veri Yönetimi
- JSON formatında veri yükleme/kaydetme
- Ders, öğretim elemanı ve derslik yönetimi
- Zaman dilimi ayarları

## Kurulum

### Gereksinimler
- Python 3.6+
- PyQt5

### Adımlar

1. Repository'yi klonlayın:
```bash
git clone <repository-url>
cd BeePlan
```

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

### Uygulamayı Çalıştırma
```bash
python main_gui.py
```

### Veri Yükleme
1. Ana ekranda "Veri Yükle (JSON)" butonuna tıklayın
2. `university_schedule_data.json` veya `example_data.json` dosyasını seçin
3. Veriler otomatik olarak yüklenecektir

### Program Oluşturma

#### Yöntem 1: Tüm Derslerle
1. "Dersler" sekmesinden dersleri kontrol edin
2. "Ders Programı" sekmesine dönün
3. "Program Oluştur" butonuna tıklayın

#### Yöntem 2: Seçilen Derslerle
1. "Ders Seçimi" sekmesine gidin
2. Sınıfınızı seçin (1, 2, 3, 4)
3. Mevcut derslerden seçim yapın
4. "Seçilen Derslerle Program Oluştur" butonuna tıklayın

### Program Kaydetme
1. Oluşturulan programı kontrol edin
2. "Programı Kaydet" butonuna tıklayın
3. JSON formatında kaydedin

## Dosya Yapısı

```
BeePlan/
├── main_gui.py              # Ana GUI uygulaması
├── scheduler.py              # Program oluşturma algoritması
├── example_data.json         # Örnek veri dosyası
├── university_schedule_data.json  # Üniversite veri dosyası
├── requirements.txt          # Python bağımlılıkları
├── README.md                 # Bu dosya
└── .gitignore                # Git ignore dosyası
```

## Teknik Detaylar

### Algoritma
- **Backtracking**: Çakışmasız program üretimi için geri izleme algoritması
- **Öncelik Sıralaması**:
  1. Sabit zaman dilimli dersler
  2. Ortak dersler (PHYS, MATH, ENG, TURK, HIST)
  3. Teori dersleri (lab'lardan önce)
  4. Düşük sınıf seviyeli dersler
  5. Zorunlu dersler (seçmelilerden önce)

### Veri Modelleri
- **Course**: Ders bilgileri (kod, ad, öğretim elemanı, saat, tip, sınıf, vb.)
- **Instructor**: Öğretim elemanı bilgileri ve kısıtlamaları
- **Room**: Derslik bilgileri (ad, kapasite, tip)

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## Geliştirici Notları

- Tüm veriler JSON formatında saklanır
- Program oluşturma işlemi gerçek zamanlı olarak çalışır
- Manuel düzenleme yapılabilir (tablo hücrelerine çift tıklayarak)


