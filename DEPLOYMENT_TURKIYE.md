# 🚀 ComplaintIQ - Türkiye'de Yayınlama Rehberi

## 📌 Hızlı Başlangıç (5 Dakika)

### Yerel Sunucuda Çalıştırma

```bash
# 1. Proje dizinine git
cd d:\ComplaintIQ

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. API'yi başlat (Terminal 1)
python api.py

# 4. Frontend'i başlat (Terminal 2)
streamlit run app.py

# 5. Tarayıcıda aç
# API: http://localhost:8000/docs
# Frontend: http://localhost:8501
```

---

## 🌐 Türkiye'de Barındırma Seçenekleri

### 1. 🔵 **Heroku** (En Kolay - Ücretsiz Tier Kapatıldı)

**Alternatif: Railway.app**

```bash
# 1. Railway hesabı oluştur: https://railway.app
# 2. GitHub'a push et
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/complaintiq.git
git push -u origin main

# 3. Railway'de yeni proje oluştur
# 4. GitHub repo'yu bağla
# 5. Environment variables ekle:
# - PYTHON_VERSION=3.12
# - PORT=8000
```

**Dockerfile (Railway için):**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "api.py"]
```

---

### 2. 🟢 **Render.com** (Türkiye Dostu)

**Avantajlar:**

- Ücretsiz tier mevcut
- Türkiye'den erişim hızlı
- PostgreSQL desteği
- Otomatik deploy

**Adımlar:**

```bash
# 1. Render hesabı oluştur: https://render.com
# 2. GitHub'a push et
# 3. Render'da "New Web Service" oluştur
# 4. GitHub repo'yu seç
# 5. Build command: pip install -r requirements.txt
# 6. Start command: python api.py
# 7. Environment variables:
#    - PYTHON_VERSION=3.12
#    - PORT=8000
```

---

### 3. 🟡 **PythonAnywhere** (Türkiye'de Popüler)

**Avantajlar:**

- Python-specific hosting
- Kolay kurulum
- Türkiye'den hızlı erişim

**Adımlar:**

```bash
# 1. PythonAnywhere hesabı oluştur: https://www.pythonanywhere.com
# 2. Web app oluştur (Flask/FastAPI)
# 3. WSGI dosyasını düzenle:

# /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py
import sys
path = '/home/YOUR_USERNAME/complaintiq'
if path not in sys.path:
    sys.path.append(path)

from api import app as application
```

---

### 4. 🔴 **AWS Lightsail** (Profesyonel)

**Avantajlar:**

- Türkiye'de sunucu seçeneği
- Ölçeklenebilir
- Güvenilir

**Adımlar:**

```bash
# 1. AWS Lightsail hesabı oluştur
# 2. Ubuntu 22.04 instance oluştur
# 3. SSH ile bağlan:
ssh -i key.pem ubuntu@YOUR_IP

# 4. Sunucuyu hazırla:
sudo apt update
sudo apt install python3.12 python3-pip git

# 5. Projeyi klonla:
git clone https://github.com/YOUR_USERNAME/complaintiq.git
cd complaintiq
pip install -r requirements.txt

# 6. Systemd service oluştur:
sudo nano /etc/systemd/system/complaintiq.service
```

**Service dosyası:**

```ini
[Unit]
Description=ComplaintIQ API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/complaintiq
ExecStart=/usr/bin/python3.12 /home/ubuntu/complaintiq/api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 7. Service'i başlat:
sudo systemctl enable complaintiq
sudo systemctl start complaintiq
```

---

### 5. 🟣 **DigitalOcean App Platform** (Türkiye Dostu)

**Avantajlar:**

- Türkiye'de veri merkezi
- Uygun fiyat
- Kolay deploy

**Adımlar:**

```bash
# 1. DigitalOcean hesabı oluştur: https://www.digitalocean.com
# 2. App Platform'da yeni app oluştur
# 3. GitHub repo'yu bağla
# 4. Build command: pip install -r requirements.txt
# 5. Run command: python api.py
# 6. Port: 8000
```

---

### 6. 🟠 **Vercel** (Frontend için)

**Streamlit Frontend için:**

```bash
# 1. Vercel hesabı oluştur: https://vercel.com
# 2. GitHub repo'yu bağla
# 3. Framework: Other
# 4. Build command: pip install -r requirements.txt && streamlit run app.py
# 5. Output directory: .streamlit
```

---

## 🐳 Docker ile Yayınlama

### Docker Image Oluştur

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Port
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Başlangıç
CMD ["python", "api.py"]
```

### Docker Compose (API + Frontend)

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    restart: always

  frontend:
    build: .
    ports:
      - "8501:8501"
    command: streamlit run app.py
    environment:
      - PYTHONUNBUFFERED=1
    depends_on:
      - api
    restart: always

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api
      - frontend
    restart: always
```

### Docker ile Çalıştır

```bash
# Image oluştur
docker build -t complaintiq:latest .

