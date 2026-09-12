from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/extract")
def extract_instagram_video(payload: URLRequest):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)
            
            video_url = None
            if 'url' in info:
                video_url = info['url']
            elif 'entries' in info and len(info['entries']) > 0:
                video_url = info['entries'][0]['url']
                
            if not video_url:
                raise HTTPException(status_code=400, detail="Mídia não encontrada.")
                
            return {
                "status": "success",
                "title": info.get('title', 'instagram_video'),
                "download_url": video_url
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
