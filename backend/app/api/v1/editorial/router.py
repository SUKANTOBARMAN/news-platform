"""
EDITORIAL role router — সাংবাদিক/এডিটরদের CMS (Reporter, Section Editor, Editor-in-Chief)
এই ফোল্ডারের সব endpoint ফাইলকে একত্রিত করে api/v1/router.py-তে mount হয়।
"""
from fastapi import APIRouter

from app.api.v1.editorial import articles
from app.api.v1.editorial import media
from app.api.v1.editorial import newsroom
from app.api.v1.editorial import integrity

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["Editorial - Articles"])
api_router.include_router(media.router, prefix="/media", tags=["Editorial - Media"])
api_router.include_router(newsroom.router, prefix="/newsroom", tags=["Editorial - Newsroom"])
api_router.include_router(integrity.router, prefix="/integrity", tags=["Editorial - Integrity"])
