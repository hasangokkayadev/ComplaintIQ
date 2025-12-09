# 🇹🇷 Türkiye'ye Özel En İdeal Şikayet Dataset Stratejisi

## ⭐ Kapsamlı Dataset Kombinasyonu

**Hedef Hacim:** 6.000–20.000 satır  
**Beklenen Performans:** %88–93 Macro F1 (DistilBERT ile %94+)

## 📊 Dataset Kaynakları ve Hacim Dağılımı

| Veri Kaynağı                              | Hedef Adet         | Güçlü Yönleri                                          |
| ----------------------------------------- | ------------------ | ------------------------------------------------------ |
| **Google Maps Negatif Yorumları**         | 1.000 – 3.000      | Tamamen gerçek, tüm sektörler, mükemmel dil modeli     |
| **Şikayetvar.com Şikayetleri**            | 1.000 – 5.000      | Net şikayet dili, çok çeşitli kategoriler              |
| **Trendyol/Hepsiburada Negatif Yorumlar** | 500 – 3.000        | Saf e-ticaret şikayetleri, küçük işletmeler için ideal |
| **Sentetik Şikayet Üretimi (ChatGPT)**    | 500 – 2.000        | Kategori dengesi, minority class desteği               |
| **TOPLAM**                                | **3.000 – 13.000** | **Türkiye pazarının en güçlü dataseti**                |

## 🔥 1. Google Maps Negatif Yorumları (Çekirdek Data)

### Neden Çok Güçlü?

- ✅ Tamamen gerçek müşteri şikayetleri
- ✅ Türk işletmelerine özel yazım
- ✅ Her sektörden çeşitlilik (kafe, restoran, mağaza, güzellik...)
- ✅ Dil modeli için mükemmel

### Kategori Eşleştirme:

- Ürün/Hizmet Kalitesi
- Personel Davranışı
- Hizmet Gecikmesi
- Temizlik/Ortam
- Teknik Sorunlar
- Fiyat Memnuniyetsizliği

### Toplama Yöntemi:

```python
# Google Maps Places API + Reviews
# Her şehirden her sektörden 20-50 yorum
# Rating 1-2 yıldız olanları seç
```

## 📝 2. Şikayetvar.com Şikayetleri

### Avantajlar:

- ✅ Çok net "şikayet dili"
- ✅ Detaylı cümle yapısı
- ✅ Çok fazla kategori çeşitliliği
- ✅ Gerçek müşteri problemi

### Kategori Zaten Hazır:

- Kargo problemleri
- Online alışveriş sorunları
- Elektronik şikayetleri
- Giyim/ aksesuar
- Bankacılık
- Telekom
- Yeme-içme

### Etik Durum:

⚠️ **Tamamen kamuya açık veri** - Etik kullanımda sorun yok

## 🛒 3. Trendyol/Hepsiburada Negatif Yorumlar

### E-ticaret Odaklı Şikayetler:

- "Kargom gelmedi"
- "Yanlış ürün geldi"
- "Kutu ezilmişti"
- "Yorumlarda yazdığı gibi çıkmadı"

### Küçük İşletmeler İçin Değer:

- E-ticaret dilini öğretir
- Satıcı kalite sorunlarını gösterir
- Kategoriler çok belirgin

### Toplama:

```python
# 1 yıldız yorumları filtrele
# Her kategoriden eşit dağılım
# Spam ve gereksiz yorumları temizle
```

## 🤖 4. Sentetik Şikayet Üretimi (ChatGPT Destekli)

### Neden Gerekli?

- ✅ Kategorilerde denge sağlar
- ✅ Minority class'ları güçlendirir
- ✅ Gerçek veriyi "doping" gibi destekler

### Kategori Başına Sentetik Örnekler (50-150 adet):

- Teslimat gecikmesi
- Yanlış ürün
- Eksik ürün
- Kötü ambalaj
- İade sorunu
- Fatura/ödeme sorunu
- Destek hattı sorunu
- Teknik problem

## 🎯 Nihai Kategori Seti (Türkiye'ye Özel)

### 12 Kategori - En Kapsamlı Sınıflandırıcı:

1. **Ürün Kalite Sorunu**
2. **Yanlış Ürün**
3. **Eksik Ürün**
4. **Kargo Gecikmesi**
5. **Kargo Firması Problemi**
6. **İade/Değişim Sorunu**
7. **Ödeme/Fatura Sorunu**
8. **Müşteri Hizmetleri Sorunu**
9. **Paketleme/Ambalaj Problemi**
10. **Ürün Açıklaması Yanıltıcı**
11. **Hizmet Kalite Sorunu** (Google Maps)
12. **Teknik/Uygulama Sorunu**

### Neden Bu Kategori Seti?

- ✅ Hem e-ticaret hem mağaza hem hizmet sektörü
- ✅ Türkiye pazarına özel
- ✅ En geniş kapsamlı mümkün olan sınıflandırıcı
- ✅ Her sektör için uygulanabilir

## 📈 Beklenen Model Performansı

### Sentetik Mevcut Dataset:

- **Accuracy**: %85+
- **Macro F1**: %83+

### Yeni Türkiye Optimized Dataset:

- **Accuracy**: %90+
- **Macro F1**: %88–93
- **DistilBERT ile**: %94+ F1

### Neden Bu Kadar Yüksek?

- ✅ Gerçek Türkçe dil pattern'ları
- ✅ Çok çeşitli kaynak kombinasyonu
- ✅ Dengeli kategori dağılımı
- ✅ Minority class desteği

## 🛠️ Implementasyon Adımları

### Faz 1: Data Collection (1-2 ay)

1. **Google Maps API** entegrasyonu
2. **Şikayetvar.com** web scraping
3. **E-ticaret** platform scraping
4. **ChatGPT API** sentetik üretim

### Faz 2: Data Processing (2-3 hafta)

1. **Otomatik etiketleme** sistemi
2. **Veri temizleme** pipeline'ı
3. **Duplicate removal**
4. **Kategori dengeleme**

### Faz 3: Model Training (1-2 hafta)

1. **TF-IDF + Logistic Regression** (Baseline)
2. **BERT/DistilBERT** fine-tuning
3. **Model karşılaştırma**
4. **Performance optimization**

## 💎 Bu Stratejinin Avantajları

### Teknik Avantajlar:

- ✅ **Türkçe'ye optimize** edilmiş
- ✅ **Real-world patterns** öğrenir
- ✅ **High accuracy** beklenir
- ✅ **Production ready** olur

### İş Avantajları:

- ✅ **Türkiye pazarına** özel
- ✅ **Küçük işletmeler** için ideal
- ✅ **Scalable** çözüm
- ✅ **Commercial viability** yüksek

## 🏆 Sonuç

**Bu kombinasyon = Türkiye pazarında yapılabilen EN GÜÇLÜ NLP şikayet sınıflandırma datasetidir.**

- Hem **final proje** için mükemmel
- Hem de **ticari ürün** için ideal
- **%94+ F1 score** potansiyeli
- **Real-world deployment** ready

---

**ComplaintIQ için en ideal dataset stratejisi tamamlandı! 🚀**
