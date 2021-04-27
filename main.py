from fastapi import FastAPI
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from fractal_pyrs import render
from PIL import Image
import uuid
import io

app = FastAPI() 

class Config(BaseModel):
    height: int 
    width: int
    cx: float
    cy: float
    zoom: float
    iter: int

async def image_streamer(img):
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    data = img_byte_arr.getvalue()
    for b in range(len(data)):
        yield data

@app.get("/alive")
async def alive():
    return {"status": "alive"}

@app.post("/mandelbrot")
async def mandelbrot(config: Config):
    """
    Generates a Mandelbrot fractal image with the specified parameters. The 
    link to the static resource is returned so that the caller may access it
    with an HTTP get using a binary format as opposed to base64 encoding the 
    image in the response payload.
    """
    data = render(config.width, 
                  config.height, 
                  config.cx, 
                  config.cy, 
                  config.zoom, 
                  config.iter)
    bytes_array = bytearray(data)
    byte_object = bytes(bytes_array)
    img = Image.frombytes("RGBA", (config.width, config.height), byte_object)
    return StreamingResponse(image_streamer(img))