"""
🇹🇷 Türkiye'ye Özel Veri Toplama Pipeline
ComplaintIQ - Gerçek Müşteri Şikayetleri Data Collection

Bu pipeline aşağıdaki kaynaklardan veri toplar:
1. Google Maps Negatif Yorumları
2. Şikayetvar.com Şikayetleri  
3. Trendyol/Hepsiburada Negatif Yorumlar
4. ChatGPT Sentetik Veri Üretimi
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import logging
from pathlib import Path
import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import rate_limiter

# Logging ayarı
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TurkeyComplaintDataCollector:
    """
    Türkiye'ye özel müşteri şikayet data toplama sınıfı
    """
    
    def __init__(self, config_path: str = "config.json"):
        """Data collector başlatma"""
        self.config = self.load_config(config_path)
        self.collected_data = []
        self.rate_limiter = rate_limiter.RateLimiter(
            calls_per_minute=self.config.get("rate_limit", 30)
        )
        
    def load_config(self, config_path: str) -> Dict:
        """Konfigürasyon dosyası yükle"""
        default_config = {
            "rate_limit": 30,
            "max_retries": 3,
            "timeout": 10,
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "openai_api_key": "",
            "google_maps_api_key": "",
            "proxy_settings": {}
        }
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {**default_config, **config}
        except FileNotFoundError:
            logger.warning(f"Config dosyası bulunamadı: {config_path}. Varsayılan ayarlar kullanılıyor.")
            return default_config
    
    def clean_text(self, text: str) -> str:
        """Metin temizleme fonksiyonu"""
        if not text:
            return ""
            
        # Temel temizlik
        text = re.sub(r'\s+', ' ', text)  # Çoklu boşlukları tek boşluk
        text = re.sub(r'[^\w\s.,!?ğüşıöçĞÜŞIİÖÇ]', '', text)  # Özel karakterleri temizle
        text = text.strip()
        
        # Kısa metinleri filtrele (5 karakterden az)
        if len(text) < 5:
            return ""
            
        return text
    
    def categorize_complaint(self, text: str) -> Tuple[str, float]:
        """
        Metni otomatik kategorize etme
        Türkiye'ye özel 12 kategori sistemi
        """
        text_lower = text.lower()
        
        # Kategori kuralları (keyword matching)
        category_rules = {
            "Ürün Kalite Sorunu": {
                "keywords": ["kalite", "bozuk", "çürük", "hasarlı", "malzeme", "işçilik", "dayanıklı", "kusur"],
                "weight": 1.0
            },
            "Yanlış Ürün": {
                "keywords": ["yanlış", "farklı", "başka", "istedigim", "sipar", "gelen"],
                "weight": 1.0
            },
            "Eksik Ürün": {
                "keywords": ["eksik", "yok", "tam değil", "parça", "aks", "kutu"],
                "weight": 1.0
            },
            "Kargo Gecikmesi": {
                "keywords": ["gecikti", "geç", "zaman", "kargo", "teslimat", "bekliyorum"],
                "weight": 1.0
            },
            "Kargo Firması Problemi": {
                "keywords": ["kargo firması", "kurye", "dağıtım", "lojistik", "firma"],
                "weight": 1.0
            },
            "İade/Değişim Sorunu": {
                "keywords": ["iade", "değişim", "para iadesi", "geri gönderme", "işlem"],
                "weight": 1.0
            },
            "Ödeme/Fatura Sorunu": {
                "keywords": ["fatura", "ödeme", "para", "kart", "faturalandırma", "tutar"],
                "weight": 1.0
            },
            "Müşteri Hizmetleri Sorunu": {
                "keywords": ["müşteri hizmetleri", "temsilci", "telefon", "destek", "yardım"],
                "weight": 1.0
            },
            "Paketleme/Ambalaj Problemi": {
                "keywords": ["paket", "ambalaj", "kutu", "paketleme", "hasar", "ezik"],
                "weight": 1.0
            },
            "Ürün Açıklaması Yanıltıcı": {
                "keywords": ["açıklama", "fotoğraf", "özellik", "yanlış", "farklı", "uymuyor"],
                "weight": 1.0
            },
            "Hizmet Kalite Sorunu": {
                "keywords": ["hizmet", "kalite", "personel", "davranış", "ortam", "işletme"],
                "weight": 1.0
            },
            "Teknik/Uygulama Sorunu": {
                "keywords": ["teknik", "uygulama", "yazılım", "sistem", "hata", "çalışmıyor"],
                "weight": 1.0
            }
        }
        
        # Keyword scoring
        scores = {}
        for category, rules in category_rules.items():
            score = 0
            for keyword in rules["keywords"]:
                if keyword in text_lower:
                    score += rules["weight"]
            scores[category] = score
        
        # En yüksek skorlu kategoriyi seç
        if max(scores.values()) > 0:
            predicted_category = max(scores, key=scores.get)
            confidence = min(scores[predicted_category] / 3.0, 1.0)  # Normalize confidence
            return predicted_category, confidence
        else:
            return "Bilinmeyen", 0.0
    
    def scrape_google_maps_reviews(self, business_name: str, location: str, max_reviews: int = 100) -> List[Dict]:
        """
        Google Maps'ten negatif yorumları toplama
        """
        logger.info(f"Google Maps yorumları toplanıyor: {business_name}, {location}")
        
        try:
            # Google Places API kullanımı (gerçek implementasyon)
            # Place Search + Place Details + Reviews API
            
            place_id = self._find_place_id(business_name, location)
            if not place_id:
                logger.warning(f"İşletme bulunamadı: {business_name}")
                return []
            
            reviews = self._fetch_place_reviews(place_id, max_reviews)
            
            # Sadece negatif yorumları filtrele (1-2 yıldız)
            negative_reviews = []
            for review in reviews:
                if review.get('rating', 0) <= 2:
                    cleaned_text = self.clean_text(review.get('text', ''))
                    if cleaned_text:
                        category, confidence = self.categorize_complaint(cleaned_text)
                        
                        negative_reviews.append({
                            'text': cleaned_text,
                            'category': category,
                            'confidence': confidence,
                            'source': 'google_maps',
                            'rating': review.get('rating', 0),
                            'business_name': business_name,
                            'location': location,
                            'date': review.get('time', ''),
                            'author': review.get('author_name', ''),
                            'raw_data': review
                        })
            
            logger.info(f"Google Maps'ten {len(negative_reviews)} negatif yorum toplandı")
            return negative_reviews
            
        except Exception as e:
            logger.error(f"Google Maps scraping hatası: {e}")
            return []
    
    def scrape_sikayetvar(self, category: str = None, max_pages: int = 10) -> List[Dict]:
        """
        Şikayetvar.com'dan şikayetleri toplama
        """
        logger.info("Şikayetvar.com'dan şikayetler toplanıyor")
        
        complaints = []
        
        try:
            headers = {
                'User-Agent': self.config['user_agent'],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            for page in range(1, max_pages + 1):
                self.rate_limiter.wait()
                
                url = f"https://www.sikayetvar.com/{category or ''}?page={page}"
                
                try:
                    response = requests.get(url, headers=headers, timeout=self.config['timeout'])
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Şikayet kartlarını bul
                    complaint_cards = soup.find_all('div', class_='complaint-item')
                    
                    for card in complaint_cards:
                        try:
                            text_element = card.find('p', class_='complaint-text')
                            if not text_element:
                                continue
                                
                            cleaned_text = self.clean_text(text_element.get_text())
                            if not cleaned_text:
                                continue
                            
                            category_element = card.find('span', class_='category')
                            detected_category = category_element.get_text().strip() if category_element else "Bilinmeyen"
                            
                            # Otomatik kategorilendirme
                            auto_category, confidence = self.categorize_complaint(cleaned_text)
                            
                            # Tarih bilgisi
                            date_element = card.find('time')
                            date = date_element.get('datetime') if date_element else ""
                            
                            complaints.append({
                                'text': cleaned_text,
                                'category': auto_category,
                                'confidence': confidence,
                                'source': 'sikayetvar',
                                'original_category': detected_category,
                                'date': date,
                                'url': card.find('a')['href'] if card.find('a') else "",
                                'raw_data': str(card)[:500]  # İlk 500 karakter
                            })
                            
                        except Exception as e:
                            logger.warning(f"Şikayet kartı işlenemedi: {e}")
                            continue
                    
                    logger.info(f"Sayfa {page}: {len(complaints)} şikayet toplandı")
                    
                except requests.RequestException as e:
                    logger.error(f"Sayfa {page} yüklenemedi: {e}")
                    continue
            
            logger.info(f"Şikayetvar.com'dan toplam {len(complaints)} şikayet toplandı")
            return complaints
            
        except Exception as e:
            logger.error(f"Şikayetvar scraping hatası: {e}")
            return []
    
    def scrape_ecommerce_reviews(self, platform: str = "trendyol", max_products: int = 50) -> List[Dict]:
        """
        Trendyol/Hepsiburada'dan negatif ürün yorumlarını toplama
        """
        logger.info(f"{platform.capitalize()}'den negatif yorumlar toplanıyor")
        
        reviews = []
        
        # Örnek ürün kategorileri (gerçek implementasyonda dinamik olacak)
        categories = ["elektronik", "giyim", "ev-yasam", "kozmetik"]
        
        try:
            for category in categories:
                try:
                    products = self._get_category_products(platform, category, max_products // len(categories))
                    
                    for product in products:
                        self.rate_limiter.wait()
                        product_reviews = self._get_product_reviews(platform, product['id'])
                        
                        # Sadece negatif yorumları filtrele
                        for review in product_reviews:
                            if review.get('rating', 0) <= 2:
                                cleaned_text = self.clean_text(review.get('text', ''))
                                if cleaned_text:
                                    category_pred, confidence = self.categorize_complaint(cleaned_text)
                                    
                                    reviews.append({
                                        'text': cleaned_text,
                                        'category': category_pred,
                                        'confidence': confidence,
                                        'source': platform,
                                        'rating': review.get('rating', 0),
                                        'product_name': product['name'],
                                        'product_category': category,
                                        'date': review.get('date', ''),
                                        'author': review.get('author', ''),
                                        'raw_data': review
                                    })
                
                except Exception as e:
                    logger.warning(f"{category} kategorisi işlenemedi: {e}")
                    continue
            
            logger.info(f"{platform.capitalize()}'den toplam {len(reviews)} negatif yorum toplandı")
            return reviews
            
        except Exception as e:
            logger.error(f"{platform} scraping hatası: {e}")
            return []
    
    def generate_synthetic_data(self, num_samples: int = 1000) -> List[Dict]:
        """
        ChatGPT API ile sentetik şikayet verisi üretme
        """
        logger.info(f"ChatGPT ile {num_samples} sentetik şikayet üretiliyor")
        
        if not self.config.get('openai_api_key'):
            logger.warning("OpenAI API key bulunamadı, sentetik veri üretilemiyor")
            return []
        
        synthetic_data = []
        
        # Her kategori için eşit dağılım
        categories = list(self.categorize_complaint("dummy").keys())
        samples_per_category = num_samples // len(categories)
        
        openai.api_key = self.config['openai_api_key']
        
        try:
            for category in categories:
                if category == "Bilinmeyen":
                    continue
                
                # Kategori örneklemesi için template prompt
                prompt = f"""
                Türkiye'de {category} konusunda gerçekçi müşteri şikayeti yaz.
                Özellikler:
                - Gerçek Türkçe dil kullan
                - 10-50 kelime arası olsun
                - Duygusal ve samimi olsun
                - Farklı varyasyonlarla 5 farklı örnek ver
                
                Kategori: {category}
                """
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.8
                )
                
                generated_texts = response.choices[0].message.content.split('\n')
                
                for text in generated_texts:
                    cleaned_text = self.clean_text(text)
                    if cleaned_text and len(cleaned_text) > 10:
                        synthetic_data.append({
                            'text': cleaned_text,
                            'category': category,
                            'confidence': 0.9,  # Sentetik veri yüksek güven
                            'source': 'synthetic_chatgpt',
                            'generated_by': 'gpt-3.5-turbo',
                            'date': datetime.now().isoformat()
                        })
                
                logger.info(f"{category} kategorisi için sentetik veri üretildi")
                
        except Exception as e:
            logger.error(f"Sentetik veri üretim hatası: {e}")
        
        logger.info(f"Toplam {len(synthetic_data)} sentetik veri üretildi")
        return synthetic_data
    
    def _find_place_id(self, business_name: str, location: str) -> Optional[str]:
        """Google Places API ile işletme ID bulma"""
        # Place Search API implementasyonu
        pass
    
    def _fetch_place_reviews(self, place_id: str, max_reviews: int) -> List[Dict]:
        """Google Places API ile yorumları çekme"""
        # Place Details + Reviews API implementasyonu
        pass
    
    def _get_category_products(self, platform: str, category: str, limit: int) -> List[Dict]:
        """E-ticaret platform'undan kategori ürünlerini çekme"""
        # Platform API implementasyonu
        pass
    
    def _get_product_reviews(self, platform: str, product_id: str) -> List[Dict]:
        """E-ticaret platform'undan ürün yorumlarını çekme"""
        # Platform API implementasyonu
        pass
    
    def collect_all_data(self) -> pd.DataFrame:
        """Tüm kaynaklardan veri toplama"""
        logger.info("Tüm veri kaynaklarından toplama başlıyor...")
        
        all_data = []
        
        # 1. Google Maps (Örnek işletmeler)
        sample_businesses = [
            ("McDonald's", "İstanbul"),
            ("Starbucks", "Ankara"),
            ("KFC", "İzmir"),
            ("Domino's Pizza", "Bursa"),
            ("CarrefourSA", "Antalya")
        ]
        
        for business, location in sample_businesses:
            google_data = self.scrape_google_maps_reviews(business, location, 20)
            all_data.extend(google_data)
            time.sleep(2)  # Rate limiting
        
        # 2. Şikayetvar
        sikayetvar_data = self.scrape_sikayetvar(max_pages=5)
        all_data.extend(sikayetvar_data)
        
        # 3. E-ticaret yorumları
        trendyol_data = self.scrape_ecommerce_reviews("trendyol", 25)
        all_data.extend(trendyol_data)
        
        hepsiburada_data = self.scrape_ecommerce_reviews("hepsiburada", 25)
        all_data.extend(hepsiburada_data)
        
        # 4. Sentetik veri
        synthetic_data = self.generate_synthetic_data(500)
        all_data.extend(synthetic_data)
        
        # DataFrame'e çevir
        df = pd.DataFrame(all_data)
        
        if not df.empty:
            # Duplicate temizleme
            df = df.drop_duplicates(subset=['text'], keep='first')
            
            # Kategori dağılımı logla
            logger.info(f"Toplam veri: {len(df)} kayıt")
            logger.info(f"Kategori dağılımı:\n{df['category'].value_counts()}")
        
        return df
    
    def save_data(self, df: pd.DataFrame, filename: str = None) -> str:
        """Toplanan veriyi kaydetme"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"turkey_complaints_dataset_{timestamp}.csv"
        
        filepath = Path("data/collected") / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Veri kaydedildi: {filepath}")
        
        return str(filepath)

# Kullanım örneği
if __name__ == "__main__":
    # Data collector oluştur
    collector = TurkeyComplaintDataCollector()
    
    # Tüm veriyi topla
    dataset = collector.collect_all_data()
    
    if not dataset.empty:
        # Veriyi kaydet
        filepath = collector.save_data(dataset)
        
        # Özet istatistikler
        print(f"\n📊 Veri Toplama Özeti:")
        print(f"Toplam kayıt: {len(dataset)}")
        print(f"Kaynak dağılımı:")
        print(dataset['source'].value_counts())
        print(f"\nKategori dağılımı:")
        print(dataset['category'].value_counts())
        
        print(f"\n✅ Dataset kaydedildi: {filepath}")
    else:
        print("❌ Hiç veri toplanamadı!")
