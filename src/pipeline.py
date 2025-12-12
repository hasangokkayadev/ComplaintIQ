"""
ML Pipeline - Müşteri şikayet kategorilendirme pipeline'ı
Türkiye'ye özel veri toplama ve işleme entegrasyonu
"""
import pandas as pd
import numpy as np
import logging
import joblib
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack, csr_matrix
import re
from typing import Tuple, Dict, Any, List, Optional
from src.config import DATA_PATHS, MODELS_DIR, BUSINESS_RULES

logger = logging.getLogger(__name__)

class TurkeyDataCollector:
    """
    🇹🇷 Türkiye'ye özel müşteri şikayet veri toplama sınıfı
    """
    
    def __init__(self):
        """Data collector başlatma"""
        self.collected_data = []
        self.categories = {
            "Ürün Kalite Sorunu": ["kalite", "bozuk", "çürük", "hasarlı", "malzeme"],
            "Yanlış Ürün": ["yanlış", "farklı", "başka", "istedigim"],
            "Eksik Ürün": ["eksik", "yok", "tam değil", "parça"],
            "Kargo Gecikmesi": ["gecikti", "geç", "zaman", "kargo", "teslimat"],
            "Kargo Firması Problemi": ["kargo firması", "kurye", "dağıtım"],
            "İade/Değişim Sorunu": ["iade", "değişim", "para iadesi"],
            "Ödeme/Fatura Sorunu": ["fatura", "ödeme", "para", "kart"],
            "Müşteri Hizmetleri Sorunu": ["müşteri hizmetleri", "temsilci", "destek"],
            "Paketleme/Ambalaj Problemi": ["paket", "ambalaj", "kutu", "ezik"],
            "Ürün Açıklaması Yanıltıcı": ["açıklama", "fotoğraf", "özellik"],
            "Hizmet Kalite Sorunu": ["hizmet", "kalite", "personel"],
            "Teknik/Uygulama Sorunu": ["teknik", "uygulama", "yazılım", "hata"]
        }
    
    def categorize_text(self, text: str) -> Tuple[str, float]:
        """Metni otomatik kategorize etme"""
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score
        
        if max(scores.values()) > 0:
            predicted_category = max(scores, key=scores.get)
            confidence = min(scores[predicted_category] / 3.0, 1.0)
            return predicted_category, confidence
        else:
            return "Bilinmeyen", 0.0
    
    def clean_text(self, text: str) -> str:
        """Metin temizleme"""
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,!?ğüşıöçĞÜŞIİÖÇ]', '', text)
        text = text.strip()
        
        if len(text) < 5:
            return ""
        
        return text
    
    def add_complaint(self, text: str, source: str = "manual", 
                     category: Optional[str] = None) -> Dict[str, Any]:
        """Şikayet ekleme"""
        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return None
        
        if category is None:
            category, confidence = self.categorize_text(cleaned_text)
        else:
            confidence = 1.0
        
        complaint = {
            'text': cleaned_text,
            'category': category,
            'confidence': confidence,
            'source': source,
            'date': pd.Timestamp.now().isoformat()
        }
        
        self.collected_data.append(complaint)
        return complaint
    
    def get_dataframe(self) -> pd.DataFrame:
        """Toplanan veriyi DataFrame'e çevir"""
        if not self.collected_data:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.collected_data)
        df = df.drop_duplicates(subset=['text'], keep='first')
        
        logger.info(f"Toplam veri: {len(df)} kayıt")
        logger.info(f"Kategori dağılımı:\n{df['category'].value_counts()}")
        
        return df

