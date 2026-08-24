"""
SQLAlchemy engine ও session তৈরি -- get_db() dependency এখান থেকেই আসে।
নিয়ম (দ্রষ্টব্য ORM Maintenance Guide): কোথাও রুটে সরাসরি SessionLocal() কল করা যাবে না,
সবসময় get_db() dependency দিয়েই session নিতে হবে।
"""
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# নোট: pool_size/max_overflow শুধু QueuePool-ভিত্তিক ডেটাবেজে (MySQL, PostgreSQL)
# কাজ করে -- SQLite (টেস্ট/CI-তে ব্যবহৃত) ডিফল্টভাবে SingletonThreadPool ব্যবহার করে,
# যেটা এই kwargs গ্রহণ করে না। তাই শুধু non-SQLite URL-এ এগুলো পাস করা হচ্ছে।
_engine_kwargs: dict = {"pool_pre_ping": True, "echo": settings.DEBUG}
if not settings.DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["pool_size"] = 10
    _engine_kwargs["max_overflow"] = 20

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()