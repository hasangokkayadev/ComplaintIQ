# 🌐 ComplaintIQ - Browser Test Rehberi

## 📋 Genel Bakış

Bu rehber, ComplaintIQ projesini browser'da nasıl test edeceğinizi adım adım anlatır.

## 🚀 Hızlı Başlangıç (3 Adım)

### Adım 1: Terminal 1'de API Sunucusunu Başlat

```bash
cd d:\ComplaintIQ
python api.py
```

**Beklenen Çıktı:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Adım 2: Terminal 2'de Streamlit Frontend'ini Başlat

```bash
cd d:\ComplaintIQ
streamlit run app.py
```

**Beklenen Çıktı:**

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Adım 3: Browser'da Açın

- **API Dokümantasyonu:** http://localhost:8000/docs
- **Streamlit Frontend:** http://localhost:8501
- **Test Sayfası:** file:///d:/ComplaintIQ/test_browser.html

---

## 🔗 Browser Bağlantıları

### 1. API Dokümantasyonu (Swagger UI)

**URL:** `http://localhost:8000/docs`

**Özellikler:**

- Tüm API endpoint'lerini görebilirsiniz
- Endpoint'leri doğrudan test edebilirsiniz
- Request/Response örneklerini görebilirsiniz

**Test Etmek İçin:**

1. `/predict` endpoint'ini açın
2. "Try it out" butonuna tıklayın
3. Aşağıdaki JSON'u girin:

```json
{
  "text": "Ürün teslim edilmemiş, çok uzun sürdü"
}
```

4. "Execute" butonuna tıklayın

### 2. Streamlit Frontend

**URL:** `http://localhost:8501`

**Sayfalar:**

- 🏠 **Ana Sayfa** - Sistem özeti ve özellikler
- 🔍 **Tekil Tahmin** - Tek şikayet tahmini
- 📊 **Toplu İşlem** - Birden fazla şikayet işleme
- 💾 **Veri Toplama** - Şikayet toplama ve model eğitimi
- 📈 **Analiz ve Raporlar** - Detaylı analiz
- ⚙️ **Sistem Bilgileri** - Teknik bilgiler

### 3. Test Sayfası (HTML)

**URL:** `file:///d:/ComplaintIQ/test_browser.html`

**Özellikler:**

- Tüm API endpoint'lerini test edebilirsiniz
- Sonuçları JSON formatında görebilirsiniz
- Hızlı test butonları

---

## 📝 API Endpoint'leri

### 1. Tekil Tahmin

**Endpoint:** `POST /predict`

**Request:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Ürün teslim edilmemiş"}'
```

**Response:**

```json
{
  "prediction": "Kargo Gecikmesi",
  "confidence": 0.95,
  "all_probabilities": {
    "Kargo Gecikmesi": 0.95,
    "Ürün Kalite Sorunu": 0.03,
    ...
  },
  "text_length": 25,
  "word_count": 4
}
```

### 2. Toplu Tahmin

**Endpoint:** `POST /batch_predict`

**Request:**

```bash
curl -X POST "http://localhost:8000/batch_predict" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Ürün kalitesi çok kötü",
      "Teslimat çok geç oldu",
      "Yanlış ürün göndermiş"
    ]
  }'
```

### 3. Şikayet Ekleme

**Endpoint:** `POST /collect/complaint`

**Request:**

```bash
curl -X POST "http://localhost:8000/collect/complaint" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Müşteri hizmetleri çok kaba davrandı",
    "category": null,
    "source": "manual"
  }'
```

### 4. Toplanan Verileri Görüntüleme

**Endpoint:** `GET /collect/data`

**Request:**

```bash
curl "http://localhost:8000/collect/data"
```

### 5. Modeli Eğitme

**Endpoint:** `POST /train`

**Request:**

```bash
curl -X POST "http://localhost:8000/train" \
  -H "Content-Type: application/json" \
  -d '{
    "complaints": [
      {"text": "Ürün kalitesi çok kötü", "source": "manual"},
      {"text": "Teslimat çok geç oldu", "source": "manual"}
    ],
    "save_model": true
  }'