class ComplaintClassificationPipeline:
    """
    Müşteri şikayet kategorilendirme pipeline'ı
    """
    
    def __init__(self):
        """Pipeline bileşenleri"""
        self.tfidf_vectorizer = None
        self.feature_scaler = None
        self.model = None
        self.categories = None
        self.is_trained = False
    
    def load_data(self, data_path: str = None) -> pd.DataFrame:
        """
        Veri setini yükler
        
        Args:
            data_path: Veri dosyası yolu
            
        Returns:
            Yüklenen dataframe
        """
        if data_path is None:
            data_path = DATA_PATHS["complaints_data"]
        
        logger.info(f"Veri yükleniyor: {data_path}")
        df = pd.read_csv(data_path)
        
        logger.info(f"Veri boyutu: {df.shape}")
        logger.info(f"Kategoriler: {df['complaint_category'].value_counts().to_dict()}")
        
        return df
    
    def preprocess_text(self, text: str) -> str:
        """
        Metin ön işleme
        
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
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[Any, pd.Series]:
        """
        Özellik hazırlama
        
        Args:
            df: Input dataframe
            
        Returns:
            Özellik matrisi ve hedef değişken
        """
        logger.info("Özellikler hazırlanıyor...")
        
        # Metin temizleme
        df['cleaned_text'] = df['complaint_text'].apply(self.preprocess_text)
        
        # Ek özellikler
        df['text_length'] = df['complaint_text'].str.len()
        df['word_count'] = df['complaint_text'].str.split().str.len()
        
        # TF-IDF vektörleştirme
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
            sublinear_tf=True
        )
        
        X_text = self.tfidf_vectorizer.fit_transform(df['cleaned_text'])
        
        # Sayısal özellikler
        self.feature_scaler = StandardScaler()
        X_numerical = self.feature_scaler.fit_transform(
            df[['text_length', 'word_count']].values
        )
        
        # Özellikleri birleştir
        X_combined = hstack([X_text, csr_matrix(X_numerical)])
        y = df['complaint_category']
        
        logger.info(f"Özellik matrisi boyutu: {X_combined.shape}")
        
        return X_combined, y
    
    def train_model(self, X: Any, y: pd.Series) -> Dict[str, Any]:
        """
        Model eğitimi
        
        Args:
            X: Özellik matrisi
            y: Hedef değişken
            
        Returns:
            Eğitim sonuçları
        """
        logger.info("Model eğitimi başlatılıyor...")
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Model
        self.model = LogisticRegression(
            C=1.0,
            penalty='l2',
            solver='liblinear',
            random_state=42,
            max_iter=1000,
            class_weight='balanced'
        )
        
        # Eğitim
        self.model.fit(X_train, y_train)
        self.categories = self.model.classes_
        self.is_trained = True
        
        # Performans değerlendirme
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=cv, scoring='accuracy')
        
        results = {
            'test_accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'test_size': len(y_test),
            'train_size': len(y_train)
        }
        
        logger.info(f"Model eğitimi tamamlandı. Test doğruluğu: {accuracy:.4f}")
        
        return results
    
    def save_model(self, output_dir: Path = None) -> Dict[str, str]:
        """
        Model kaydetme
        
        Args:
            output_dir: Kayıt dizini
            
        Returns:
            Kaydedilen dosya yolları
        """
        if output_dir is None:
            output_dir = MODELS_DIR
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("Model kaydediliyor...")
        
        # Model kaydetme
        model_path = output_dir / 'final_model.pkl'
        joblib.dump(self.model, model_path)
        
        # TF-IDF vectorizer kaydetme
        tfidf_path = output_dir / 'tfidf_vectorizer.pkl'
        joblib.dump(self.tfidf_vectorizer, tfidf_path)
        
        # Feature scaler kaydetme
        scaler_path = output_dir / 'feature_scaler.pkl'
        joblib.dump(self.feature_scaler, scaler_path)
        
        # Metadata kaydetme
        metadata = {
            'model_type': 'LogisticRegression',
            'categories': self.categories.tolist(),
            'features': self.tfidf_vectorizer.get_feature_names_out().shape[0] if self.tfidf_vectorizer else 0,
            'training_info': {
                'is_trained': self.is_trained,
                'has_vectorizer': self.tfidf_vectorizer is not None,
                'has_scaler': self.feature_scaler is not None
            }
        }
        
        import json
        metadata_path = output_dir / 'pipeline_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        paths = {
            'model': str(model_path),
            'tfidf': str(tfidf_path),
            'scaler': str(scaler_path),
            'metadata': str(metadata_path)
        }
        
        logger.info(f"Model kaydedildi: {paths}")
        
        return paths
    
    def load_model(self, model_dir: Path = None) -> bool:
        """
        Model yükleme
        
        Args:
            model_dir: Model dizini
            
        Returns:
            Yükleme başarısı
        """
        if model_dir is None:
            model_dir = MODELS_DIR
        
        try:
            logger.info("Pipeline modeli yükleniyor...")
            
            # Model yükleme
            model_path = model_dir / 'final_model.pkl'
            self.model = joblib.load(model_path)
            
            # TF-IDF vectorizer yükleme
            tfidf_path = model_dir / 'tfidf_vectorizer.pkl'
            self.tfidf_vectorizer = joblib.load(tfidf_path)
            
            # Feature scaler yükleme
            scaler_path = model_dir / 'feature_scaler.pkl'
            self.feature_scaler = joblib.load(scaler_path)
            
            # Metadata yükleme
            metadata_path = model_dir / 'pipeline_metadata.json'
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                self.categories = metadata['categories']
            
            self.is_trained = True
            
            logger.info("Pipeline modeli başarıyla yüklendi!")
            
            return True
            
        except Exception as e:
            logger.error(f"Model yükleme hatası: {e}")
            return False
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Tahmin yapma
        
        Args:
            text: Tahmin edilecek metin
            
        Returns:
            Tahmin sonucu
        """
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş!")
        
        # Metin ön işleme
        cleaned_text = self.preprocess_text(text)
        
        # Özellik çıkarma
        text_features = self.tfidf_vectorizer.transform([cleaned_text])
        text_length = len(text)
        word_count = len(text.split())
        numerical_features = self.feature_scaler.transform([[text_length, word_count]])
        
        # Özellikleri birleştir
        features = hstack([text_features, csr_matrix(numerical_features)])
        
        # Tahmin
        prediction = self.model.predict(features)[0]
        probabilities = self.model.predict_proba(features)[0]
        
        # Sonuç
        result = {
            'prediction': prediction,
            'confidence': float(probabilities.max()),
            'all_probabilities': {
                cat: float(prob) for cat, prob in zip(self.categories, probabilities)
            },
            'text_length': len(text),
            'word_count': word_count
        }
        
        return result
    
    def evaluate_model(self, X_test: Any, y_test: pd.Series) -> Dict[str, Any]:
        """
        Model değerlendirme
        
        Args:
            X_test: Test özellikleri
            y_test: Test hedefi
            
        Returns:
            Değerlendirme sonuçları
        """
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş!")
        
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)
        
        from sklearn.metrics import precision_score, recall_score, f1_score
        
        results = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision_weighted': precision_score(y_test, y_pred, average='weighted'),
            'recall_weighted': recall_score(y_test, y_pred, average='weighted'),
            'f1_weighted': f1_score(y_test, y_pred, average='weighted'),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        return results
    
    def run_full_pipeline(self, data_path: str = None, save_model: bool = True) -> Dict[str, Any]:
        """
        Tam pipeline çalıştırma
        
        Args:
            data_path: Veri dosyası yolu
            save_model: Model kaydedilsin mi
            
        Returns:
            Pipeline sonuçları
        """
        logger.info("Tam pipeline çalıştırılıyor...")
        
        # 1. Veri yükleme
        df = self.load_data(data_path)
        
        # 2. Özellik hazırlama
        X, y = self.prepare_features(df)
        
        # 3. Model eğitimi
        training_results = self.train_model(X, y)
        
        # 4. Model kaydetme
        saved_paths = {}
        if save_model:
            saved_paths = self.save_model()
        
        # Pipeline özeti
        pipeline_summary = {
            'data_shape': df.shape,
            'features_shape': X.shape,
            'categories': self.categories.tolist(),
            'training_results': training_results,
            'saved_paths': saved_paths,
            'status': 'success'
        }
        
        logger.info("Pipeline başarıyla tamamlandı!")
        
        return pipeline_summary

