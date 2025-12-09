# 📁 Data Klasör Yapısı Açıklaması

## 🔍 Mevcut Durum

```
data/
├── raw/                    # ✅ Ham veri dosyaları
│   └── customer_complaints.csv
├── processed/              # ❌ Henüz boş - İşlenmemiş
└── [diğer alt klasörler]
```

## 📊 Raw Data (Mevcut)

**`data/raw/customer_complaints.csv`** ✅

- Ham müşteri şikayet verisi
- 11 sütun: customer_id, complaint_text, complaint_category, vb.
- ~20 satır örnek veri
- Model eğitimi için hazır

## 🚀 Processed Data (Boş - Normal!)

**`data/processed/`** ❌

- **Neden boş?** Notebook'lar henüz çalıştırılmadı
- **Ne zaman dolacak?** Model eğitimi sonrası

## 🔄 Model Eğitimi Sonrası Beklenen Yapı

### Processed Data:

```
data/processed/
├── processed_complaints.csv     # Temizlenmiş, işlenmiş veri
├── train_test_split_data/      # Eğitim/test bölünmüş veriler
├── feature_engineered_data.csv # Özellik mühendisliği uygulanmış veri
└── [ara işleme dosyaları]
```

### Models:

```
models/
├── final_model.pkl             # Eğitilmiş Logistic Regression model
├── tfidf_vectorizer.pkl        # TF-IDF vektörleştirici
├── feature_scaler.pkl          # StandardScaler
├── pipeline_metadata.json      # Model meta verileri
└── model_performance.json      # Performans metrikleri
```

## 📈 Model Eğitimi Süreci

### 1. **Veri Yükleme** (Raw → Memory)

- CSV dosyasını okuma
- DataFrame oluşturma
- İlk veri analizi

### 2. **Veri Ön İşleme**

- Metin temizleme
- Eksik değer kontrolü
- Kategori dağılım analizi

### 3. **Özellik Mühendisliği**

- TF-IDF vektörleştirme
- Sayısal özellikler (text_length, word_count)
- Özellik birleştirme

### 4. **Model Eğitimi**

- Train/test split
- Logistic Regression eğitimi
- Cross-validation

### 5. **Model Kaydetme**

- `models/` klasörüne pickle formatında kaydetme
- `data/processed/` klasörüne işlenmiş veriler

## 🛠️ Nasıl Doldurulur?

### Yöntem 1: Python Script

```python
from src.pipeline import run_pipeline

# Tam pipeline çalıştır
result = run_pipeline()
print(f"Model eğitimi tamamlandı!")
print(f"Kaydedilen dosyalar: {list(result['saved_paths'].keys())}")
```

### Yöntem 2: Jupyter Notebook

```bash
jupyter notebook notebooks/06_Final_Pipeline.ipynb
# Hücreleri sırayla çalıştır
```

### Yöntem 3: Diğer Notebook'lar

```bash
jupyter notebook notebooks/
# 01_EDA.ipynb - Veri analizi
# 02_Baseline.ipynb - Baseline model
# 03_Feature_Engineering.ipynb - Özellik mühendisliği
# 04_Model_Optimization.ipynb - Model optimizasyonu
# 05_Model_Evaluation.ipynb - Değerlendirme
```

## ✅ Sonuç

**Processed klasörü boş olması tamamen normal!**

- ✅ Raw data mevcut ve hazır
- ✅ Pipeline kodu yazılmış
- ⏳ Sadece notebook'ları çalıştırmak gerekiyor
- 🚀 Model eğitimi sonrası tüm dosyalar oluşacak

Bu, projenin **henüz kullanıma hazır olmadığını** değil, sadece **model eğitiminin yapılmadığını** gösterir.
