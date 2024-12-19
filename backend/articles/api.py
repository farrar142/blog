from ninja import Router

from authentications.bearers import JwtBearer
from backend.requests import AuthenticatedRequest


router = Router(tags=["articles"])


@router.post("/", auth=JwtBearer())
def post(request: AuthenticatedRequest):
    pass
