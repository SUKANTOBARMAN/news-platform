"""
Module 12 — Marketing, Notifications & Interactive
SQLAlchemy মডেল এখানে লিখবে (Base, TimestampMixin ইনহেরিট করে)।

STUB — এখানে এখনো কোনো ইমপ্লিমেন্টেশন লেখা হয়নি।


এই মডিউলের টেবিলসমূহ (পূর্ণ কলাম-বিবরণের জন্য দেখো docs/project_documentation_redesigned.pdf, Module 12):
#   - notifications
#   - notification_logs
#   - newsletters
#   - subscribers
#   - newsletter_subscriber
#   - push_notifications
#   - polls
#   - poll_options
#   - poll_votes
#   - interactive_widgets

মনে রাখবে (ORM Maintenance Guide অনুযায়ী):
- প্রতিটা ক্লাস Base, TimestampMixin ইনহেরিট করবে (প্রয়োজন অনুযায়ী)
- snake_case টেবিল নাম, বহুবচন (__tablename__ = "...")
- Mapped[type] প্রতিটা কলামে, nullable= এক্সপ্লিসিট
- নতুন মডেল লেখার পর app/models/__init__.py-এ ইম্পোর্ট যোগ করতে ভুলো না
  (নাহলে Alembic autogenerate নতুন টেবিল দেখবে না)
"""
from app.models.base import Base, TimestampMixin  # noqa: F401

# TODO: এখানে Marketing মডিউলের ক্লাস লেখো
