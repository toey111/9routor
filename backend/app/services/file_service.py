import os
import uuid
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_DOC_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx"}
ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/webp",
    "application/pdf", "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
}

def validate_and_save_file(file: UploadFile, subfolder: str = "avatars") -> str:
    # 1. Check extension
    filename = file.filename or "unknown"
    ext = os.path.splitext(filename)[1].lower()
    
    if subfolder == "avatars" and ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"อนุญาตเฉพาะไฟล์รูปภาพ ({', '.join(ALLOWED_IMAGE_EXTENSIONS)}) เท่านั้น"
        )
    elif subfolder == "docs" and ext not in ALLOWED_DOC_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"อนุญาตเฉพาะไฟล์เอกสาร ({', '.join(ALLOWED_DOC_EXTENSIONS)}) เท่านั้น"
        )

    # 2. Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ประเภทไฟล์ไม่ถูกต้องหรือไม่ปลอดภัย"
        )

    # 3. Create destination directory if not exists
    dest_dir = os.path.join(settings.UPLOAD_DIR, subfolder)
    os.makedirs(dest_dir, exist_ok=True)

    # 4. Generate unique secure filename
    unique_name = f"{uuid.uuid4().hex}{ext}"
    target_path = os.path.join(dest_dir, unique_name)

    # 5. Read and write with size limit
    size = 0
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    with open(target_path, "wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                os.remove(target_path)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"ขนาดไฟล์เกินกำหนด (สูงสุด {settings.MAX_FILE_SIZE_MB}MB)"
                )
            buffer.write(chunk)

    return f"/uploads/{subfolder}/{unique_name}"
