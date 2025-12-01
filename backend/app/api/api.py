from fastapi import APIRouter
from .v1 import terrestre, maritimo

api_router = APIRouter()

api_router.include_router(terrestre.router) 
api_router.include_router(maritimo.router) 