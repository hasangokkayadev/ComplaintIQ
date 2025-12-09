# 🚀 Streamlit Cloud'a Yayınlama Rehberi

## 📌 Hızlı Başlangıç (10 Dakika)

### Adım 1: GitHub'a Proje Yükle

```bash
# Proje dizininde
cd d:\ComplaintIQ

# Git repository oluştur
git init
git add .
git commit -m "Initial commit - ComplaintIQ"

# GitHub'a push et
git remote add origin https://github.com/YOUR_USERNAME/complaintiq.git
git branch -M main
git push -u origin main
```

### Adım 2: Streamlit Cloud Hesabı Oluştur

1. https://streamlit.io/cloud adresine git
2. "Sign up" butonuna tıkla
3. GitHub hesabınla giriş yap
4. Streamlit Cloud'a erişim izni ver

### Adım 3: Uygulamayı Deploy Et

1. Streamlit Cloud dashboard'a git
2. "New app" butonuna tıkla
3. Aşağıdaki bilgileri gir:

   - **Repository:** YOUR_USERNAME/complaintiq
   - **Branch:** main
   - **Main file path:** app.py

4. "Deploy" butonuna tıkla

### Adım 4: Uygulamaya Erişim

Deployment tamamlandıktan sonra:

- **URL:** https://complaintiq.streamlit.app
- **Veya:** https://YOUR_USERNAME-complaintiq.streamlit.app

---

## 🔧 Streamlit Konfigürasyonu

### `.streamlit/config.toml` Oluştur

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
toolbarMode = "minimal"

[logger]
level = "info"

[server]
port = 8501
headless = true
runOnSave = true
maxUploadSize = 200
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### `.streamlit/secrets.toml` Oluştur (Yerel)

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

### Streamlit Cloud'da Secrets Ayarla

1. Streamlit Cloud dashboard'a git
2. Uygulamayı seç
3. "Settings" → "Secrets" tıkla
4. Aşağıdaki secrets'i ekle:

```toml
# API Configuration
api_url = "https://your-api-domain.com"
api_key = "your-production-key"

# Database
database_url = "postgresql://user:password@host/db"

# Email
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "your-email@gmail.com"
smtp_password = "your-app-password"
```

---

## 📦 Bağımlılıklar

### `requirements.txt` Kontrol Et

```bash
# Gerekli paketler
streamlit>=1.28.0
fastapi>=0.104.0
uvicorn>=0.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
plotly>=5.17.0
requests>=2.31.0
python-multipart>=0.0.6
pydantic>=2.0.0
```

### Streamlit Cloud'da Kurulum

Streamlit Cloud otomatik olarak `requirements.txt`'i okur ve bağımlılıkları yükler.

---

## 🌐 API Bağlantısı

### Seçenek 1: Aynı Sunucuda (Önerilen)

Eğer API ve Frontend aynı sunucuda çalışıyorsa:

```python
# app.py
import streamlit as st
import requests
import os

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# API'ye istek gönder
response = requests.post(
    f"{API_URL}/predict",
    json={"text": "Şikayet metni"}
)
```

### Seçenek 2: Farklı Sunucuda

Eğer API başka bir sunucuda çalışıyorsa:

```python
# app.py
import streamlit as st
import requests
import os

# Streamlit Cloud'dan API URL'sini oku
API_URL = st.secrets.get("api_url", "http://localhost:8000")

# API'ye istek gönder
try:
    response = requests.post(
        f"{API_URL}/predict",
        json={"text": "Şikayet metni"},
        timeout=10
    )
    result = response.json()
except requests.exceptions.RequestException as e:
    st.error(f"API bağlantı hatası: {e}")
```

---

## 🔐 Güvenlik Ayarları

### 1. CORS Ayarları (API'de)

```python
# api.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "https://complaintiq.streamlit.app",
        "https://YOUR_USERNAME-complaintiq.streamlit.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. API Key Doğrulaması

```python
# api.py
from fastapi import Header, HTTPException

@app.post("/predict")
async def predict(request: PredictRequest, x_api_key: str = Header(None)):
    if x_api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    # ... tahmin yap
```

### 3. Rate Limiting

```python
# app.py
import streamlit as st
from datetime import datetime, timedelta

# Session state'de rate limiting
if "last_request" not in st.session_state:
    st.session_state.last_request = datetime.now()

# 1 saniye bekleme
if datetime.now() - st.session_state.last_request < timedelta(seconds=1):
    st.warning("Çok hızlı istek gönderiyorsunuz. Lütfen bekleyin.")
else:
    st.session_state.last_request = datetime.now()
    # ... istek gönder
```

---

## 📊 Monitoring ve Logging

### Streamlit Cloud Logs

```bash
# Streamlit Cloud dashboard'da
# Uygulamayı seç → "Manage app" → "View logs"
```

### Sentry ile Error Tracking

```python
# app.py
import sentry_sdk

sentry_sdk.init(
    dsn=st.secrets.get("sentry_dsn"),
    traces_sample_rate=1.0
)

