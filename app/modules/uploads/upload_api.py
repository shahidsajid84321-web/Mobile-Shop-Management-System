from fastapi import APIRouter, File, UploadFile

from app.shared.file_upload import save_product_image

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("/product-image")
def upload_product_image(
    file: UploadFile = File(...),
):

    image = save_product_image(
        file,
    )

    return {
        "image": image,
    }
