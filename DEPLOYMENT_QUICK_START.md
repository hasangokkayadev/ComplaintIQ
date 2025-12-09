# 🚀 ComplaintIQ - Hızlı Deployment Rehberi

## 📋 İçindekiler

1. [Yerel Kurulum](#yerel-kurulum)
2. [Docker ile Deployment](#docker-ile-deployment)
3. [Bulut Platformlarına Deploy](#bulut-platformlarına-deploy)
4. [Sorun Giderme](#sorun-giderme)

---

## 🏠 Yerel Kurulum

### Adım 1: Bağımlılıkları Yükle

```bash
# Proje dizinine git
cd d:\ComplaintIQ

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### Adım 2: API'yi Başlat

```bash
# Terminal 1'de
python api.py
```

**Beklenen çıktı:**

```
INFO:     Started server process [12345]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Adım 3: Frontend'i Başlat

```bash
# Terminal 2'de
streamlit run app.py
```

**Beklenen çıktı:**

```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Adım 4: Tarayıcıda Aç

- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:8501

---

## 🐳 Docker ile Deployment

### Adım 1: Docker Yükle

- Windows: https://www.docker.com/products/docker-desktop
- Linux: `sudo apt install docker.io docker-compose`

### Adım 2: Docker Image Oluştur

```bash
# Proje dizininde
docker build -t complaintiq:latest .
```

### Adım 3: Container Çalıştır

```bash
# Tek container
docker run -p 8000:8000 -p 8501:8501 complaintiq:latest

# Docker Compose ile (önerilen)
docker-compose up -d
```

### Adım 4: Kontrol Et

```bash
# Container'ları listele
docker ps

# Logs'u gör
docker logs complaintiq-api
docker logs complaintiq-frontend
```

---

## ☁️ Bulut Platformlarına Deploy

### 🔵 Railway.app (En Kolay)

**Maliyet:** Ücretsiz (5$ kredi)  
**Kurulum Süresi:** 5 dakika

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
# 5. Deploy et
```

**Environment Variables:**

```
PYTHON_VERSION=3.12
PORT=8000
```

---

### 🟢 Render.com (Türkiye Dostu)

**Maliyet:** Ücretsiz tier + 7$/ay  
**Kurulum Süresi:** 10 dakika

```bash
# 1. Render hesabı oluştur: https://render.com

# 2. GitHub'a push et (yukarıdaki gibi)

# 3. Render'da "New Web Service" oluştur
# 4. GitHub repo'yu seç
# 5. Build command: pip install -r requirements.txt
# 6. Start command: python api.py
```

---

### 🟡 PythonAnywhere (Türkiye'de Popüler)

**Maliyet:** 5$/ay  
**Kurulum Süresi:** 15 dakika

```bash
# 1. PythonAnywhere hesabı oluştur: https://www.pythonanywhere.com

# 2. Web app oluştur (Flask/FastAPI seç)

# 3. WSGI dosyasını düzenle:
# /var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py

import sys
path = '/home/YOUR_USERNAME/complaintiq'
if path not in sys.path:
    sys.path.append(path)

from api import app as application
```

---

### 🔴 AWS Lightsail (Profesyonel)

**Maliyet:** 3.5$/ay  
**Kurulum Süresi:** 30 dakika

```bash
# 1. AWS Lightsail hesabı oluştur

# 2. Ubuntu 22.04 instance oluştur

# 3. SSH ile bağlan
ssh -i key.pem ubuntu@YOUR_IP

# 4. Sunucuyu hazırla
sudo apt update
sudo apt install python3.12 python3-pip git

# 5. Projeyi klonla
git clone https://github.com/YOUR_USERNAME/complaintiq.git
cd complaintiq
pip install -r requirements.txt

# 6. Systemd service oluştur
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

[Install]
WantedBy=multi-user.target
```

```bash
# Service'i başlat
sudo systemctl enable complaintiq
sudo systemctl start complaintiq
```

---

### 🟣 DigitalOcean App Platform

**Maliyet:** 4$/ay  
**Kurulum Süresi:** 10 dakika

```bash
# 1. DigitalOcean hesabı oluştur: https://www.digitalocean.com

# 2. GitHub'a push et

# 3. App Platform'da yeni app oluştur
# 4. GitHub repo'yu bağla
# 5. Build command: pip install -r requirements.txt
# 6. Run command: python api.py
```

---

## 🔐 Güvenlik Ayarları

### 1. Environment Variables Ayarla

```bash
# .env dosyası oluştur
cp .env.example .env

# Dosyayı düzenle
nano .env
```

### 2. HTTPS/SSL Sertifikası

```bash
# Let's Encrypt ile ücretsiz sertifika
sudo apt install certbot python3-certbot-nginx

# Sertifika oluştur
sudo certbot certonly --standalone -d yourdomain.com
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

## 🔧 Sorun Giderme

### Port Zaten Kullanımda

```bash
# Port 8000'i kullanan işlemi bul
netstat -ano | findstr :8000

# İşlemi kapat
taskkill /PID <PID> /F
```

### Bağımlılık Hatası

```bash
# Tüm bağımlılıkları yeniden yükle
pip install --upgrade -r requirements.txt
```

### Model Dosyası Bulunamadı

```bash
# Model eğit
python -c "from src.pipeline import run_pipeline; run_pipeline()"
```

### Docker Hatası

```bash
# Docker daemon'u yeniden başlat
sudo systemctl restart docker

# Container'ları temizle
docker system prune -a
```

---

## 📊 Monitoring

### PM2 ile Process Management

```bash
# PM2 yükle
npm install -g pm2

# API'yi başlat
pm2 start api.py --name "complaintiq-api"

# Frontend'i başlat
pm2 start "streamlit run app.py" --name "complaintiq-frontend"

# Logs
pm2 logs complaintiq-api
```

---

## ✅ Deployment Checklist

- [ ] Bağımlılıklar yüklendi
- [ ] Model eğitildi
- [ ] API yerel olarak çalışıyor
- [ ] Frontend yerel olarak çalışıyor
- [ ] Environment variables ayarlandı
- [ ] Docker image oluşturuldu
- [ ] Bulut platformu seçildi
- [ ] Deploy edildi
- [ ] HTTPS/SSL ayarlandı
- [ ] Monitoring yapılandırıldı

---

## 🎯 Önerilen Kurulum

### Başlangıç (Hızlı Test)

```bash
# Yerel kurulum
pip install -r requirements.txt
python api.py
streamlit run app.py
```

### Üretim (Profesyonel)

```bash
# Docker Compose
docker-compose up -d

# Veya AWS Lightsail
# Bkz: AWS Lightsail bölümü
```

---

## 📞 Destek

- **GitHub Issues:** https://github.com/YOUR_USERNAME/complaintiq/issues
- **Email:** support@complaintiq.com

---

**Son Güncelleme:** 2025-12-09