try:
    # Uygulamayı çalıştır
    pass
except Exception as e:
    sentry_sdk.capture_exception(e)
    st.error("Bir hata oluştu")
```

---

## 🚀 Deployment Seçenekleri

### Seçenek 1: Streamlit Cloud (Önerilen)

**Avantajlar:**

- ✅ Ücretsiz
- ✅ Otomatik deploy
- ✅ HTTPS/SSL dahil
- ✅ Custom domain desteği
- ✅ Kolay yönetim

**Dezavantajlar:**

- ❌ Sınırlı kaynak
- ❌ Uyku modu (inaktif uygulamalar)
- ❌ Veri depolama sınırı

**Kurulum:** 5 dakika

---

### Seçenek 2: Heroku (Kapatıldı)

Heroku ücretsiz tier'i kapatıldı. Alternatif: Railway, Render

---

### Seçenek 3: Railway + Streamlit Cloud

**Kurulum:**

1. **API'yi Railway'e deploy et:**

   ```bash
   # Railway hesabı oluştur: https://railway.app
   # GitHub repo'yu bağla
   # Deploy et
   ```

2. **Frontend'i Streamlit Cloud'a deploy et:**
   ```bash
   # Streamlit Cloud'da deploy et
   # API URL'sini secrets'e ekle
   ```

**Maliyet:** 5$ (Railway) + Ücretsiz (Streamlit Cloud)

---

### Seçenek 4: Docker + Streamlit Cloud

Streamlit Cloud Docker'ı desteklemez. Bunun yerine Railway veya Render kullanın.

---

## 📱 Mobil Uyumluluğu

### Responsive Design

```python
# app.py
import streamlit as st

# Mobil uyumlu layout
st.set_page_config(
    page_title="ComplaintIQ",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="auto"
)

# Responsive columns
col1, col2 = st.columns([1, 1])

with col1:
    st.write("Mobil uyumlu içerik")
```

---

## 🔄 Otomatik Deploy

### GitHub Actions ile Otomatik Deploy

```yaml
# .github/workflows/streamlit-deploy.yml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Streamlit Cloud
        run: |
          pip install streamlit
          streamlit run app.py --logger.level=debug
```

---

## 🐛 Sorun Giderme

### Uygulama Açılmıyor

```
Hata: "ModuleNotFoundError: No module named 'fastapi'"
Çözüm: requirements.txt'e fastapi ekle
```

### API Bağlantı Hatası

```
Hata: "Connection refused"
Çözüm: API URL'sini kontrol et, CORS ayarlarını kontrol et
```

### Uyku Modu (Inactivity)

```
Hata: "App is sleeping"
Çözüm: Streamlit Cloud Pro'ya yükselt veya API'yi ayrı sunucuda çalıştır
```

### Timeout Hatası

```
Hata: "Request timeout"
Çözüm: API'nin yanıt süresini azalt, cache kullan
```

---

## 💾 Veri Depolama

### Streamlit Cloud'da Veri Kaydetme

```python
# app.py
import streamlit as st
import pandas as pd
import os

# Veri dosyası
DATA_FILE = "data/complaints.csv"

# Veri yükle
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame()

# Veri kaydet
df.to_csv(DATA_FILE, index=False)
```

### GitHub'da Veri Depolama

```bash
# .gitignore'a ekle
data/raw/*.csv
data/processed/*.csv

# Veya GitHub LFS kullan
git lfs install
git lfs track "*.csv"
```

---

## 🎯 Önerilen Kurulum

### Hızlı Başlangıç (Streamlit Cloud)

```bash
# 1. GitHub'a push et
git push origin main

# 2. Streamlit Cloud'da deploy et
# https://streamlit.io/cloud

# 3. Uygulamaya erişim
# https://complaintiq.streamlit.app
```

### Profesyonel Kurulum (Railway + Streamlit Cloud)

```bash
# 1. API'yi Railway'e deploy et
# https://railway.app

# 2. Frontend'i Streamlit Cloud'a deploy et
# https://streamlit.io/cloud

# 3. Secrets'i ayarla
# API URL'sini Streamlit Cloud'da ekle
```

---

## ✅ Deployment Checklist

- [ ] GitHub'a proje yüklendi
- [ ] Streamlit Cloud hesabı oluşturuldu
- [ ] requirements.txt kontrol edildi
- [ ] .streamlit/config.toml oluşturuldu
- [ ] API bağlantısı ayarlandı
- [ ] CORS ayarları yapıldı
- [ ] Secrets ayarlandı
- [ ] Uygulamaya erişim sağlandı
- [ ] Mobil uyumluluğu test edildi
- [ ] Custom domain bağlandı (opsiyonel)

---

## 📞 Destek

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Community:** https://discuss.streamlit.io
- **GitHub Issues:** https://github.com/YOUR_USERNAME/complaintiq/issues

---

**Son Güncelleme:** 2025-12-09
