# 📦 Bağımlılık Kurulum Rehberi

## ⚠️ Hata: ModuleNotFoundError: No module named 'fastapi'

Bu hata, gerekli Python paketlerinin yüklü olmadığı anlamına gelir.

---

## ✅ Çözüm: Bağımlılıkları Yükleyin

### Adım 1: Terminal Açın

1. **Windows Başlat Menüsü**'nü açın
2. **cmd** yazın ve **Command Prompt** açın

### Adım 2: Proje Dizinine Gidin

Terminal'de yazın:

```bash
cd d:\ComplaintIQ
```

**Enter** tuşuna basın

### Adım 3: Bağımlılıkları Yükleyin

Terminal'de yazın:

```bash
python -m pip install fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

**Enter** tuşuna basın

### Adım 4: Kurulumu Bekleyin

Kurulum birkaç dakika sürebilir. Aşağıdaki gibi bir mesaj göreceksiniz:

```
Collecting fastapi
Collecting uvicorn
Collecting streamlit
...
Successfully installed fastapi-0.124.0 uvicorn-0.38.0 streamlit-1.52.1 ...
```

✅ **Başarılı!** Tüm paketler yüklendi.

---

## 🚀 Şimdi Uygulamayı Çalıştırın

### Terminal 1: API Sunucusu

```bash
cd d:\ComplaintIQ
python api.py
```

### Terminal 2: Streamlit Frontend

```bash
cd d:\ComplaintIQ
streamlit run app.py
```

### Browser

```
http://localhost:8501
```

---

## 📋 Yüklenen Paketler

| Paket            | Açıklama                |
| ---------------- | ----------------------- |
| **fastapi**      | Web API framework'ü     |
| **uvicorn**      | ASGI sunucusu           |
| **streamlit**    | Web arayüzü framework'ü |
| **pandas**       | Veri işleme             |
| **scikit-learn** | Machine Learning        |
| **plotly**       | Grafikler               |
| **requests**     | HTTP istekleri          |

---

## 🐛 Eğer Hala Sorun Yaşarsanız

### Seçenek 1: Tüm Bağımlılıkları Yükleyin

```bash
python -m pip install -r requirements.txt
```

### Seçenek 2: Pip'i Güncelleyin

```bash
python -m pip install --upgrade pip
```

Sonra tekrar deneyin:

```bash
python -m pip install fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

### Seçenek 3: Virtual Environment Kullanın

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

---

## ✅ Kontrol Listesi

- [ ] Terminal açtım
- [ ] `cd d:\ComplaintIQ` komutunu çalıştırdım
- [ ] `python -m pip install fastapi uvicorn streamlit pandas scikit-learn plotly requests` komutunu çalıştırdım
- [ ] Kurulum tamamlandı
- [ ] `python api.py` komutunu çalıştırdım
- [ ] `streamlit run app.py` komutunu çalıştırdım
- [ ] http://localhost:8501 açıldı

---

**Başarılar! 🎉**
