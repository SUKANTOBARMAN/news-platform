"""
Alembic env.py এই ফাইল থেকে Base.metadata ইম্পোর্ট করে autogenerate করার জন্য।
app/models/__init__.py-এ প্রতিটা মডেল ইম্পোর্ট করা থাকতে হবে, নাহলে migration নতুন
টেবিল "দেখতে" পাবে না (দ্রষ্টব্য ORM Maintenance Guide, Part ১১)।
"""
from app.models import Base  # noqa: F401  (re-exported for Alembic)
from app.models import *  # noqa: F401,F403  (ensures every model is registered on Base.metadata)
