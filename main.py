from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.post("/extract")
def extract_video(payload: VideoRequest):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)
            video_url = info.get('url')
            
            if not video_url:
                raise HTTPException(status_code=400, detail="Não foi possível obter o link do vídeo.")
                
            return {"download_url": video_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download-file")
def download_file(url: str):
    """Rota Proxy para forçar o download direto no dispositivo"""
    try:
        req = requests.get(url, stream=True)
        headers = {
            "Content-Disposition": 'attachment; filename="snapgram_video.mp4"',
            "Content-Type": "video/mp4"
        }
        return Response(content=req.content, headers=headers, media_type="video/mp4")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Falha ao transferir o arquivo.")
