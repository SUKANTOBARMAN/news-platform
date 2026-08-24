"""
Module 2 — Identity & Access Management (অ্যাডমিন অংশ, সম্পূর্ণ)
Role: admin (সিস্টেম অ্যাডমিনিস্ট্রেশন — Super Admin)

নোট: এই এন্ডপয়েন্টগুলো এখনো require_permission() দিয়ে সুরক্ষিত না —
require_permission("users.manage") এখানে Depends()-এ যোগ করে দেওয়া উচিত
production-এ যাওয়ার আগে (দেখো app/api/deps.py-এর require_permission)।

সতর্কতা — route অর্ডার গুরুত্বপূর্ণ: /roles/ ও /permissions/ (static path)
অবশ্যই /{user_id} (dynamic path)-এর *আগে* ডিফাইন করতে হবে, নাহলে FastAPI
"/roles/" রিকোয়েস্টকে ভুলভাবে user_id="roles" হিসেবে ধরার চেষ্টা করবে।
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.user import Permission, Role, User
from app.schemas.user import (
    AssignRoleIn,
    PermissionOut,
    RoleCreate,
    RoleDetailOut,
    UserOut,
)

router = APIRouter()


# ── Roles & Permissions ম্যানেজমেন্ট (static path -- /{user_id}-এর আগে) ──


@router.get("/roles/", response_model=list[RoleDetailOut])
def list_roles(db: Session = Depends(get_db)):
    return list(db.scalars(select(Role)))


@router.post("/roles/", response_model=RoleDetailOut, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Role).where(Role.name == payload.name))
    if existing:
        raise HTTPException(status_code=400, detail="এই নামে রোল আগে থেকেই আছে")

    role = Role(name=payload.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.get("/permissions/", response_model=list[PermissionOut])
def list_permissions(db: Session = Depends(get_db)):
    return list(db.scalars(select(Permission)))


# ── User Listing ও Role Assignment (dynamic /{user_id} path) ──


@router.get("/", response_model=list[UserOut])
def list_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return list(db.scalars(select(User).offset(skip).limit(limit)))


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="ইউজার পাওয়া যায়নি")
    return user


@router.post("/{user_id}/roles", response_model=UserOut)
def assign_role(user_id: int, payload: AssignRoleIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="ইউজার পাওয়া যায়নি")

    role = db.scalar(select(Role).where(Role.id == payload.role_id))
    if not role:
        raise HTTPException(status_code=404, detail="রোল পাওয়া যায়নি")

    if role not in user.roles:
        user.roles.append(role)
        db.commit()
        db.refresh(user)
    return user


@router.delete("/{user_id}/roles/{role_id}", response_model=UserOut)
def remove_role(user_id: int, role_id: int, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="ইউজার পাওয়া যায়নি")

    user.roles = [r for r in user.roles if r.id != role_id]
    db.commit()
    db.refresh(user)
    return user