# Pipeline instance
pipeline = ComplaintClassificationPipeline()
data_collector = TurkeyDataCollector()

def run_pipeline(data_path: str = None, save: bool = True) -> Dict[str, Any]:
    """
    Pipeline çalıştırma wrapper fonksiyonu
    
    Args:
        data_path: Veri dosyası yolu
        save: Model kaydedilsin mi
        
    Returns:
        Pipeline sonuçları
    """
    return pipeline.run_full_pipeline(data_path, save)

def expand_categories_9_to_12(text: str, category: str) -> str:
    """
    9 İngilizce kategoriyi 12 Türkçe kategoriye genişlet

    Args:
        text: Şikayet metni
        category: Orijinal kategori

    Returns:
        Genişletilmiş kategori
    """
    text_lower = text.lower()

    # Delivery Issues mapping
    if category == "Delivery Issues":
        if any(keyword in text_lower for keyword in ["gecik", "geç", "zaman", "teslimat"]):
            return "Kargo Gecikmesi"
        elif any(keyword in text_lower for keyword in ["kurye", "dağıtım", "kargo firması", "şube", "teslim edilemedi"]):
            return "Kargo Firması Problemi"
        else:
            return "Kargo Gecikmesi"  # default

    # Product Quality mapping
    elif category == "Product Quality":
        if any(keyword in text_lower for keyword in ["kalite", "bozuk", "kusur"]):
            return "Ürün Kalite Sorunu"
        elif any(keyword in text_lower for keyword in ["paket", "ambalaj", "kutu", "ezik"]):
            return "Paketleme/Ambalaj Problemi"
        elif any(keyword in text_lower for keyword in ["açıklama", "fotoğraf", "yanıltıcı"]):
            return "Ürün Açıklaması Yanıltıcı"
        else:
            return "Ürün Kalite Sorunu"  # default

    # Direct mappings
    elif category == "Customer Service":
        return "Müşteri Hizmetleri Sorunu"
    elif category == "Technical Support":
        return "Teknik/Uygulama Sorunu"
    elif category == "Return/Refund":
        return "İade/Değişim Sorunu"
    elif category == "Billing Issues":
        return "Ödeme/Fatura Sorunu"
    elif category == "Website Issues":
        return "Teknik/Uygulama Sorunu"
    elif category == "Service Outage":
        return "Hizmet Kalite Sorunu"
    elif category == "Fraud Issues":
        return "Ödeme/Fatura Sorunu"

    # Default fallback
    return category

