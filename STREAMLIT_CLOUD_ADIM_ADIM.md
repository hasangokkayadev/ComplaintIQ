# 🚀 Streamlit Cloud'a Yayınlama - Adım Adım Rehberi

## 📋 Ön Koşullar

- [ ] GitHub hesabı (https://github.com)
- [ ] Streamlit Cloud hesabı (https://streamlit.io/cloud)
- [ ] Proje GitHub'da yüklü

---

## 🔧 Adım 1: GitHub'a Proje Yükle

### 1.1 GitHub Repository Oluştur

1. https://github.com/new adresine git
2. Repository adı: `complaintiq`
3. Açıklama: "AI-powered complaint categorization system"
4. Public seç (Streamlit Cloud public repo'ları tercih eder)
5. "Create repository" butonuna tıkla

### 1.2 Projeyi GitHub'a Push Et

```bash
# Proje dizininde
cd d:\ComplaintIQ

# Git repository oluştur
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit - ComplaintIQ v1.0"

# GitHub'a bağla (YOUR_USERNAME yerine kendi kullanıcı adını yaz)
git remote add origin https://github.com/YOUR_USERNAME/complaintiq.git

# Main branch'e push et
git branch -M main
git push -u origin main
```

### 1.3 GitHub'da Kontrol Et

1. https://github.com/YOUR_USERNAME/complaintiq adresine git
2. Tüm dosyaların yüklendiğini kontrol et
3. `app.py` dosyasını gör

---

## 🌐 Adım 2: Streamlit Cloud Hesabı Oluştur

### 2.1 Streamlit Cloud'a Kaydol

1. https://streamlit.io/cloud adresine git
2. "Sign up" butonuna tıkla
3. "Continue with GitHub" seç
4. GitHub hesabınla giriş yap
5. Streamlit Cloud'a erişim izni ver

### 2.2 Hesabı Doğrula

1. Email adresini doğrula
2. Profil bilgilerini tamamla
3. Dashboard'a erişim sağlandığını kontrol et

---

## 🚀 Adım 3: Uygulamayı Deploy Et

### 3.1 Streamlit Cloud Dashboard'a Git

1. https://share.streamlit.io adresine git
2. Giriş yap
3. "New app" butonuna tıkla

### 3.2 Deploy Ayarlarını Yap

**Repository seç:**

- Repository: `YOUR_USERNAME/complaintiq`
- Branch: `main`
- Main file path: `app.py`

**Advanced settings (opsiyonel):**

- Python version: `3.12`
- Custom domain: `complaintiq` (opsiyonel)

### 3.3 Deploy Et

1. "Deploy" butonuna tıkla
2. Deployment başlayacak (2-3 dakika sürer)
3. "Your app is ready!" mesajını bekle

---

## 🔐 Adım 4: Secrets Ayarla

### 4.1 Streamlit Cloud'da Secrets Ekle

1. Uygulamayı seç
2. Sağ üstte "⋮" (üç nokta) menüsüne tıkla
3. "Settings" seç
4. "Secrets" sekmesine tıkla

### 4.2 Secrets Dosyasını Yapıştır

Aşağıdaki içeriği "Secrets" alanına yapıştır:

```toml
# API Configuration
api_url = "http://localhost:8000"
api_key = "your-secret-key"

# Database
database_url = "sqlite:///./complaintiq.db"

# Email
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your-email@gmail.com"
smtp_password = "your-app-password"
```

### 4.3 Kaydet

1. "Save" butonuna tıkla
2. Uygulama otomatik olarak yeniden başlayacak

---

## ✅ Adım 5: Uygulamayı Test Et

### 5.1 Uygulamaya Erişim

Deployment tamamlandıktan sonra:

- **URL:** https://complaintiq.streamlit.app
- **Veya:** https://YOUR_USERNAME-complaintiq.streamlit.app

### 5.2 Temel Testler

- [ ] Uygulamayı aç
- [ ] Sidebar'ı kontrol et
- [ ] Tahmin sayfasını test et
- [ ] Veri toplama sayfasını test et
- [ ] Analytics sayfasını kontrol et

### 5.3 API Bağlantısını Test Et

Eğer API başka sunucuda çalışıyorsa:

1. API'nin çalıştığını kontrol et
2. API URL'sini secrets'e ekle
3. Tahmin yap
4. Hata mesajını kontrol et

---

## 🔄 Adım 6: Güncellemeleri Deploy Et

### 6.1 Yerel Değişiklik Yap

```bash
# Dosyaları düzenle
# Örneğin: app.py

# Değişiklikleri commit et
git add .
git commit -m "Update: Yeni özellik eklendi"

# GitHub'a push et
git push origin main
```

### 6.2 Streamlit Cloud Otomatik Deploy

1. GitHub'a push ettikten sonra
2. Streamlit Cloud otomatik olarak yeni versiyonu deploy eder
3. 1-2 dakika içinde güncelleme canlı olur

### 6.3 Deployment Durumunu Kontrol Et

1. Streamlit Cloud dashboard'a git
2. Uygulamayı seç
3. "Manage app" → "View logs" seç
4. Deployment durumunu kontrol et

---

## 🎯 Adım 7: Custom Domain Bağla (Opsiyonel)

### 7.1 Domain Satın Al

1. Godaddy, Namecheap vb. sitelerden domain satın al
2. Örneğin: `complaintiq.com`

### 7.2 DNS Ayarlarını Yap

1. Domain sağlayıcısında DNS ayarlarına git
2. CNAME kaydı ekle:
   - **Name:** `www`
   - **Value:** `YOUR_USERNAME-complaintiq.streamlit.app`

### 7.3 Streamlit Cloud'da Domain Bağla

1. Streamlit Cloud dashboard'a git
2. Uygulamayı seç
3. "Settings" → "Custom domain" seç
4. Domain adını gir: `www.complaintiq.com`
5. "Save" butonuna tıkla

---

## 🔐 Adım 8: Güvenlik Ayarları

### 8.1 CORS Ayarları (API'de)

Eğer API başka sunucuda çalışıyorsa, `api.py`'de CORS ayarlarını yap:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://complaintiq.streamlit.app",
        "https://YOUR_USERNAME-complaintiq.streamlit.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 8.2 API Key Doğrulaması

```python
@app.post("/predict")
async def predict(request: PredictRequest, x_api_key: str = Header(None)):
    if x_api_key != st.secrets.get("api_key"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... tahmin yap
```

### 8.3 Rate Limiting

```python
# app.py
import streamlit as st
from datetime import datetime, timedelta

if "last_request" not in st.session_state:
    st.session_state.last_request = datetime.now()

if datetime.now() - st.session_state.last_request < timedelta(seconds=1):
    st.warning("Çok hızlı istek gönderiyorsunuz")
else:
    st.session_state.last_request = datetime.now()
    # ... istek gönder
```

---

## 📊 Adım 9: Monitoring ve Logging

### 9.1 Logs'u Kontrol Et

1. Streamlit Cloud dashboard'a git
2. Uygulamayı seç
3. "Manage app" → "View logs" seç
4. Hataları kontrol et

### 9.2 Sentry ile Error Tracking

```python
# app.py
import sentry_sdk

sentry_sdk.init(
    dsn=st.secrets.get("sentry_dsn"),
    traces_sample_rate=1.0
)
```

---

## 🐛 Adım 10: Sorun Giderme

### Sorun: "ModuleNotFoundError"

```
Hata: ModuleNotFoundError: No module named 'fastapi'
Çözüm: requirements.txt'e fastapi ekle ve GitHub'a push et
```

### Sorun: "Connection refused"

```
Hata: Connection refused (API bağlantı hatası)
Çözüm:
1. API'nin çalıştığını kontrol et
2. API URL'sini secrets'e ekle
3. CORS ayarlarını kontrol et
```

### Sorun: "App is sleeping"

```
Hata: App is sleeping (Streamlit Cloud uyku modu)
Çözüm:
1. Streamlit Cloud Pro'ya yükselt
2. Veya API'yi ayrı sunucuda çalıştır
```

### Sorun: "Timeout"

```
Hata: Request timeout
Çözüm:
1. API'nin yanıt süresini azalt
2. Cache kullan
3. Async işlemler kullan
```

---

## ✅ Deployment Checklist

- [ ] GitHub hesabı oluşturuldu
- [ ] Proje GitHub'a yüklendi
- [ ] Streamlit Cloud hesabı oluşturuldu
- [ ] Uygulamayı deploy ettim
- [ ] Secrets ayarlandı
- [ ] Uygulamayı test ettim
- [ ] API bağlantısı çalışıyor
- [ ] Custom domain bağlandı (opsiyonel)
- [ ] Güvenlik ayarları yapıldı
- [ ] Monitoring ayarlandı

---

## 🎉 Başarılı Deployment!

Tebrikler! Uygulamanız Streamlit Cloud'da canlı!

### Erişim Bilgileri

- **URL:** https://complaintiq.streamlit.app
- **GitHub:** https://github.com/YOUR_USERNAME/complaintiq
- **Streamlit Cloud:** https://share.streamlit.io

### Sonraki Adımlar

1. Uygulamayı sosyal medyada paylaş
2. Kullanıcı geri bildirimi topla
3. Yeni özellikler ekle
4. Model performansını iyileştir

---

## 📞 Destek

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Community:** https://discuss.streamlit.io
- **GitHub Issues:** https://github.com/YOUR_USERNAME/complaintiq/issues

---

**Son Güncelleme:** 2025-12-09
**Versiyon:** 1.0
