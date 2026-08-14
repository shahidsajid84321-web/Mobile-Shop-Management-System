from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from app.core.constants.permissions import PermissionCode
from app.modules.permissions.permission_dependencies import require_permission
from app.shared.file_upload import (
    save_product_image,
)


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post("/product-image")
def upload_product_image(
    file: UploadFile = File(...),
    current_user=Depends(
        require_permission(PermissionCode.PRODUCTS_UPDATE)
    ),
):
    try:
        image = save_product_image(file)
    except ValueError as exc:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    return {
        "message": "Image uploaded successfully.",
        "image": image,
    }
