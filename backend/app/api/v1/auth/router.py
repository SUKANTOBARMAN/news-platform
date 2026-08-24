"""
AUTH role router — অথেন্টিকেশন — রেজিস্ট্রেশন, লগইন, টোকেন
এই ফোল্ডারের সব endpoint ফাইলকে একত্রিত করে api/v1/router.py-তে mount হয়।

নোট: top-level router.py-তেই এই পুরো role router "/auth" প্রিফিক্স দিয়ে
mount হয় (দেখো api/v1/router.py) -- তাই এখানে আবার "/auth" prefix দেওয়া হয়নি
(নাহলে path হয়ে যেত /api/v1/auth/auth/register, যা রিডান্ডেন্ট)।
"""
from fastapi import APIRouter

from app.api.v1.auth import auth

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"])

