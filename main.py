from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from image_fetcher import fetch_images
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class ProductRequest(BaseModel):
    name: str
    num_images: int = 3

@app.post("/fetch-images/")
async def fetch_images_endpoint(request: ProductRequest):
    try:
        image_paths = fetch_images(request.name, request.num_images)
        
        if not image_paths:
            raise HTTPException(status_code=404, detail="Bu istek için yeni rastgele resim bulunamadı veya yükleme başarısız oldu")
        
        return {
            "fetched_images": image_paths
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"hata oluştu: {str(e)}")

