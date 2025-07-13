import aiofiles
import subprocess
import os
import sys

async def scan_file_with_clamav(file: bytes, filename: str) -> dict:
    temp_path = f"/tmp/{filename}"
    async with aiofiles.open(temp_path, 'wb') as out_file:
        await out_file.write(file)
    try:
        result = subprocess.run(["clamscan", temp_path], capture_output=True, text=True)
        print(f"[virus-scan-service] clamscan output: {result.stdout}", file=sys.stderr)
        print(f"[virus-scan-service] clamscan returncode: {result.returncode}", file=sys.stderr)
        clean = result.returncode == 0
        print(f"[virus-scan-service] Returning clean={{clean}}, detail={{result.stdout}}", file=sys.stderr)
    finally:
        try:
            os.remove(temp_path)
        except FileNotFoundError:
            print(f"[virus-scan-service] Temp file already removed: {temp_path}", file=sys.stderr)
    return {"clean": clean, "detail": result.stdout}
