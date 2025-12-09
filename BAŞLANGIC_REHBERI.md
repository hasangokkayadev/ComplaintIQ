# 🚀 ComplaintIQ - Başlangıç Rehberi

## 📋 Uygulamayı Çalıştırmak İçin Yapmanız Gerekenler

### ✅ Adım 1: İlk Terminal Açın

1. **Windows Başlat Menüsü**'nü açın
2. **cmd** yazın ve **Command Prompt** açın
3. Aşağıdaki komutu yazın:

```bash
cd d:\ComplaintIQ
```

4. **Enter** tuşuna basın

### ✅ Adım 2: API Sunucusunu Başlatın

Aynı terminal'de aşağıdaki komutu yazın:

```bash
python api.py
```

5. **Enter** tuşuna basın

**Beklenen Çıktı:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Eğer bu mesajı görürseniz, API sunucusu başarıyla çalışıyor demektir! ✅

**Bu terminal'i açık tutun!**

---

### ✅ Adım 3: İkinci Terminal Açın

1. **Yeni bir Command Prompt penceresi açın** (Windows Başlat → cmd)
2. Aşağıdaki komutu yazın:

```bash
cd d:\ComplaintIQ
```

3. **Enter** tuşuna basın

### ✅ Adım 4: Streamlit Frontend'ini Başlatın

Aynı terminal'de aşağıdaki komutu yazın:

```bash
streamlit run app.py
```

4. **Enter** tuşuna basın

**Beklenen Çıktı:**

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

Eğer bu mesajı görürseniz, Streamlit başarıyla çalışıyor demektir! ✅

**Bu terminal'i de açık tutun!**

---

## 🌐 Adım 5: Browser'da Uygulamayı Açın

### Seçenek 1: Streamlit Frontend (Önerilen)

1. **Google Chrome** veya **Microsoft Edge** açın
2. Adres çubuğuna yazın:

```
http://localhost:8501
```

3. **Enter** tuşuna basın

### Seçenek 2: API Dokümantasyonu

1. Browser'da yeni sekme açın
2. Adres çubuğuna yazın:

```
http://localhost:8000/docs
```

3. **Enter** tuşuna basın

---

## 🎯 Uygulamayı Kullanmaya Başlayın

### Streamlit Frontend'de (http://localhost:8501)

#### 1️⃣ Ana Sayfa

- Sistem hakkında bilgi alın
- Desteklenen kategorileri görün
- Örnek tahmin deneyin

#### 2️⃣ Tekil Tahmin (🔍)

- Bir şikayet metni yazın
- "🎯 Kategori Tahmini Yap" butonuna tıklayın
- Sonucu göreceksiniz

**Örnek Metinler:**

- "Ürün teslim edilmemiş, çok uzun sürdü"
- "Ürün kalitesi çok kötü, bozuk geldi"
- "Müşteri hizmetleri çok kaba davrandı"
- "Yanlış ürün göndermiş, başka şey istemiştim"

#### 3️⃣ Toplu İşlem (📊)

- Birden fazla şikayeti aynı anda işleyin
- CSV dosyası yükleyin veya manuel giriş yapın
- Sonuçları indirin

#### 4️⃣ Veri Toplama (💾) - YENİ!

- **Şikayet Ekle:** Yeni şikayetler toplayın
- **Toplanan Veriler:** Topladığınız şikayetleri görün
- **Model Eğit:** Modeli yeniden eğitin

#### 5️⃣ Analiz ve Raporlar (📈)

- Model istatistiklerini görün
- Kategori bilgilerini öğrenin
- Performance metriklerini kontrol edin

#### 6️⃣ Sistem Bilgileri (⚙️)

- Teknik detayları öğrenin
- Deployment bilgilerini görün
- Güvenlik özelliklerini kontrol edin

---

## 🧪 Test Senaryoları

### Senaryo 1: Basit Tahmin

1. **Tekil Tahmin** sayfasına gidin
2. Metin alanına yazın: `Ürün teslim edilmemiş`
3. "🎯 Kategori Tahmini Yap" butonuna tıklayın
4. Sonucu göreceksiniz

### Senaryo 2: Veri Toplama

1. **Veri Toplama** sayfasına gidin
2. **Şikayet Ekle** sekmesinde:
   - Metin yazın: `Müşteri hizmetleri çok kaba davrandı`
   - Kategori: "Müşteri Hizmetleri Sorunu" seçin
   - Veri kaynağı: "Manual" seçin
   - "➕ Şikayet Ekle" butonuna tıklayın
3. Başarı mesajı göreceksiniz

### Senaryo 3: Toplanan Verileri Görüntüleme

1. **Veri Toplama** sayfasında **Toplanan Veriler** sekmesine gidin
2. "🔄 Verileri Yenile" butonuna tıklayın
3. Kategori dağılımını göreceksiniz

### Senaryo 4: Model Eğitimi

1. **Veri Toplama** sayfasında **Model Eğit** sekmesine gidin
2. "🎓 Modeli Eğit" butonuna tıklayın
3. Model eğitilecektir

---

## 📊 Desteklenen Kategoriler

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

## 🐛 Sorun Giderme

### Problem: "Bağlantı reddedildi" hatası

**Çözüm:**

1. Terminal 1'de API sunucusunun çalıştığını kontrol edin
2. Eğer çalışmıyorsa, `python api.py` komutunu çalıştırın
3. Browser'ı yenileyin (F5)

### Problem: "Streamlit bağlantısı kurulamadı"

**Çözüm:**

1. Terminal 2'de Streamlit'in çalıştığını kontrol edin
2. Eğer çalışmıyorsa, `streamlit run app.py` komutunu çalıştırın
3. Browser'ı yenileyin (F5)

### Problem: "ModuleNotFoundError"

**Çözüm:**

1. Terminal'de Ctrl+C tuşlarına basarak uygulamayı durdurun
2. Aşağıdaki komutu çalıştırın:

```bash
python -m pip install fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

3. Tekrar `python api.py` veya `streamlit run app.py` komutunu çalıştırın

---

## 📞 Hızlı Referans

| İşlem                  | URL                          | Açıklama          |
| ---------------------- | ---------------------------- | ----------------- |
| **Streamlit Frontend** | http://localhost:8501        | Kullanıcı arayüzü |
| **API Dokümantasyonu** | http://localhost:8000/docs   | Swagger UI        |
| **API Health Check**   | http://localhost:8000/health | Sunucu durumu     |

---

## ✅ Kontrol Listesi

- [ ] Terminal 1'de `python api.py` çalışıyor
- [ ] Terminal 2'de `streamlit run app.py` çalışıyor
- [ ] http://localhost:8501 açılıyor
- [ ] Tekil tahmin çalışıyor
- [ ] Veri toplama çalışıyor
- [ ] Model eğitimi çalışıyor

---

## 🎓 Sonraki Adımlar

1. **Veri Toplama:** Müşteri şikayetlerini toplayın
2. **Model Eğitimi:** Topladığınız verilerle modeli eğitin
3. **Analiz:** Sonuçları analiz edin
4. **Deployment:** Uygulamayı production'a dağıtın

---

**Başarılar! 🎉**

Herhangi bir sorun yaşarsanız, `BROWSER_TEST_REHBERI.md` dosyasını kontrol edin.

**Proje Konumu:** `d:\ComplaintIQ`  
**Versiyon:** 1.0.0  
**Durum:** ✅ Kullanıma Hazır
