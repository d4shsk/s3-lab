from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from s3_client import list_files, upload_file, delete_file, generate_presign_url
import os

app = FastAPI(title="S3 Lab Service", description="Simple FastAPI service for Yandex Object Storage (S3)")

@app.get("/files")
async def get_files():
    """Получить список файлов в бакете"""
    try:
        files = list_files()
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file_endpoint(file: UploadFile = File(...)):
    """Загрузить файл в бакет"""
    try:
        upload_file(file.file, file.filename)
        return {"message": f"Файл {file.filename} успешно загружен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/files/{filename}")
async def delete_file_endpoint(filename: str):
    """Удалить файл из бакета"""
    try:
        delete_file(filename)
        return {"message": f"Файл {filename} успешно удалён"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/presign/{filename}")
async def presign_file(filename: str):
    """Получить presign-ссылку для скачивания/просмотра файла"""
    try:
        url = generate_presign_url(filename)
        if url is None:
            raise HTTPException(status_code=404, detail="Файл не найден или недоступен")
        return {"presign_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))