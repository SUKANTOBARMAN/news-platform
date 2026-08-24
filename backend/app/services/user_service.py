"""
Module 2 — Identity & Access Management
জটিল বিজনেস লজিক (যা রাউট ফাইলে রাখা উচিত না) এখানে লিখবে।

STUB — এখানে এখনো কোনো ইমপ্লিমেন্টেশন লেখা হয়নি।

মনে রাখবে (ORM Maintenance Guide, Part ৯):
- Service ফাংশন নিজে কখনো SessionLocal() কল করে নতুন session বানাবে না
- route থেকে যে session (db: Session) পাস করা হয়েছে সেটাই ব্যবহার করবে,
  যাতে একই request-এর সব DB অপারেশন একই transaction-এর অংশ থাকে

উদাহরণ প্যাটার্ন:
    def do_something(db: Session, ...) -> None:
        ...
"""
from sqlalchemy.orm import Session  # noqa: F401

# TODO: এখানে User মডিউলের service ফাংশন লেখো
