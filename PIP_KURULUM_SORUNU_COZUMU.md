# 🔧 Pip Kurulum Sorunu Çözümü

## ⚠️ Hata Mesajı

```
ERROR: Could not install packages due to an OSError: [WinError 2]
Sistem belirtilen dosyayı bulamıyor: 'C:\\Python312\\Scripts\\normalizer.exe'
```

Bu hata, Python Scripts klasöründe izin sorunu olduğu anlamına gelir.

---

## ✅ Çözüm 1: --user Parametresi Kullanın (EN KOLAY)

### Adım 1: Terminal Açın

```bash
Windows Başlat → cmd yazın → Command Prompt açın
```

### Adım 2: Proje Dizinine Gidin

```bash
cd d:\ComplaintIQ
```

### Adım 3: Bağımlılıkları Yükleyin (--user ile)

```bash
python -m pip install --user fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

**Enter tuşuna basın**

✅ Bu sefer başarılı olmalı!

---

## ✅ Çözüm 2: Virtual Environment Kullanın

### Adım 1: Terminal Açın

```bash
cd d:\ComplaintIQ
```

### Adım 2: Virtual Environment Oluşturun

```bash
python -m venv venv
```

### Adım 3: Virtual Environment'i Aktifleştirin

```bash
venv\Scripts\activate
```

Başarılı olursa, terminal'de `(venv)` göreceksiniz.

### Adım 4: Bağımlılıkları Yükleyin

```bash
python -m pip install fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

### Adım 5: Uygulamayı Çalıştırın

```bash
python api.py
```

---

## ✅ Çözüm 3: Pip'i Yeniden Yükleyin

### Adım 1: Terminal Açın

```bash
cd d:\ComplaintIQ
```

### Adım 2: Pip'i Yeniden Yükleyin

```bash
python -m pip install --upgrade --force-reinstall pip
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
python -m pip install --user fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

---

## 🎯 Önerilen Yol: Çözüm 1 (--user)

En basit ve hızlı çözüm:

```bash
cd d:\ComplaintIQ
python -m pip install --user fastapi uvicorn streamlit pandas scikit-learn plotly requests
```

---

## 🚀 Kurulum Başarılı Olursa

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

## 📋 Adım Adım Kontrol Listesi

- [ ] Terminal açtım
- [ ] `cd d:\ComplaintIQ` komutunu çalıştırdım
- [ ] `python -m pip install --user fastapi uvicorn streamlit pandas scikit-learn plotly requests` komutunu çalıştırdım
- [ ] Kurulum başarılı oldu (hata yok)
- [ ] `python api.py` komutunu çalıştırdım
- [ ] `streamlit run app.py` komutunu çalıştırdım
- [ ] http://localhost:8501 açıldı

---

## 🐛 Hala Sorun Yaşarsanız

### Seçenek A: Pip Sürümünü Kontrol Edin

```bash
python -m pip --version
```

### Seçenek B: Python Sürümünü Kontrol Edin

```bash
python --version
```

### Seçenek C: Yönetici Olarak Çalıştırın

1. Command Prompt'u kapatın
2. Windows Başlat menüsünde "cmd" yazın
3. Sağ tıklayın → "Yönetici olarak çalıştır" seçin
4. Tekrar deneyin

---

**Başarılar! 🎉**

Herhangi bir sorun yaşarsanız, `BAŞLANGIC_REHBERI.md` dosyasını kontrol edin.
