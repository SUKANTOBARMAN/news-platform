"""
V1 API — top-level router। প্রতিটা role-এর নিজস্ব router (role folder-এর
router.py) এখানে একটা prefix দিয়ে mount হয়। role-এর ভেতরের ফাইলগুলো (যেমন
public/articles.py) নিজেদের সাব-প্রিফিক্স ব্যবহার করে, তাই চূড়ান্ত path হয়:

    /api/v1/{role}/{resource}/...
    উদাহরণ: /api/v1/public/articles/  ,  /api/v1/user/billing/checkout

ব্যতিক্রম: /api/v1/auth/... (role নিজেই একটা resource, তাই ভেতরে আলাদা প্রিফিক্স নেই)
"""
from fastapi import APIRouter

from app.api.v1 import health
from app.api.v1.admin.router import api_router as admin_router
from app.api.v1.auth.router import api_router as auth_router
from app.api.v1.editorial.router import api_router as editorial_router
from app.api.v1.public.router import api_router as public_router
from app.api.v1.user.router import api_router as user_router

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(public_router, prefix="/public", tags=["Public"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(editorial_router, prefix="/editorial", tags=["Editorial"])
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
