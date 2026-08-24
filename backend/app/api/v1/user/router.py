"""
USER role router — লগইন করা সাবস্ক্রাইবার/পাঠকের নিজের ডেটা নিয়ে কাজ (Subscriber)
এই ফোল্ডারের সব endpoint ফাইলকে একত্রিত করে api/v1/router.py-তে mount হয়।
"""
from fastapi import APIRouter

from app.api.v1.user import profile
from app.api.v1.user import engagement
from app.api.v1.user import billing
from app.api.v1.user import notifications

api_router = APIRouter()

api_router.include_router(profile.router, prefix="/profile", tags=["User - Profile"])
api_router.include_router(engagement.router, prefix="/engagement", tags=["User - Engagement"])
api_router.include_router(billing.router, prefix="/billing", tags=["User - Billing"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["User - Notifications"])
