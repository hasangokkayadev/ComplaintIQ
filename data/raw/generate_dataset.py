import csv
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
random.seed(42)

# Complaint categories and their weights
complaint_categories = [
    "Delivery Issues", "Billing Issues", "Product Quality", "Customer Service", 
    "Technical Support", "Return/Refund", "Website Issues", "Service Outage", "Fraud Issues"
]

# Product types
product_types = [
    "Online Shopping", "E-commerce", "Electronics", "Grocery", 
    "Software", "Financial Services", "Retail", "Telecom", 
    "Home & Garden", "Utilities", "Insurance", "Automotive",
    "Fashion", "Books & Media", "Health & Beauty"
]

# Complaint channels
channels = ["Phone", "Email", "Web Form", "Chat", "Mobile App"]
priority_levels = ["Low", "Medium", "High", "Critical"]
resolution_statuses = ["Pending", "In Progress", "Resolved", "Escalated"]

# Complaint templates for each category
complaint_templates = {
    "Delivery Issues": [
        "Siparişim henüz gelmedi, teslimat süresi çok uzun",
        "Kargo hasarlı geldi, paket açılmış durumda",
        "Yanlış adrese gönderilmiş, başka birisi almış",
        "Teslimat süresi tahmin edilenden çok uzun sürdü",
        "Kargo kaybolmuş, takip numarası işlemiyor",
        "Kurye gelmedi, kapıda kimse yok denildi",
        "Ürün teslim edilmemiş ama sistemde teslim gözüküyor",
        "Belirtilen saatte teslimat yapılmadı"
    ],
    "Billing Issues": [
        "Faturalandırma hatası var, yanlış tutar çıkmış",
        "Fatura bilgileri güncellenmemiş",
        "Ödeme işlemi başarısız oldu ama ücret kesildi",
        "Aylık abonelik ücreti yanlış hesaplanmış",
        "İndirim uygulanmamış, tam fiyat çıkmış",
        "Vergi hesaplaması yanlış yapılmış",
        "Ödeme planı yanlış uygulanmış",
        "Gizli ücretler çıkmış, açıklanmamış"
    ],
    "Product Quality": [
        "Ürün kusurlu geldi, çalışmıyor",
        "Ürün kalitesi beklentimin altında",
        "Ürün bozuk geldi, hemen iade ediyorum",
        "Ürün fotoğraftaki gibi değil",
        "Kalite standartlarına uymuyor",
        "Ürün çok çabuk bozuldu",
        "Malzeme kalitesi düşük",
        "Ürün beklendiği gibi performans göstermiyor"
    ],
    "Customer Service": [
        "Müşteri temsilcisi kaba davrandı",
        "Sorunumu çözemediler, sürekli başka bölüme yönlendiriyorlar",
        "Müşteri hizmetleri çok yavaş",
        "Bilgilendirme yetersiz ve yanlış",
        "Şikayetimi ciddiye almadılar",
        "Uzun beklemeler sonrası bağlantı koptu",
        "İlgisiz davrandılar, çözüm sunmadılar",
        "Profesyonel olmayan davranış sergiledi"
    ],
    "Technical Support": [
        "Teknik destek sorunumu çözemiyor",
        "Ürün kurulumu yapamıyorum",
        "Yazılım hatası var, sürekli çöküyor",
        "Teknik dokümantasyon eksik",
        "Driver güncelleme problemi yaşıyorum",
        "Ağ bağlantısı kuramıyorum",
        "Donanım uyumluluk sorunu",
        "Teknik destek çok yavaş yanıt veriyor"
    ],
    "Return/Refund": [
        "Ürün iade süreci çok uzun sürüyor",
        "Para iadesi henüz hesabıma gelmedi",
        "İade politikası net değil",
        "İade işlemi reddedildi, sebep açıklanmadı",
        "İade kargo ücreti çok yüksek",
        "İade formu kabul edilmedi",
        "Para iadesi yanlış hesaba gönderildi",
        "İade işlemi tamamlanmış ama ücret gelmedi"
    ],
    "Website Issues": [
        "Web sitesi sürekli çöküyor",
        "Ödeme sayfası açılmıyor",
        "Arama özelliği çalışmıyor",
        "Site çok yavaş açılıyor",
        "Sayfa geçişleri sorunlu",
        "Mobil site uyumlu değil",
        "JavaScript hataları alıyorum",
        "Üye giriş yapamıyorum"
    ],
    "Service Outage": [
        "Hizmet sürekli kesiliyor",
        "Sistem bakımda ama bilgilendirilmedik",
        "Acil durumda hizmet alamadım",
        "Hizmet kalitesi çok düştü",
        "Planlı bakım bildirimi yapılmadı",
        "Servis kesintisi çok sık oluyor",
        "Yedekleme sistemi çalışmıyor",
        "Kritik sistemler çalışmıyor"
    ],
    "Fraud Issues": [
        "Kredi kartımdan izinsiz para çekilmiş",
        "Hesabım hack'lendi",
        "Sahte işlem gerçekleşti",
        "Kimlik avı mağduru oldum",
        "Kart bilgilerim çalınmış",
        "Fraud koruması çalışmıyor",
        "Şüpheli işlem tespit edilmedi",
        "Güvenlik açığı var"
    ]
}

def generate_complaint_text(category):
    """Generate a complaint text based on category"""
    templates = complaint_templates[category]
    return random.choice(templates)

def generate_complaints_data(n_samples=12000):
    """Generate synthetic customer complaints data"""
    
    data = []
    start_date = datetime(2023, 1, 1)
    
    # Category weights (Delivery Issues is most common)
    category_weights = [0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.05, 0.03, 0.02]
    
    for i in range(n_samples):
        # Select category based on weights
        category_idx = random.choices(range(len(complaint_categories)), weights=category_weights)[0]
        category = complaint_categories[category_idx]
        
        # Generate other features
        customer_id = 1000 + i
        complaint_text = generate_complaint_text(category)
        product_type = random.choice(product_types)
        
        # Generate date
        days_offset = random.randint(0, (datetime.now() - start_date).days)
        complaint_date = start_date + timedelta(days=days_offset)
        
        # Generate customer demographics
        customer_age = random.randint(18, 70)
        customer_tenure = random.randint(1, 60)
        
        # Generate other features
        complaint_channel = random.choice(channels)
        priority_level = random.choice(priority_levels)
        satisfaction_rating = random.randint(1, 5)
        resolution_status = random.choice(resolution_statuses)
        
        # Add some noise and realism
        if category == "Fraud Issues":
            priority_level = "Critical"
            satisfaction_rating = random.randint(1, 2)
        
        if category == "Service Outage":
            priority_level = random.choice(["High", "Critical"])
            satisfaction_rating = random.randint(1, 3)
            
        data.append([
            customer_id,
            complaint_text,
            category,
            product_type,
            complaint_date.strftime('%Y-%m-%d'),
            customer_age,
            customer_tenure,
            complaint_channel,
            priority_level,
            satisfaction_rating,
            resolution_status
        ])
    
    return data

# Generate the dataset
print("Generating customer complaints dataset...")
data = generate_complaints_data(12000)

# Save to CSV
with open('customer_complaints_full.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        'customer_id', 'complaint_text', 'complaint_category', 'product_type', 
        'complaint_date', 'customer_age', 'customer_tenure_months', 
        'complaint_channel', 'priority_level', 'satisfaction_rating', 'resolution_status'
    ])
    writer.writerows(data)

print(f"Dataset generated with {len(data)} rows")
print("Dataset saved to customer_complaints_full.csv")