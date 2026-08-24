"""
Module 2 — Identity & Access Management (profile অংশ, সম্পূর্ণ)
Role: user (লগইন করা সাবস্ক্রাইবার/পাঠকের নিজের ডেটা নিয়ে কাজ)
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User, UserDevice
from app.schemas.user import UserDeviceCreate, UserDeviceOut, UserOut

router = APIRouter()


def _utcnow() -> datetime:
    """Naive UTC datetime -- দেখো auth.py-এর একই নামের হেল্পারের কমেন্ট।"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    get_current_user() টোকেন থেকে ইউজার বের করে -- তাই কেউ অন্য কারো id দিয়ে
    প্রোফাইল দেখতে পারবে না (আগের ভার্সনে যে authorization সমস্যা ছিল সেটা এখন ঠিক)।
    """
    return current_user


@router.get("/devices", response_model=list[UserDeviceOut])
def list_my_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return list(
        db.scalars(select(UserDevice).where(UserDevice.user_id == current_user.id))
    )


@router.post("/devices", response_model=UserDeviceOut, status_code=201)
def register_device(
    payload: UserDeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(UserDevice).where(
            UserDevice.user_id == current_user.id,
            UserDevice.device_fingerprint == payload.device_fingerprint,
        )
    )
    if existing:
        existing.fcm_token = payload.fcm_token
        existing.last_active_at = _utcnow()
        db.commit()
        db.refresh(existing)
        return existing

    device = UserDevice(
        user_id=current_user.id,
        device_fingerprint=payload.device_fingerprint,
        platform=payload.platform,
        fcm_token=payload.fcm_token,
        last_active_at=_utcnow(),
    )
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


# TODO: update profile (PATCH /me), preferred_locale বদলানো, device delete ইত্যাদি