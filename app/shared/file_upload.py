import os
import uuid

from fastapi import UploadFile

UPLOAD_FOLDER = "app/uploads/products"

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def save_product_image(
    file: UploadFile,
) -> str:

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Invalid image type."
        )

    filename = (
        f"{uuid.uuid4()}{extension}"
    )

    path = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(path, "wb") as buffer:
        buffer.write(
            file.file.read()
        )

    return f"products/{filename}"