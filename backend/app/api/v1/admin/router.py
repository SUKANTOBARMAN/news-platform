"""
ADMIN role router — সিস্টেম অ্যাডমিনিস্ট্রেশন (Super Admin, Ad Manager)
এই ফোল্ডারের সব endpoint ফাইলকে একত্রিত করে api/v1/router.py-তে mount হয়।
"""
from fastapi import APIRouter

from app.api.v1.admin import settings
from app.api.v1.admin import users
from app.api.v1.admin import ads
from app.api.v1.admin import marketing
from app.api.v1.admin import circulation
from app.api.v1.admin import compliance
from app.api.v1.admin import experiments
from app.api.v1.admin import revenue
from app.api.v1.admin import analytics

api_router = APIRouter()

api_router.include_router(settings.router, prefix="/settings", tags=["Admin - Settings"])
api_router.include_router(users.router, prefix="/users", tags=["Admin - Users"])
api_router.include_router(ads.router, prefix="/ads", tags=["Admin - Ads"])
api_router.include_router(marketing.router, prefix="/marketing", tags=["Admin - Marketing"])
api_router.include_router(circulation.router, prefix="/circulation", tags=["Admin - Circulation"])
api_router.include_router(compliance.router, prefix="/compliance", tags=["Admin - Compliance"])
api_router.include_router(experiments.router, prefix="/experiments", tags=["Admin - Experiments"])
api_router.include_router(revenue.router, prefix="/revenue", tags=["Admin - Revenue"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Admin - Analytics"])
