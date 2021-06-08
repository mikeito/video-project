from typing import Optional

from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi import Header

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from camera import WebcamCamera

app = FastAPI()

CHUNK_SIZE = 1024*1024
# video_path = Path("overload.mp4")
video_path = Path("natnatsu_16.mp4")

origins = [
    "http://localhost:8080",
    "http://192.168.43.180:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/video")
async def video_endpoint(range: str = Header(None)):
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        filesize = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


def generate():
    webcam = WebcamCamera(0)
    # camera here is an instance of webcamCamera which is passed in dynamic_stream
    while True:
        frame_data = webcam.getFrames()
        # yield b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + frame_data + b'\r\n'
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame_data) + b'\r\n'


@app.get("/streaming")
async def dynamic_stream():
    try:
        return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")
    except:
        return "error"

