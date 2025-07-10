import aiofiles
import subprocess
import os

async def scan_file_with_clamav(file: bytes, filename: str) -> dict:
    temp_path = f"/tmp/{filename}"
    async with aiofiles.open(temp_path, 'wb') as out_file:
        await out_file.write(file)
    try:
        result = subprocess.run(["clamscan", temp_path], capture_output=True, text=True)
        clean = result.returncode == 0
    finally:
        os.remove(temp_path)
    return {"clean": clean, "detail": result.stdout}
