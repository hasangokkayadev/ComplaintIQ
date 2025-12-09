# 🚀 Deploy Rehberi - Gerçek Model ile

## 📋 Adım Adım Model Eğitimi ve Deploy

### 1. 🔧 Model Eğitimi (En Önemli Adım)

#### Notebook ile Eğitim:

```bash
# 1. Jupyter Notebook'u başlat
jupyter notebook notebooks/06_Final_Pipeline.ipynb

# 2. Notebook'ta hücreleri sırayla çalıştır
# - Veri yükleme
# - Özellik mühendisliği
# - Model eğitimi
# - Model kaydetme
```

#### Python Script ile Eğitim:

```bash
# Doğrudan pipeline çalıştır
python -c "
from src.pipeline import run_pipeline
result = run_pipeline()
print('Model eğitimi tamamlandı!')
print(f'Kaydedilen dosyalar: {list(result[\"saved_paths\"].keys())}')
"
```

### 2. ✅ Model Dosyalarını Kontrol Et

Models klasöründe bu dosyalar olmalı:

```
models/
├── final_model.pkl           # Eğitilmiş model
├── tfidf_vectorizer.pkl      # TF-IDF vektörleştirici
├── feature_scaler.pkl        # Özellik ölçeklendirici
└── pipeline_metadata.json    # Model meta verileri
```

### 3. 🧪 Model Test Et

```python
# Model test
from src.inference import classifier
result = classifier.predict_single('Ürün teslim edilmemiş')
print(f"Tahmin: {result['prediction']}")
print(f"Güven: {result['confidence']:.2f}")
```

### 4. 🌐 API Başlat

```bash
# API'yi başlat
python api.py

# Test et
curl http://localhost:8000/health
```

### 5. 💻 Frontend Başlat

```bash
# Streamlit uygulamasını başlat
streamlit run app.py
```

## 🎯 Beklenen Sonuçlar

### Model Performansı:

- **Doğruluk:** %85+
- **F1-Score:** %83+
- **Tahmin Süresi:** < 100ms

### Kategoriler:

1. Delivery Issues
2. Billing Issues
3. Product Quality
4. Customer Service
5. Technical Support
6. Return/Refund
7. Website Issues
8. Service Outage
9. Fraud Issues

## 🔍 Sorun Giderme

### Hata: "Model dosyası bulunamadı"

- Pipeline'ın çalıştırıldığından emin ol
- Models klasörünün oluştuğunu kontrol et

### Hata: "FastAPI bulunamadı"

```bash
pip install fastapi streamlit uvicorn pydantic
```

### Hata: "Port zaten kullanımda"

```bash
# Farklı port kullan
python -c "from src.config import API_CONFIG; API_CONFIG['port'] = 8001"
```

## 🎉 Başarılı Deploy!

Tüm adımlar tamamlandığında:

- ✅ API: http://localhost:8000/docs
- ✅ Frontend: http://localhost:8501
- ✅ Model: Gerçek performans ile çalışıyor
- ✅ Endpoints: Tüm API endpoint'leri aktif