```

---

## 🧪 Streamlit Frontend Test Senaryoları

### Senaryo 1: Tekil Tahmin Yapma

1. **Ana Sayfa**'ya gidin
2. "🚀 Örnek Tahmin Dene" butonuna tıklayın
3. Sonucu göreceksiniz

### Senaryo 2: Toplu İşlem

1. **Toplu İşlem** sayfasına gidin
2. **CSV Dosyası** sekmesinde örnek CSV yükleyin veya
3. **Manuel Giriş** sekmesinde 5 şikayet yazın
4. "🚀 Seçili Metinleri İşle" butonuna tıklayın
5. Sonuçları göreceksiniz

### Senaryo 3: Veri Toplama

1. **Veri Toplama** sayfasına gidin
2. **Şikayet Ekle** sekmesinde:
   - Şikayet metni yazın
   - Kategori seçin (opsiyonel)
   - Veri kaynağı seçin
   - "➕ Şikayet Ekle" butonuna tıklayın
3. **Toplanan Veriler** sekmesinde:
   - "🔄 Verileri Yenile" butonuna tıklayın
   - Kategori dağılımını göreceksiniz
4. **Model Eğit** sekmesinde:
   - "🎓 Modeli Eğit" butonuna tıklayın
   - Model eğitilecektir

---

## 🐛 Sorun Giderme

### Problem 1: "API bağlantısı kurulamadı"

**Çözüm:**

1. API sunucusunun çalıştığını kontrol edin
2. Terminal 1'de `python api.py` komutunu çalıştırın
3. Port 8000'in açık olduğunu kontrol edin

### Problem 2: "ModuleNotFoundError"

**Çözüm:**

```bash
python -m pip install fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

### Problem 3: "Streamlit bağlantısı kurulamadı"

**Çözüm:**

1. Terminal 2'de `streamlit run app.py` komutunu çalıştırın
2. Port 8501'in açık olduğunu kontrol edin

### Problem 4: "Model yükleme hatası"

**Çözüm:**

- Mock model kullanılıyor, bu normal
- Gerçek model eğitmek için veri toplama yapın

---

## 📊 Test Sonuçları Örneği

### Tekil Tahmin Sonucu

```json
{
  "prediction": "Kargo Gecikmesi",
  "confidence": 0.95,
  "all_probabilities": {
    "Kargo Gecikmesi": 0.95,
    "Ürün Kalite Sorunu": 0.02,
    "Müşteri Hizmetleri Sorunu": 0.01,
    "Yanlış Ürün": 0.01,
    "Eksik Ürün": 0.01
  },
  "text_length": 25,
  "word_count": 4
}
```

### Veri Toplama Sonucu

```json
{
  "status": "success",
  "complaint": {
    "text": "Müşteri hizmetleri çok kaba davrandı",
    "category": "Müşteri Hizmetleri Sorunu",
    "confidence": 0.92,
    "source": "manual",
    "date": "2024-12-08T19:30:00"
  },
  "message": "Şikayet başarıyla toplandı"
}
```

---

## 🎯 Desteklenen Kategoriler

1. ✅ Ürün Kalite Sorunu
2. ✅ Yanlış Ürün
3. ✅ Eksik Ürün
4. ✅ Kargo Gecikmesi
5. ✅ Kargo Firması Problemi
6. ✅ İade/Değişim Sorunu
7. ✅ Ödeme/Fatura Sorunu
8. ✅ Müşteri Hizmetleri Sorunu
9. ✅ Paketleme/Ambalaj Problemi
10. ✅ Ürün Açıklaması Yanıltıcı
11. ✅ Hizmet Kalite Sorunu
12. ✅ Teknik/Uygulama Sorunu

---

## 📚 Ek Kaynaklar

- **API Dokümantasyonu:** http://localhost:8000/docs
- **Veri Toplama Rehberi:** `DATA_COLLECTION_GUIDE.md`
- **Proje Birleştirme Özeti:** `PROJE_BIRLEŞTIRME_ÖZETI.md`
- **Deployment Rehberi:** `deployment_guide.md`

---

## ✅ Kontrol Listesi

- [ ] API sunucusu çalışıyor (Terminal 1)
- [ ] Streamlit frontend çalışıyor (Terminal 2)
- [ ] http://localhost:8000/docs açılıyor
- [ ] http://localhost:8501 açılıyor
- [ ] Tekil tahmin çalışıyor
- [ ] Toplu tahmin çalışıyor
- [ ] Şikayet ekleme çalışıyor
- [ ] Veri görüntüleme çalışıyor
- [ ] Model eğitimi çalışıyor

---

**Son Güncelleme:** 2024-12-08  
**Versiyon:** 1.0.0  
**Durum:** ✅ Aktif ve Kullanıma Hazır
