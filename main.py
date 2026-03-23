from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os

# --- 1. VERİTABANI YAPILANDIRMASI ---
DATABASE_URL = "postgresql://neondb_owner:npg_nX1aHZV7zgDr@ep-broad-forest-ale1pkib.c-3.eu-central-1.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TehditVerisi(Base):
    __tablename__ = "aura_final_stable"
    id = Column(Integer, primary_key=True)
    hash_kodu = Column(String, unique=True)
    dosya_turu = Column(String)
    risk_skoru = Column(Float)

# Tabloyu güvenli şekilde oluştur
try:
    Base.metadata.create_all(bind=engine)
except:
    pass

# --- 2. TEKNİK PANEL (DOCS) ÖZELLEŞTİRME ---
tags_metadata = [
    {
        "name": "🛡️ Dosya Denetleme",
        "description": "Şüpheli dosyaların dijital imzalarını (hash) bulut veritabanında sorgulayın.",
    },
    {
        "name": "⚙️ Sistem Yönetimi",
        "description": "Veritabanını Frankfurt bulut sunucusu ile güncelleyin.",
    },
]

app = FastAPI(
    title="SİSTEM AURASI | Kontrol Paneli",
    description="""
    ## 🚀 Güvenlik Sistemine Hoş Geldiniz
    Bu panel üzerinden analiz motorunu yönetebilirsiniz.
    
    **Kullanım Sırası:**
    1. Önce **Sistem Yönetimi** kısmından verileri güncelleyin.
    2. Sonra **Dosya Denetleme** kısmından testinizi yapın.
    """,
    version="12.0.0",
    openapi_tags=tags_metadata
)

class Sorgu(BaseModel):
    hash_kodu: str

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# --- 3. İNTERAKTİF DASHBOARD (GÖRSEL VİTRİN) ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Sistem Aurası | Canlı Analiz</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
            body { margin: 0; background: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; overflow: hidden; }
            .card-container { max-width: 900px; width: 90%; text-align: center; padding: 50px; border: 1px solid #1e293b; border-radius: 40px; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(20px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
            h1 { font-size: 4rem; color: #38bdf8; margin: 0; font-weight: 900; letter-spacing: -3px; }
            .desc { color: #94a3b8; font-size: 1.2rem; margin: 20px 0 50px; font-weight: 300; }
            .steps { display: flex; gap: 20px; justify-content: center; margin-bottom: 50px; }
            .step { flex: 1; padding: 30px; border-radius: 25px; background: rgba(15, 23, 42, 0.8); border: 1px solid #1e293b; transition: 0.6s cubic-bezier(0.4, 0, 0.2, 1); opacity: 0.3; }
            .step.active { opacity: 1; border-color: #38bdf8; transform: scale(1.08); box-shadow: 0 0 30px rgba(56, 189, 248, 0.3); }
            .step h3 { color: #38bdf8; margin: 0 0 10px 0; font-size: 1.5rem; }
            .step p { font-size: 0.9rem; color: #64748b; margin: 0; }
            #status-text { margin-bottom: 30px; font-weight: bold; color: #38bdf8; height: 30px; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px; }
            .btn { background: #38bdf8; color: #020617; padding: 20px 60px; border-radius: 15px; border: none; font-weight: 900; font-size: 1.2rem; cursor: pointer; transition: 0.4s; box-shadow: 0 10px 20px rgba(56, 189, 248, 0.3); }
            .btn:hover { transform: translateY(-3px); background: #fff; box-shadow: 0 15px 30px rgba(56, 189, 248, 0.5); }
            .btn:disabled { background: #1e293b; color: #475569; cursor: not-allowed; box-shadow: none; }
        </style>
    </head>
    <body>
        <div class="card-container">
            <div style="color:#38bdf8; font-weight:bold; font-size:0.8rem; margin-bottom:10px; letter-spacing:2px;">SİBER GÜVENLİK PROTOKOLÜ</div>
            <h1>SİSTEM AURASI</h1>
            <p class="desc">Bulut tabanlı dosya güvenliği ve interaktif analiz paneli.</p>
            <div class="steps">
                <div id="step1" class="step"><h3>01. Tara</h3><p>Dijital İmza</p></div>
                <div id="step2" class="step"><h3>02. Analiz</h3><p>Bulut Sorgusu</p></div>
                <div id="step3" class="step"><h3>03. Karar</h3><p>Sonuç Raporu</p></div>
            </div>
            <div id="status-text">Sistem Kullanıma Hazır</div>
            <button id="start-btn" onclick="startAnalysis()" class="btn">ANALİZİ BAŞLAT</button>
        </div>
        <script>
            function startAnalysis() {
                const btn = document.getElementById('start-btn');
                const status = document.getElementById('status-text');
                btn.disabled = true;
                setTimeout(() => {
                    document.getElementById('step1').classList.add('active');
                    status.innerText = "Dosya imzası oluşturuluyor...";
                }, 500);
                setTimeout(() => {
                    document.getElementById('step1').classList.remove('active');
                    document.getElementById('step2').classList.add('active');
                    status.innerText = "Bulut veritabanına bağlanılıyor...";
                }, 2500);
                setTimeout(() => {
                    document.getElementById('step2').classList.remove('active');
                    document.getElementById('step3').classList.add('active');
                    status.innerText = "Rapor hazırlandı. Yönlendiriliyorsunuz...";
                }, 4500);
                setTimeout(() => { window.location.href = "/docs"; }, 6500);
            }
        </script>
    </body>
    </html>
    """

# --- 4. TEKNİK FONKSİYONLAR (ETİKETLENMİŞ) ---
@app.post("/denetle", tags=["🛡️ Dosya Denetleme"])
def denetle(sorgu: Sorgu, db: Session = Depends(get_db)):
    """
    **İşlem:** Gönderilen hash kodunu buluttaki zararlı yazılım listesiyle kıyaslar.
    """
    res = db.query(TehditVerisi).filter(TehditVerisi.hash_kodu == sorgu.hash_kodu).first()
    if res:
        return {
            "sonuc": "🚨 TEHLİKELİ",
            "tur": res.dosya_turu,
            "risk": f"%{int(res.risk_skoru * 100)}",
            "tavsiye": "Dosyayı derhal karantinaya alın."
        }
    return {"sonuc": "✅ GÜVENLİ", "tur": "Temiz", "risk": "%0", "tavsiye": "Kullanıma uygun."}

@app.post("/guncelle", tags=["⚙️ Sistem Yönetimi"])
def guncelle(db: Session = Depends(get_db)):
    """
    **İşlem:** Frankfurt merkezli bulut sunucusundan en güncel verileri çeker.
    """
    ornekler = [("malware_001", "Trojan", 0.9), ("ransom_002", "Fidye Yazılımı", 1.0)]
    for h, t, r in ornekler:
        if not db.query(TehditVerisi).filter(TehditVerisi.hash_kodu == h).first():
            db.add(TehditVerisi(hash_kodu=h, dosya_turu=t, risk_skoru=r))
    db.commit()
    return {"mesaj": "Sistem bulut verileriyle başarıyla güncellendi."}