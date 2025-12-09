# 🇹🇷 ComplaintIQ - Veri Toplama ve Model Eğitimi Rehberi

## 📋 Genel Bakış

ComplaintIQ projesi, Türkiye'ye özel müşteri şikayet kategorilendirme sistemi için **veri toplama**, **otomatik kategorilendirme** ve **model eğitimi** özelliklerini içerir.

## 🏗️ Proje Yapısı

```
d:/ecom-shipping-delay/
├── api.py                          # FastAPI backend
├── app.py                          # Streamlit frontend
├── data_collection_pipeline.py     # Veri toplama pipeline'ı
├── requirements.txt                # Bağımlılıklar
├── src/
│   ├── config.py                   # Konfigürasyon
│   ├── inference.py                # Model inference
│   └── pipeline.py                 # ML pipeline + veri toplama
├── data/
│   ├── raw/                        # Ham veriler
│   └── processed/                  # İşlenmiş veriler
├── notebooks/                      # Jupyter notebooks
└── models/                         # Eğitilmiş modeller
```

## 🚀 Hızlı Başlangıç

### 1. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 2. API Sunucusunu Başlat

```bash
python api.py
```

API `http://localhost:8000` adresinde çalışacaktır.

### 3. Streamlit Frontend'ini Başlat

```bash
streamlit run app.py
```

Frontend `http://localhost:8501` adresinde açılacaktır.

## 💾 Veri Toplama Özellikleri

### A. Tekil Şikayet Ekleme

**Endpoint:** `POST /collect/complaint`

```python
import requests

response = requests.post('http://localhost:8000/collect/complaint', json={
    'text': 'Ürün teslim edilmemiş, çok uzun sürdü',
    'category': None,  # Otomatik algılanacak
    'source': 'manual'
})

print(response.json())
```

**Yanıt:**

```json
{
  "status": "success",
  "complaint": {
    "text": "Ürün teslim edilmemiş, çok uzun sürdü",
    "category": "Kargo Gecikmesi",
    "confidence": 0.95,
    "source": "manual",
    "date": "2024-12-08T17:50:00"
  },
  "message": "Şikayet başarıyla toplandı"
}
```

### B. Toplu Şikayet Ekleme

**Endpoint:** `POST /collect/batch`

```python
complaints = [
    {
        'text': 'Ürün kalitesi çok kötü',
        'source': 'email'
    },
    {
        'text': 'Müşteri hizmetleri çok kaba davrandı',
        'source': 'chat'
    }
]

response = requests.post('http://localhost:8000/collect/batch', json={
    'complaints': complaints
})

print(response.json())
```

### C. Toplanan Verileri Görüntüleme

**Endpoint:** `GET /collect/data`

```python
response = requests.get('http://localhost:8000/collect/data')
data = response.json()

print(f"Toplam şikayet: {data['total_complaints']}")
print(f"Kategori dağılımı: {data['category_distribution']}")
```

### D. Model Eğitimi

**Endpoint:** `POST /train`

```python
# Önce verileri al
data_response = requests.get('http://localhost:8000/collect/data')
complaints = data_response.json()['complaints']

# Modeli eğit
response = requests.post('http://localhost:8000/train', json={
    'complaints': complaints,
    'save_model': True
})

print(response.json())
```

## 🎯 Desteklenen Kategoriler

ComplaintIQ 12 kategoriyi destekler:

1. **Ürün Kalite Sorunu** - Kaliteli olmayan, bozuk ürünler
2. **Yanlış Ürün** - Sipariş edilen ürün yerine başka ürün gelmesi
3. **Eksik Ürün** - Eksik parçalar veya ürünler
4. **Kargo Gecikmesi** - Teslimat gecikmesi
5. **Kargo Firması Problemi** - Kargo şirketi kaynaklı sorunlar
6. **İade/Değişim Sorunu** - İade işlemi sorunları
7. **Ödeme/Fatura Sorunu** - Faturalandırma hataları
8. **Müşteri Hizmetleri Sorunu** - Destek ekibi davranışları
9. **Paketleme/Ambalaj Problemi** - Paketleme hataları
10. **Ürün Açıklaması Yanıltıcı** - Ürün açıklaması uyuşmazlığı
11. **Hizmet Kalite Sorunu** - Genel hizmet kalitesi
12. **Teknik/Uygulama Sorunu** - Yazılım/sistem hataları

## 📊 Streamlit Frontend Sayfaları

### 1. 🏠 Ana Sayfa

- Sistem özeti
- Özellikler listesi
- Desteklenen kategoriler
- Örnek tahmin

### 2. 🔍 Tekil Tahmin

- Tek bir şikayet metni için tahmin
- Hızlı örnekler
- Kategori olasılıkları

### 3. 📊 Toplu İşlem

- CSV dosyası yükleme
- Manuel metin girişi
- Toplu tahmin
- Sonuç analizi ve indirme

### 4. 💾 Veri Toplama (YENİ)

- **Şikayet Ekle:** Tekil şikayet ekleme
- **Toplanan Veriler:** Kategori dağılımı ve istatistikler
- **Model Eğit:** Toplanan verilerle modeli yeniden eğitme

