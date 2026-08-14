from typing import Any

from app.shared.common_schema import ApiResponse


def success_response(
    message: str,
    data: Any = None,
) -> ApiResponse:
    return ApiResponse(
        success=True,
        message=message,
        data=data,
    )
