"""
FastAPI Backend - ComplaintIQ API
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging
import sys
import os
from pathlib import Path

# Import our modules
sys.path.append(str(Path(__file__).parent))
from src.config import APP_CONFIG, API_CONFIG, BUSINESS_RULES
from src.inference import classifier, predict_complaint, batch_predict_complaints, get_categories
from src.pipeline import data_collector, collect_and_train, add_complaint_to_dataset, get_collected_data

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title=APP_CONFIG["title"],
    description=APP_CONFIG["description"],
    version=APP_CONFIG["version"],
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=2000, description="Şikayet metni")

class BatchPredictionRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=100, description="Şikayet metinleri listesi")

class ComplaintCollectionRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=2000, description="Şikayet metni")
    category: Optional[str] = Field(None, description="Kategori (opsiyonel)")
    source: str = Field("manual", description="Veri kaynağı")

class BatchComplaintCollectionRequest(BaseModel):
    complaints: List[Dict] = Field(..., description="Şikayet listesi")

class TrainingRequest(BaseModel):
    complaints: List[Dict] = Field(..., description="Eğitim için şikayet listesi")
    save_model: bool = Field(True, description="Model kaydedilsin mi")

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    all_probabilities: Dict[str, float]
    text_length: int
    word_count: int

class BatchPredictionResponse(BaseModel):
    results: List[Dict]
    total_processed: int
    processing_time: float

class CategoryInfo(BaseModel):
    category: str
    description: str
    priority_suggestion: str
    common_keywords: List[str]

class SystemInfo(BaseModel):
    model_type: str
    categories: List[str]
    supported_categories: List[str]
    min_confidence_threshold: float
    version: str
    uptime: str

# Health check endpoint
@app.get("/health")
async def health_check():
    """Sağlık kontrolü"""
    return {
        "status": "healthy",
        "timestamp": "2024-12-08T15:54:00Z",
        "service": "Şikayet Kategorilendirme API",
        "version": APP_CONFIG["version"]
    }

# Main prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict_single(request: PredictionRequest):
    """Tekil şikayet kategorilendirme"""
    try:
        logger.info(f"Tahmin isteği alındı: {len(request.text)} karakter")
        
        # Prediction
        result = classifier.predict_single(request.text)
        
        # Response
        response = PredictionResponse(
            prediction=result['prediction'],
            confidence=result['confidence'],
            all_probabilities=result['all_probabilities'],
            text_length=result['text_length'],
            word_count=result['word_count']
        )
        
        logger.info(f"Tahmin tamamlandı: {result['prediction']} (güven: {result['confidence']:.3f})")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation hatası: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail="Tahmin işlemi sırasında hata oluştu")

# Batch prediction endpoint
@app.post("/batch_predict", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """Toplu şikayet kategorilendirme"""
    try:
        logger.info(f"Toplu tahmin isteği alındı: {len(request.texts)} metin")
        
        import time
        start_time = time.time()
        
        # Batch prediction
        results = classifier.predict_batch(request.texts)
        
        processing_time = time.time() - start_time
        
        # Response
        response = BatchPredictionResponse(
            results=results,
            total_processed=len(results),
            processing_time=processing_time
        )
        
        logger.info(f"Toplu tahmin tamamlandı: {len(results)} metin, {processing_time:.3f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Toplu tahmin hatası: {e}")
        raise HTTPException(status_code=500, detail="Toplu tahmin işlemi sırasında hata oluştu")

# Categories endpoint
@app.get("/categories", response_model=List[str])
async def get_supported_categories():
    """Desteklenen kategorileri getir"""
    try:
        categories = get_categories()
        logger.info(f"Kategoriler istendi: {len(categories)} kategori")

        # 12'li kategori setini doğrula
        if len(categories) != 12:
            logger.warning(f"Beklenen 12 kategori, bulunan: {len(categories)}")

        return categories
    except Exception as e:
        logger.error(f"Kategori listesi hatası: {e}")
        raise HTTPException(status_code=500, detail="Kategori listesi alınamadı")

# Category info endpoint
@app.get("/categories/info", response_model=List[CategoryInfo])
async def get_category_info():
    """Kategori detay bilgileri"""
    try:
        categories = get_categories()
        category_infos = []
        
        for category in categories:
            info = classifier.get_category_info(category)
            category_infos.append(CategoryInfo(
                category=info['category'],
                description=info['description'],
                priority_suggestion=info['priority_suggestion'],
                common_keywords=info['common_keywords']
            ))
        
        logger.info(f"Kategori bilgileri istendi: {len(category_infos)} kategori")
        return category_infos
        
    except Exception as e:
        logger.error(f"Kategori bilgisi hatası: {e}")
        raise HTTPException(status_code=500, detail="Kategori bilgileri alınamadı")

# System info endpoint
@app.get("/info", response_model=SystemInfo)
async def get_system_info():
    """Sistem bilgileri"""
    try:
        import time
        uptime = "2024-12-08T15:54:00Z"  # Simplified for demo

        # 12'li kategori setini doğrula
        supported_categories = BUSINESS_RULES["supported_categories"]
        if len(supported_categories) != 12:
            logger.warning(f"Beklenen 12 kategori, bulunan: {len(supported_categories)}")

        info = SystemInfo(
            model_type="LogisticRegression",
            categories=list(classifier.categories),
            supported_categories=supported_categories,
            min_confidence_threshold=BUSINESS_RULES["min_confidence_threshold"],
            version=APP_CONFIG["version"],
            uptime=uptime
        )

        return info

    except Exception as e:
        logger.error(f"Sistem bilgisi hatası: {e}")
        raise HTTPException(status_code=500, detail="Sistem bilgileri alınamadı")

# Statistics endpoint
@app.get("/stats")
async def get_statistics():
    """İstatistik bilgileri"""
    try:
        stats = {
            "total_categories": len(get_categories()),
            "model_accuracy": "85%+",
            "average_prediction_time": "< 100ms",
            "supported_languages": ["Türkçe"],
            "api_version": APP_CONFIG["version"],
            "last_updated": "2024-12-08",
            "deployment_date": "2024-12-08"
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"İstatistik hatası: {e}")
        raise HTTPException(status_code=500, detail="İstatistikler alınamadı")

# File upload endpoint for batch processing
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """CSV dosyası yükleme ve toplu işleme"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Sadece CSV dosyaları destekleniyor")
        
        # Read file content
        content = await file.read()
        
        # Parse CSV
        import pandas as pd
        from io import StringIO
        
        df = pd.read_csv(StringIO(content.decode('utf-8')))
        
        if 'text' not in df.columns:
            raise HTTPException(status_code=400, detail="CSV dosyasında 'text' sütunu bulunamadı")
        
        # Process texts
        texts = df['text'].fillna('').tolist()
        
        import time
        start_time = time.time()
        
        results = classifier.predict_batch(texts)
        
        processing_time = time.time() - start_time
        
        # Add results to dataframe
        df_results = pd.DataFrame(results)
        df_results['text'] = texts[:len(results)]
        
        # Convert to dict for response
        response_data = {
            "total_processed": len(results),
            "processing_time": processing_time,
            "results": results,
            "file_info": {
                "filename": file.filename,
                "size": len(content),
                "rows": len(df)
            }
        }
        
        logger.info(f"Dosya işlendi: {file.filename}, {len(results)} satır")
        
        return JSONResponse(content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Dosya yükleme hatası: {e}")
        raise HTTPException(status_code=500, detail="Dosya işlenirken hata oluştu")

# Data collection endpoints
@app.post("/collect/complaint")
async def collect_complaint(request: ComplaintCollectionRequest):
    """Tekil şikayet toplama"""
    try:
        logger.info(f"Şikayet toplanıyor: {len(request.text)} karakter")
        
        complaint = add_complaint_to_dataset(
            text=request.text,
            category=request.category,
            source=request.source
        )
        
        if complaint is None:
            raise HTTPException(status_code=400, detail="Şikayet metni çok kısa")
        
        logger.info(f"Şikayet toplandı: {complaint['category']}")
        
        return {
            "status": "success",
            "complaint": complaint,
            "message": "Şikayet başarıyla toplandı"
        }
        
    except Exception as e:
        logger.error(f"Şikayet toplama hatası: {e}")
        raise HTTPException(status_code=500, detail="Şikayet toplanırken hata oluştu")

@app.post("/collect/batch")
async def collect_batch_complaints(request: BatchComplaintCollectionRequest):
    """Toplu şikayet toplama"""
    try:
        logger.info(f"Toplu şikayet toplanıyor: {len(request.complaints)} şikayet")
        
        collected = []
        for complaint in request.complaints:
            result = add_complaint_to_dataset(
                text=complaint.get('text', ''),
                category=complaint.get('category'),
                source=complaint.get('source', 'batch')
            )
            if result:
                collected.append(result)
        
        logger.info(f"Toplu şikayet toplandı: {len(collected)} şikayet")
        
        return {
            "status": "success",
            "total_collected": len(collected),
            "complaints": collected,
            "message": f"{len(collected)} şikayet başarıyla toplandı"
        }
        
    except Exception as e:
        logger.error(f"Toplu şikayet toplama hatası: {e}")
        raise HTTPException(status_code=500, detail="Toplu şikayet toplanırken hata oluştu")

@app.get("/collect/data")
async def get_collected_complaints():
    """Toplanan şikayetleri getir"""
    try:
        df = get_collected_data()
        
        if df.empty:
            return {
                "status": "success",
                "total_complaints": 0,
                "complaints": [],
                "message": "Henüz şikayet toplanmadı"
            }
        
        return {
            "status": "success",
            "total_complaints": len(df),
            "category_distribution": df['category'].value_counts().to_dict(),
            "complaints": df.to_dict('records'),
            "message": f"Toplam {len(df)} şikayet bulundu"
        }
        
    except Exception as e:
        logger.error(f"Şikayet getirme hatası: {e}")
        raise HTTPException(status_code=500, detail="Şikayetler alınamadı")

@app.post("/train")
async def train_model(request: TrainingRequest):
    """Toplanan şikayetlerle modeli eğit"""
    try:
        logger.info(f"Model eğitimi başlıyor: {len(request.complaints)} şikayet")
        
        results = collect_and_train(
            complaints=request.complaints,
            save=request.save_model
        )
        
        logger.info(f"Model eğitimi tamamlandı")
        
        return {
            "status": "success",
            "training_results": results,
            "message": "Model başarıyla eğitildi"
        }
        
    except Exception as e:
        logger.error(f"Model eğitim hatası: {e}")
        raise HTTPException(status_code=500, detail="Model eğitilirken hata oluştu")

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "ComplaintIQ - AI destekli Şikayet Kategorilendirme API",
        "version": APP_CONFIG["version"],
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "predict": "/predict - Tekil tahmin",
            "batch_predict": "/batch_predict - Toplu tahmin", 
            "categories": "/categories - Kategori listesi",
            "info": "/info - Sistem bilgileri",
            "stats": "/stats - İstatistikler",
            "collect_complaint": "/collect/complaint - Tekil şikayet toplama",
            "collect_batch": "/collect/batch - Toplu şikayet toplama",
            "get_collected": "/collect/data - Toplanan şikayetleri getir",
            "train": "/train - Modeli eğit"
        }
    }

# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"error": "Geçersiz input", "detail": str(exc)}
    )

@app.exception_handler(Exception)
async def general_error_handler(request, exc):
    logger.error(f"General error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "İç sunucu hatası", "detail": "Bir hata oluştu"}
    )

if __name__ == "__main__":
    import uvicorn
    
    # Port 8000 kullanılıyorsa 8001 kullan
    port = API_CONFIG["port"]
    try:
        logger.info(f"API başlatılıyor: {API_CONFIG['host']}:{port}")
        uvicorn.run(
            "api:app",
            host=API_CONFIG["host"],
            port=port,
            reload=API_CONFIG["reload"],
            workers=API_CONFIG["workers"]
        )
    except OSError:
        port = 8001
        logger.info(f"Port {API_CONFIG['port']} kullanılıyor, {port} kullanılıyor")
        uvicorn.run(
            "api:app",
            host=API_CONFIG["host"],
            port=port,
            reload=API_CONFIG["reload"],
            workers=API_CONFIG["workers"]
        )