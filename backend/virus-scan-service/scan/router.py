from fastapi import APIRouter, UploadFile, File
from .service import scan_file_with_clamav

router = APIRouter()

@router.post("/scan", description="Проверка файла на вирусы с помощью ClamAV")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    result = await scan_file_with_clamav(content, file.filename)
    if not result["clean"]:
        return {"clean": False, "detail": result["detail"]}
    return {"clean": True}
