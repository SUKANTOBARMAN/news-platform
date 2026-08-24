"""
Module 2 — Identity & Access Management schema (সম্পূর্ণ)
নিয়ম: response schema-তে model_config = {"from_attributes": True} বাধ্যতামূলক,
নাহলে route থেকে SQLAlchemy object সরাসরি রিটার্ন করলে serialize করতে পারবে না।
"""
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ── User ──
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = None
    phone: str | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class RoleOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str


class UserOut(UserBase):
    model_config = {"from_attributes": True}

    id: int
    is_journalist: bool
    preferred_locale: str
    created_at: datetime
    roles: list[RoleOut] = []


# ── Auth (login/token) ──
class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── OTP ──
class OtpRequestIn(BaseModel):
    phone_or_email: str
    purpose: str = "login"  # login, email_verify, phone_verify, password_reset


class OtpVerifyIn(BaseModel):
    phone_or_email: str
    otp_code: str
    purpose: str = "login"


# ── User Device ──
class UserDeviceCreate(BaseModel):
    device_fingerprint: str
    platform: str  # ios, android, web, desktop
    fcm_token: str | None = None


class UserDeviceOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    platform: str
    device_fingerprint: str
    is_notifications_enabled: bool
    last_active_at: datetime | None = None


# ── Role & Permission (admin) ──
class PermissionOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str


class RoleCreate(BaseModel):
    name: str


class RoleDetailOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    permissions: list[PermissionOut] = []


class AssignRoleIn(BaseModel):
    role_id: int