def collect_and_train(complaints: List[Dict[str, str]], save: bool = True) -> Dict[str, Any]:
    """
    Şikayetleri topla ve modeli eğit

    Args:
        complaints: Şikayet listesi [{'text': '...', 'category': '...'}, ...]
        save: Model kaydedilsin mi

    Returns:
        Pipeline sonuçları
    """
    logger.info(f"Veri toplama başlıyor: {len(complaints)} şikayet")

    # Şikayetleri collector'a ekle
    for complaint in complaints:
        data_collector.add_complaint(
            text=complaint.get('text', ''),
            source=complaint.get('source', 'manual'),
            category=complaint.get('category')
        )

    # DataFrame'e çevir
    df = data_collector.get_dataframe()

    if df.empty:
        logger.error("Hiç veri toplanamadı!")
        return {'status': 'error', 'message': 'No data collected'}

    # 9→12 label genişletme
    df['category_new'] = df.apply(lambda row: expand_categories_9_to_12(row['text'], row['category']), axis=1)

    # Veriyi kaydet
    output_path = Path(DATA_PATHS.get("complaints_data", "data/raw/complaints.csv"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Kolon adlarını rename et
    df_renamed = df.rename(columns={
        'text': 'complaint_text',
        'category': 'complaint_category',
        'category_new': 'complaint_category_new'
    })

    df_renamed.to_csv(output_path, index=False, encoding='utf-8')
    logger.info(f"Veri kaydedildi: {output_path}")

    # Pipeline çalıştır
    return pipeline.run_full_pipeline(str(output_path), save)

def add_complaint_to_dataset(text: str, category: Optional[str] = None, 
                            source: str = "manual") -> Dict[str, Any]:
    """
    Tek bir şikayet ekle
    
    Args:
        text: Şikayet metni
        category: Kategori (opsiyonel)
        source: Veri kaynağı
        
    Returns:
        Eklenen şikayet
    """
    return data_collector.add_complaint(text, source, category)

def get_collected_data() -> pd.DataFrame:
    """Toplanan tüm veriyi al"""
    return data_collector.get_dataframe()