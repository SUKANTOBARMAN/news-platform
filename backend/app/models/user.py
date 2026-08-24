"""
Module 2 — Identity & Access Management (সম্পূর্ণ)
টেবিল তালিকা (পূর্ণ বিবরণের জন্য docs/project_documentation_redesigned.pdf, Module 2):
  users, user_devices, otps, roles, permissions,
  user_roles (মূল ব্লুপ্রিন্টে model_has_roles নামে ছিল), role_permissions

নোট — সরলীকরণ: মূল ব্লুপ্রিন্টে model_has_roles পলিমরফিক ছিল (model_type, model_id)
যাতে ভবিষ্যতে User ছাড়া অন্য মডেলও role পেতে পারে। এই পোর্টে আপাতত শুধু User-ই
role পাবে, তাই সরাসরি user_id FK দিয়ে সহজ many-to-many রাখা হয়েছে (user_roles)।
যদি ভবিষ্যতে polymorphic দরকার হয়, তখন এটাকে পলিমরফিক টেবিলে রূপান্তর করা যাবে।
"""
from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

# ── user_roles: many-to-many pivot (User <-> Role) ──
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

# ── role_permissions: many-to-many pivot (Role <-> Permission) ──
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str | None] = mapped_column(String(191), unique=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_journalist: Mapped[bool] = mapped_column(default=False)
    preferred_locale: Mapped[str] = mapped_column(String(10), default="bn")
    last_login_at: Mapped[datetime | None] = mapped_column(nullable=True)

    devices: Mapped[list["UserDevice"]] = relationship(back_populates="user")
    roles: Mapped[list["Role"]] = relationship(secondary=user_roles, back_populates="users")

    def has_permission(self, permission_name: str) -> bool:
        """
        উদাহরণ: user.has_permission("articles.publish")
        নিয়ম (ORM Guide অনুযায়ী): permission নাম resource.action প্যাটার্নে।
        """
        for role in self.roles:
            for perm in role.permissions:
                if perm.name == permission_name:
                    return True
        return False


class UserDevice(Base, TimestampMixin):
    """পুশ নোটিফিকেশন ও সেশন ট্র্যাকিং-এর জন্য রেজিস্টার্ড ডিভাইস।"""

    __tablename__ = "user_devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    device_fingerprint: Mapped[str] = mapped_column(String(64), index=True)
    platform: Mapped[str] = mapped_column(String(20))  # ios, android, web, desktop
    fcm_token: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_notifications_enabled: Mapped[bool] = mapped_column(default=True)
    last_active_at: Mapped[datetime | None] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="devices")


class Otp(Base):
    """
    লগইন, ভেরিফিকেশন, পাসওয়ার্ড রিসেটের জন্য এক-বার-ব্যবহারযোগ্য কোড।
    শুধু created_at দরকার (updated_at না) -- তাই TimestampMixin ইনহেরিট করা হয়নি,
    দরকারি কলাম নিজে লেখা হয়েছে (ORM Guide, Part ২ — শুধু প্রয়োজনীয় কলাম রাখা)।
    """

    __tablename__ = "otps"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_or_email: Mapped[str] = mapped_column(String(191), index=True)
    otp_code_hash: Mapped[str] = mapped_column(String(255))  # হ্যাশ করে রাখা হয়, plain না
    purpose: Mapped[str] = mapped_column(String(30))  # login, email_verify, phone_verify, password_reset
    expires_at: Mapped[datetime] = mapped_column()
    is_verified: Mapped[bool] = mapped_column(default=False)
    attempts: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column()


class Role(Base, TimestampMixin):
    """super_admin, editor_in_chief, section_editor, reporter, subscriber ইত্যাদি।"""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    users: Mapped[list["User"]] = relationship(secondary=user_roles, back_populates="roles")
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permissions, back_populates="roles"
    )


class Permission(Base, TimestampMixin):
    """গ্র্যানুলার একশন — articles.publish, comments.moderate, ads.manage ইত্যাদি (resource.action)।"""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)

    roles: Mapped[list["Role"]] = relationship(
        secondary=role_permissions, back_populates="permissions"
    )