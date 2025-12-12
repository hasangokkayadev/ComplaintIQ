"""
Konfigürasyon dosyası - Müşteri Şikayet Kategorilendirme Projesi
"""
import os
from pathlib import Path

# Proje yapısı
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Model konfigürasyonu
MODEL_CONFIG = {
    "model_path": MODELS_DIR / "final_model.pkl",
    "tfidf_path": MODELS_DIR / "tfidf_vectorizer.pkl", 
    "scaler_path": MODELS_DIR / "feature_scaler.pkl",
    "metadata_path": MODELS_DIR / "model_metadata.json",
}

# API konfigürasyonu
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": False,
    "workers": 1,
}

# Uygulama konfigürasyonu
APP_CONFIG = {
    "title": "ComplaintIQ",
    "description": "AI destekli müşteri şikayet kategorilendirme SaaS platformu",
    "version": "1.0.0",
    "author": "ComplaintIQ Team",
}

# Business kuralları
BUSINESS_RULES = {
    "min_confidence_threshold": 0.6,
    "max_prediction_time": 0.1,  # saniye
    "supported_categories": [
        "Ürün Kalite Sorunu",
        "Yanlış Ürün",
        "Eksik Ürün",
        "Kargo Gecikmesi",
        "Kargo Firması Problemi",
        "İade/Değişim Sorunu",
        "Ödeme/Fatura Sorunu",
        "Müşteri Hizmetleri Sorunu",
        "Paketleme/Ambalaj Problemi",
        "Ürün Açıklaması Yanıltıcı",
        "Hizmet Kalite Sorunu",
        "Teknik/Uygulama Sorunu"
    ],
    "text_limits": {
        "min_length": 10,
        "max_length": 2000,
    }
}

# Logging konfigürasyonu
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": PROJECT_ROOT / "logs" / "app.log",
}

# Veri dosya yolları
DATA_PATHS = {
    "complaints_data": RAW_DATA_DIR / "customer_complaints_full.csv",
    "processed_data": PROCESSED_DATA_DIR / "processed_complaints.csv",
}

# Environment variables
def get_env_var(key: str, default=None):
    """Environment variable al"""
    return os.getenv(key, default)

# Debug modu
DEBUG = get_env_var("DEBUG", "False").lower() == "true"

# Database (gelecekte kullanım için)
DATABASE_CONFIG = {
    "url": get_env_var("DATABASE_URL", "sqlite:///./complaints.db"),
    "echo": DEBUG,
}