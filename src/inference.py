"""
Inference modülü - Model tahmin işlemleri
"""
import joblib
import logging
import re
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from scipy.sparse import hstack, csr_matrix
from src.config import MODEL_CONFIG, BUSINESS_RULES

logger = logging.getLogger(__name__)

class ComplaintClassifier:
    """
    Müşteri şikayet kategorilendirme sınıfı
    """
    
    def __init__(self):
        """Model ve bileşenleri yükler"""
        self.model = None
        self.tfidf = None
        self.scaler = None
        self.categories = None
        self._load_model()
    
    def _load_model(self):
        """Eğitilmiş model ve bileşenleri yükler"""
        try:
            logger.info("Model yükleniyor...")
            
            # Model dosyalarının varlığını kontrol et
            model_path = MODEL_CONFIG["model_path"]
            tfidf_path = MODEL_CONFIG["tfidf_path"]
            scaler_path = MODEL_CONFIG["scaler_path"]
            
            if not all([model_path.exists(), tfidf_path.exists(), scaler_path.exists()]):
                logger.warning("Model dosyaları bulunamadı. Mock model kullanılıyor.")
                self._setup_mock_model()
                return
            
            # Model bileşenlerini yükle
            self.model = joblib.load(MODEL_CONFIG["model_path"])
            self.tfidf = joblib.load(MODEL_CONFIG["tfidf_path"])
            self.scaler = joblib.load(MODEL_CONFIG["scaler_path"])
            
            # Kategorileri al
            self.categories = self.model.classes_
            
            logger.info(f"Model başarıyla yüklendi. Kategoriler: {list(self.categories)}")
            
        except Exception as e:
            logger.error(f"Model yükleme hatası: {e}")
            logger.info("Fallback olarak mock model kullanılıyor.")
            self._setup_mock_model()
    
    def _setup_mock_model(self):
        """Mock model kurulumu - demo amaçlı"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        import numpy as np
        
        # Mock kategoriler
        self.categories = np.array(BUSINESS_RULES["supported_categories"])
        
        # Mock TF-IDF vectorizer
        self.tfidf = TfidfVectorizer(max_features=100, vocabulary={'demo': 0})
        
        # Mock scaler
        self.scaler = StandardScaler()
        self.scaler.mean_ = np.array([50, 10])  # mean for text_length, word_count
        self.scaler.scale_ = np.array([25, 5])   # std for text_length, word_count
        self.scaler.n_features_in_ = 2
        
        # Mock model - her zaman "Delivery Issues" döndürür
        self.model = type('MockModel', (), {
            'classes_': self.categories,
            'predict': lambda self, X: ['Delivery Issues'] * X.shape[0],
            'predict_proba': lambda self, X: np.array([[0.8, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.06] for _ in range(X.shape[0])])
        })()
        
        logger.info("Mock model kuruldu - Demo modu aktif")
    
    def preprocess_text(self, text: str) -> str:
        """
        Metin ön işleme yapar
        
        Args:
            text: İşlenecek metin
            
        Returns:
            Temizlenmiş metin
        """
        if pd.isna(text) or text == "":
            return ""
        
        # Temel temizleme
        text = text.lower()
        text = re.sub(r'[^a-zğüşıöçĞÜŞIİÖÇ\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_features(self, text: str) -> csr_matrix:
        """
        Metinden özellik çıkarır
        
        Args:
            text: Özellik çıkarılacak metin
            
        Returns:
            Birleştirilmiş özellik matrisi
        """
        # Metin özellikleri (TF-IDF)
        cleaned_text = self.preprocess_text(text)
        text_features = self.tfidf.transform([cleaned_text])
        
        # Sayısal özellikler
        text_length = len(text)
        word_count = len(text.split())
        numerical_features = self.scaler.transform([[text_length, word_count]])
        
        # Özellikleri birleştir
        combined_features = hstack([text_features, csr_matrix(numerical_features)])
        
        return combined_features
    
    def predict_single(self, text: str) -> Dict:
        """
        Tek metin için tahmin yapar
        
        Args:
            text: Tahmin edilecek metin
            
        Returns:
            Tahmin sonuçları
        """
        try:
            # Giriş validasyonu
            if not text or len(text.strip()) < BUSINESS_RULES["text_limits"]["min_length"]:
                raise ValueError(f"Metin çok kısa. Minimum {BUSINESS_RULES['text_limits']['min_length']} karakter gerekli.")
            
            if len(text) > BUSINESS_RULES["text_limits"]["max_length"]:
                raise ValueError(f"Metin çok uzun. Maksimum {BUSINESS_RULES['text_limits']['max_length']} karakter.")
            
            # Özellik çıkarma
            features = self.extract_features(text)
            
            # Tahmin
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            
            # Güven skoru
            confidence = probabilities.max()
            
            # Tüm olasılıklar
            all_probabilities = {
                cat: float(prob) for cat, prob in zip(self.categories, probabilities)
            }
            
            result = {
                'prediction': prediction,
                'confidence': float(confidence),
                'all_probabilities': all_probabilities,
                'text_length': len(text),
                'word_count': len(text.split())
            }
            
            logger.info(f"Tahmin yapıldı: {prediction} (güven: {confidence:.3f})")
            
            return result
            
        except Exception as e:
            logger.error(f"Tahmin hatası: {e}")
            raise
    
    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """
        Çoklu metin için tahmin yapar
        
        Args:
            texts: Tahmin edilecek metinler listesi
            
        Returns:
            Tahmin sonuçları listesi
        """
        results = []
        
        for i, text in enumerate(texts):
            try:
                result = self.predict_single(text)
                result['text_index'] = i
                results.append(result)
            except Exception as e:
                logger.error(f"Metin {i} tahmin hatası: {e}")
                results.append({
                    'text_index': i,
                    'error': str(e),
                    'success': False
                })
        
        return results
    
    def get_category_info(self, category: str) -> Dict:
        """
        Kategori hakkında bilgi getirir
        
        Args:
            category: Kategori adı
            
        Returns:
            Kategori bilgisi
        """
        category_info = {
            "category": category,
            "description": self._get_category_description(category),
            "priority_suggestion": self._get_priority_suggestion(category),
            "common_keywords": self._get_common_keywords(category)
        }
        
        return category_info
    
    def _get_category_description(self, category: str) -> str:
        """Kategori açıklaması"""
        descriptions = {
            "Delivery Issues": "Teslimat problemleri, kargo gecikmeleri, hasarlı paketler",
            "Billing Issues": "Faturalandırma hataları, ödeme sorunları, fiyat problemleri",
            "Product Quality": "Ürün kalitesi, kusurlu ürünler, beklentiye uymayan ürünler",
            "Customer Service": "Müşteri hizmetleri davranışları, iletişim problemleri",
            "Technical Support": "Teknik destek, ürün kurulumu, yazılım problemleri",
            "Return/Refund": "İade işlemleri, para iadesi, değişim talepleri",
            "Website Issues": "Web sitesi problemleri, teknik arızalar, kullanım zorlukları",
            "Service Outage": "Hizmet kesintileri, sistem arızaları, erişim problemleri",
            "Fraud Issues": "Dolandırıcılık, güvenlik ihlalleri, şüpheli işlemler"
        }
        
        return descriptions.get(category, "Kategori bilgisi bulunamadı")
    
    def _get_priority_suggestion(self, category: str) -> str:
        """Kategori için öncelik önerisi"""
        high_priority = ["Fraud Issues", "Service Outage", "Technical Support"]
        medium_priority = ["Delivery Issues", "Billing Issues", "Product Quality"]
        
        if category in high_priority:
            return "Yüksek Öncelik"
        elif category in medium_priority:
            return "Orta Öncelik"
        else:
            return "Düşük Öncelik"
    
    def _get_common_keywords(self, category: str) -> List[str]:
        """Kategori için yaygın anahtar kelimeler"""
        keywords = {
            "Delivery Issues": ["teslimat", "kargo", "paket", "gecikme", "hasar"],
            "Billing Issues": ["fatura", "ödeme", "ücret", "hata", "yanlış"],
            "Product Quality": ["kalite", "kusur", "bozuk", "çürük", "iade"],
            "Customer Service": ["hizmet", "davranış", "kaba", "yardım", "destek"],
            "Technical Support": ["teknik", "kurulum", "yazılım", "donanım", "arıza"],
            "Return/Refund": ["iade", "para", "değişim", "ürün", "süreç"],
            "Website Issues": ["web", "site", "açılmıyor", "hata", "yavaş"],
            "Service Outage": ["kesinti", "çalışmıyor", "arıza", "hizmet", "erişim"],
            "Fraud Issues": ["dolandırıcılık", "hack", "güvenlik", "çalınmış", "şüpheli"]
        }
        
        return keywords.get(category, [])

# Global classifier instance
classifier = ComplaintClassifier()

def predict_complaint(text: str) -> Dict:
    """
    Tek metin için tahmin yapan wrapper fonksiyon
    
    Args:
        text: Tahmin edilecek şikayet metni
        
    Returns:
        Tahmin sonucu
    """
    return classifier.predict_single(text)

def batch_predict_complaints(texts: List[str]) -> List[Dict]:
    """
    Çoklu metin için tahmin yapan wrapper fonksiyon
    
    Args:
        texts: Tahmin edilecek şikayet metinleri
        
    Returns:
        Tahmin sonuçları listesi
    """
    return classifier.predict_batch(texts)

def get_categories() -> List[str]:
    """
    Desteklenen kategorileri getirir
    
    Returns:
        Kategori listesi
    """
    return BUSINESS_RULES["supported_categories"]