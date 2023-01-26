from aiofile import async_open
from fastapi import APIRouter, File, UploadFile

router = APIRouter()


async def read_image(file: UploadFile) -> bytes:
    """Считать изображение из тела запроса"""
    byte_img = await file.read()
    return byte_img


@router.get("/ping")
async def pong():
    return {
        "ping": "pong!",
        "environment": "Test task",
        "testing": "testing",
    }


@router.post("/send_file")
async def save_file(img: UploadFile = File(...)):
    image = await read_image(img)
    async with async_open("/uploads/filename.jpg", 'wb') as f:
        await f.write(image)
    return
