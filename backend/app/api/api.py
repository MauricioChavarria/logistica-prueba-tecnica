from fastapi import APIRouter
from .v1 import terrestre, maritimo

api_router = APIRouter(prefix="/v1")

api_router.include_router(terrestre.router) 
api_router.include_router(maritimo.router) 