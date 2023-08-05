"""
user api endpoints
"""

from fastapi import APIRouter, Request

from ..core.user import User, get_user as core_get_user

router = APIRouter()


@router.get(
    "/", response_model=User, tags=["user"], summary="User Api", operation_id="get_user"
)
async def get_user(request: Request) -> User:
    """
    user api endpoint
    """
    return core_get_user(request.app.spotlight_license)