# Container çalıştır
docker run -p 8000:8000 -p 8501:8501 complaintiq:latest

# Docker Compose ile çalıştır
docker-compose up -d
```

---

## 🔐 Güvenlik Ayarları

### 1. Environment Variables

```bash
# .env dosyası oluştur
API_KEY=your_secret_key_here
DATABASE_URL=postgresql://user:password@localhost/complaintiq
ALLOWED_ORIGINS=https://yourdomain.com
DEBUG=False
```

### 2. HTTPS/SSL Sertifikası

```bash
# Let's Encrypt ile ücretsiz sertifika
sudo apt install certbot python3-certbot-nginx

# Sertifika oluştur
sudo certbot certonly --standalone -d yourdomain.com

# Nginx'te kullan
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
    }
}
```

### 3. Firewall Ayarları

```bash
# UFW ile firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📊 Monitoring ve Logging

### 1. PM2 ile Process Management

```bash
# PM2 yükle
npm install -g pm2

# Ecosystem dosyası oluştur
pm2 init

# API'yi başlat
pm2 start api.py --name "complaintiq-api"

# Frontend'i başlat
pm2 start "streamlit run app.py" --name "complaintiq-frontend"

# Logs
pm2 logs complaintiq-api
pm2 logs complaintiq-frontend

# Monitoring
pm2 monit
```

### 2. Logging Konfigürasyonu

```python
# src/logging_config.py
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # File handler
    handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
```

---

## 💰 Maliyet Karşılaştırması

| Platform       | Ücretsiz Tier | Aylık Ücret | Türkiye Desteği |
| -------------- | ------------- | ----------- | --------------- |
| Railway        | 5$ kredi      | 5$+         | ✅ İyi          |
| Render         | Sınırlı       | 7$+         | ✅ İyi          |
| PythonAnywhere | Evet          | 5$+         | ✅ Çok İyi      |
| AWS Lightsail  | 1 ay ücretsiz | 3.5$+       | ✅ Mükemmel     |
| DigitalOcean   | Evet          | 4$+         | ✅ Çok İyi      |
| Vercel         | Evet          | 20$+        | ✅ İyi          |

---

## 🎯 Önerilen Kurulum (Başlangıç)

### Seçenek 1: Hızlı Başlangıç (Railway)

```bash
# 1. Railway hesabı oluştur
# 2. GitHub'a push et
# 3. Railway'de deploy et
# Maliyet: Ücretsiz (5$ kredi)
# Kurulum süresi: 5 dakika
```

### Seçenek 2: Profesyonel (AWS Lightsail)

```bash
# 1. AWS hesabı oluştur
# 2. Lightsail instance oluştur
# 3. SSH ile bağlan
# 4. Projeyi deploy et
# Maliyet: 3.5$ / ay
# Kurulum süresi: 30 dakika
```

### Seçenek 3: Türkiye Optimized (PythonAnywhere)

```bash
# 1. PythonAnywhere hesabı oluştur
# 2. Web app oluştur
# 3. Dosyaları yükle
# Maliyet: 5$ / ay
# Kurulum süresi: 15 dakika
```

---

## 🔧 Sorun Giderme

### Port Zaten Kullanımda

```bash
# Port 8000'i kullanan işlemi bul
netstat -ano | findstr :8000

# İşlemi kapat
taskkill /PID <PID> /F

# Farklı port kullan
python api.py --port 8001
```

### Bağımlılık Hatası

```bash
# Tüm bağımlılıkları yeniden yükle
pip install --upgrade -r requirements.txt

# Virtual environment kullan
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Model Dosyası Bulunamadı

```bash
# Model eğit
python -c "from src.pipeline import run_pipeline; run_pipeline()"

# Veya Streamlit'te "Model Eğit" butonuna tıkla
```

---

## 📱 Mobil Uygulamaya Dönüştürme

### React Native ile

```bash
# Expo ile başla
npx create-expo-app complaintiq-mobile

# API'ye bağlan
fetch('https://your-api.com/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Şikayet metni' })
})
```

---

## 📞 Destek ve İletişim

- **GitHub Issues:** https://github.com/YOUR_USERNAME/complaintiq/issues
- **Email:** support@complaintiq.com
- **Discord:** [Sunucu Linki]

---

## ✅ Deployment Checklist

- [ ] Bağımlılıklar yüklendi
- [ ] Model eğitildi ve kaydedildi
- [ ] API yerel olarak çalışıyor
- [ ] Frontend yerel olarak çalışıyor
- [ ] Environment variables ayarlandı
- [ ] HTTPS/SSL sertifikası oluşturuldu
- [ ] Firewall kuralları ayarlandı
- [ ] Monitoring ve logging yapılandırıldı
- [ ] Backup stratejisi belirlendi
- [ ] Domain adı satın alındı
- [ ] DNS ayarları yapıldı
- [ ] Canlı ortamda test edildi

---

**Son Güncelleme:** 2025-12-09
**Versiyon:** 1.0
