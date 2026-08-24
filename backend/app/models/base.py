"""
সব মডেলের ভিত্তি। SQLAlchemy 2.0-স্টাইল DeclarativeBase ব্যবহার করা হয়েছে
(পুরনো declarative_base() না) -- IDE/mypy টাইপ-হিন্ট পুরোপুরি পায়।

দ্রষ্টব্য: Poribar Health ORM Maintenance Guide অনুসরণ করা হয়েছে --
- snake_case টেবিল নাম, বহুবচন
- Mapped[type] সব কলামে
- nullable= সবসময় explicit
- TimestampMixin দিয়ে created_at/updated_at DRY রাখা হয়েছে
"""
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """created_at / updated_at -- যেসব মডেলে দুটোই দরকার সেগুলো এটা ইনহেরিট করবে।"""

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
