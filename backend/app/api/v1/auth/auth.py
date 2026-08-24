"""
Module 2 — Identity & Access Management (auth অংশ, সম্পূর্ণ)
Role: auth (অথেন্টিকেশন — রেজিস্ট্রেশন, লগইন, OTP, টোকেন)

দেখো System Design Section 12 (Sanctum-স্টাইল Auth Flow) — এই ফাইলের
লজিক সেই ফ্লো-এর Python/JWT-ভার্সন।
"""
import random
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import Otp, User
from app.schemas.user import (
    LoginIn,
    OtpRequestIn,
    OtpVerifyIn,
    TokenOut,
    UserCreate,
    UserOut,
)

router = APIRouter()


def _utcnow() -> datetime:
    """
    Naive UTC datetime রিটার্ন করে (timezone info ছাড়া) -- কারণ MySQL/SQLite-এ
    DATETIME কলাম naive হিসেবে স্টোর হয়। timezone-aware datetime ব্যবহার করলে
    DB থেকে ফেরত আসা naive datetime-এর সাথে তুলনা করতে গেলে
    "can't compare offset-naive and offset-aware datetimes" এরর আসে -- তাই পুরো
    অ্যাপে সবসময় এই হেল্পার দিয়ে naive UTC ব্যবহার করা হয়, ধারাবাহিকতা বজায় রাখতে।
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


OTP_EXPIRE_MINUTES = 10
OTP_MAX_ATTEMPTS = 5


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="এই ইমেইল দিয়ে ইতিমধ্যে অ্যাকাউন্ট আছে")

    user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    """
    ইমেইল + পাসওয়ার্ড দিয়ে লগইন — সফল হলে JWT access token রিটার্ন করে।

    নোট: rate limiting (Redis দিয়ে, "৫ বার ভুল দিলে ৫ মিনিট ব্লক" — দেখো
    System Design Section 12) এখনো ইমপ্লিমেন্ট করা হয়নি, brute-force
    প্রোটেকশনের জন্য এটা প্রোডাকশনে যাওয়ার আগে যোগ করা জরুরি।
    """
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ইমেইল বা পাসওয়ার্ড ভুল",
        )

    user.last_login_at = _utcnow()
    db.commit()

    access_token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=access_token)


@router.post("/otp/request", status_code=status.HTTP_204_NO_CONTENT)
def request_otp(payload: OtpRequestIn, db: Session = Depends(get_db)):
    """
    OTP জেনারেট করে (এই স্টাবে সরাসরি রেসপন্সে ফেরত দেওয়া হচ্ছে ডেভ-টেস্টিং সুবিধার
    জন্য -- প্রোডাকশনে এটা কখনো response-এ দেওয়া উচিত না, শুধু SMS/email queue-তে
    পাঠানো উচিত, দেখো services/notification_dispatch_service.py স্টাব)।
    """
    otp_code = f"{random.randint(0, 999999):06d}"

    otp = Otp(
        phone_or_email=payload.phone_or_email,
        otp_code_hash=hash_password(otp_code),
        purpose=payload.purpose,
        expires_at=_utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES),
        created_at=_utcnow(),
    )
    db.add(otp)
    db.commit()

    # TODO: প্রোডাকশনে এখানে print()-এর বদলে SMS/email পাঠানোর সার্ভিস কল করো
    print(f"[DEV ONLY] OTP for {payload.phone_or_email} ({payload.purpose}): {otp_code}")


@router.post("/otp/verify", response_model=TokenOut)
def verify_otp(payload: OtpVerifyIn, db: Session = Depends(get_db)):
    otp = db.scalar(
        select(Otp)
        .where(
            Otp.phone_or_email == payload.phone_or_email,
            Otp.purpose == payload.purpose,
            Otp.is_verified == False,  # noqa: E712
        )
        .order_by(Otp.id.desc())
    )
    if not otp:
        raise HTTPException(status_code=400, detail="কোনো বৈধ OTP পাওয়া যায়নি")
    if otp.expires_at < _utcnow():
        raise HTTPException(status_code=400, detail="OTP-এর মেয়াদ শেষ হয়ে গেছে")
    if otp.attempts >= OTP_MAX_ATTEMPTS:
        raise HTTPException(status_code=429, detail="সর্বোচ্চ চেষ্টার সীমা পার হয়ে গেছে")
    if not verify_password(payload.otp_code, otp.otp_code_hash):
        otp.attempts += 1
        db.commit()
        raise HTTPException(status_code=400, detail="ভুল OTP")

    otp.is_verified = True
    db.commit()

    # login purpose হলে সরাসরি টোকেন দিয়ে দাও (phone দিয়ে ইউজার খুঁজে)
    user = db.scalar(select(User).where(User.phone == payload.phone_or_email))
    if not user:
        raise HTTPException(status_code=404, detail="এই নাম্বারে কোনো অ্যাকাউন্ট পাওয়া যায়নি")

    access_token = create_access_token(subject=str(user.id))
    return TokenOut(access_token=access_token)