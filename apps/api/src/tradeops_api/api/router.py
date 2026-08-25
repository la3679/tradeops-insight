"""Top-level API router composition."""

from fastapi import APIRouter

from tradeops_api.api.routes import meta

api_router = APIRouter()
api_router.include_router(meta.router, prefix="/meta")
