# YTcut - AI Video Shorts Generator

YouTube videolarını otomatik olarak analiz eden, en iyi anları seçen ve dikey (Shorts/TikTok) formatına dönüştüren yapay zeka destekli araç.

## Kurulum ve Çalıştırma

Bu proje iki ana parçadan oluşur: **Backend** (Python) ve **Frontend** (Next.js). İkisini aynı anda çalıştırmak için iki farklı terminal penceresi kullanmalısınız.

### 1. Backend'i Başlatma (Terminal 1)
Bu terminal video indirme ve işleme işlemlerini yapacak.

```powershell
cd backend
# Gerekli paketleri yükle (sadece ilk seferde)
python -m pip install -r requirements.txt

# Sunucuyu başlat
python -m uvicorn main:app --reload
```
*Backend `http://localhost:8000` adresinde çalışacaktır.*

### 2. Frontend'i Başlatma (Terminal 2)
Bu terminal kullanıcı arayüzünü gösterecek.

```powershell
cd frontend
# Gerekli paketleri yükle (sadece ilk seferde)
npm install

# Uygulamayı başlat
npm run dev
```
*Frontend `http://localhost:3000` adresinde çalışacaktır. Tarayıcıda bu adrese gidin.*

## Gereksinimler
- Python 3.8+
- Node.js 18+
- ffmpeg (Sistem yoluna eklenmiş olmalı)
- Gemini API Anahtarı (`backend/.env` dosyasında)
