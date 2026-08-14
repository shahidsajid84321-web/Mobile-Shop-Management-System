import os
import uuid
from pathlib import Path

from fastapi import UploadFile


UPLOAD_FOLDER = Path(__file__).resolve().parents[1] / "uploads" / "products"

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def save_product_image(
    file: UploadFile,
) -> str:

    if not file.filename:
        raise ValueError("No file selected.")

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Invalid image type. "
            "Allowed types: jpg, jpeg, png, webp."
        )

    expected_content_types = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".png": "image/png", ".webp": "image/webp",
    }
    if file.content_type != expected_content_types[extension]:
        raise ValueError("File content type does not match its image extension.")

    file_content = file.file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError(
            "Image size must not exceed 5 MB."
        )

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4()}{extension}"

    path = UPLOAD_FOLDER / filename

    with open(path, "wb") as buffer:
        buffer.write(file_content)

    return f"products/{filename}"