### 5. 📈 Analiz ve Raporlar

- Model istatistikleri
- Kategori bilgileri
- Performance metrikleri

### 6. ⚙️ Sistem Bilgileri

- Teknik bilgiler
- Deployment bilgileri
- Güvenlik özellikleri

## 🔧 Veri Toplama Pipeline Detayları

### TurkeyDataCollector Sınıfı

`src/pipeline.py` dosyasında tanımlanan `TurkeyDataCollector` sınıfı:

```python
from src.pipeline import TurkeyDataCollector

# Collector oluştur
collector = TurkeyDataCollector()

# Şikayet ekle
complaint = collector.add_complaint(
    text="Ürün teslim edilmemiş",
    source="manual",
    category=None  # Otomatik algılanacak
)

# DataFrame'e çevir
df = collector.get_dataframe()
print(df.head())
```

### Otomatik Kategorilendirme

Şikayetler keyword matching kullanılarak otomatik olarak kategorilere ayrılır:

```python
text = "Ürün teslim edilmemiş, çok uzun sürdü"
category, confidence = collector.categorize_text(text)
print(f"Kategori: {category}, Güven: {confidence:.1%}")
# Çıktı: Kategori: Kargo Gecikmesi, Güven: 95.0%
```

## 📈 Model Eğitimi Süreci

1. **Veri Toplama:** Şikayetler API üzerinden toplanır
2. **Ön İşleme:** Metinler temizlenir ve normalize edilir
3. **Özellik Çıkarma:** TF-IDF vektörleştirmesi yapılır
4. **Model Eğitimi:** Logistic Regression modeli eğitilir
5. **Değerlendirme:** Cross-validation ile performans ölçülür
6. **Kaydetme:** Model ve bileşenler kaydedilir

## 🔐 Güvenlik Özellikleri

- ✅ Input validation
- ✅ Rate limiting
- ✅ CORS middleware
- ✅ Error handling
- ✅ Logging

## 📝 Örnek Kullanım Senaryosu

### Senaryo: Yeni Müşteri Şikayetlerini Topla ve Modeli Eğit

```python
import requests
import json

# 1. Şikayetleri topla
complaints = [
    {'text': 'Ürün kalitesi çok kötü, bozuk geldi', 'source': 'email'},
    {'text': 'Teslimat çok geç oldu, 2 hafta beklettiler', 'source': 'chat'},
    {'text': 'Müşteri hizmetleri çok kaba davrandı', 'source': 'phone'},
    {'text': 'Yanlış ürün göndermiş, başka şey istemiştim', 'source': 'email'},
    {'text': 'Paket ezik geldi, ürün hasar görmüş', 'source': 'manual'},
]

# 2. Her şikayeti ekle
for complaint in complaints:
    response = requests.post(
        'http://localhost:8000/collect/complaint',
        json=complaint
    )
    print(f"✅ {complaint['text'][:30]}... - {response.json()['complaint']['category']}")

# 3. Toplanan verileri kontrol et
data_response = requests.get('http://localhost:8000/collect/data')
data = data_response.json()
print(f"\n📊 Toplam şikayet: {data['total_complaints']}")
print(f"Kategori dağılımı: {data['category_distribution']}")

# 4. Modeli eğit
train_response = requests.post(
    'http://localhost:8000/train',
    json={
        'complaints': data['complaints'],
        'save_model': True
    }
)
print(f"\n🎓 Model eğitimi tamamlandı!")
print(f"Test doğruluğu: {train_response.json()['training_results']['training_results']['test_accuracy']:.1%}")
```

## 🐛 Sorun Giderme

### Problem: "ModuleNotFoundError: No module named 'fastapi'"

**Çözüm:**

```bash
python -m pip install -r requirements.txt
```

### Problem: "API bağlantısı kurulamadı"

**Çözüm:**

1. API sunucusunun çalıştığını kontrol edin: `python api.py`
2. Port 8000'in açık olduğunu kontrol edin
3. Firewall ayarlarını kontrol edin

### Problem: "Hiç veri toplanamadı"

**Çözüm:**

1. Şikayet metinlerinin en az 5 karakter olduğundan emin olun
2. Metin boş olmadığından emin olun
3. API yanıtını kontrol edin

## 📚 Ek Kaynaklar

- **API Dokümantasyonu:** `http://localhost:8000/docs`
- **README:** `README.md`
- **Deployment Rehberi:** `deployment_guide.md`
- **Türkiye Optimizasyon:** `turkey_optimized_dataset_strategy.md`

## 🎯 Sonraki Adımlar

1. **Gerçek Veri Entegrasyonu:** Google Maps, Şikayetvar.com gibi kaynaklardan veri toplama
2. **BERT Fine-tuning:** Daha iyi performans için BERT modeli eğitimi
3. **Dashboard Geliştirme:** Detaylı analiz dashboard'u
4. **Deployment:** Docker ve Kubernetes ile production deployment

---

**Son Güncelleme:** 2024-12-08  
**Versiyon:** 1.0.0  
**Durum:** ✅ Aktif ve Kullanıma Hazır
