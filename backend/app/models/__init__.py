"""
Central export — app/models/__init__.py

নিয়ম (ORM Maintenance Guide, Part ১): প্রতিটা নতুন মডেল ফাইল বানানোর পর এখানে
অবশ্যই ইম্পোর্ট যোগ করতে হবে -- নাহলে Alembic autogenerate নতুন টেবিল "দেখতে" পাবে না।

module-by-module ইমপ্লিমেন্টেশনের সময় নিচের কমেন্ট করা লাইনগুলো আনকমেন্ট করবে,
যখন সেই মডিউলের models/*.py ফাইলে ক্লাস লেখা শেষ হবে। প্রতিটা stub ফাইল আগে
থেকেই তৈরি আছে (backend/app/models/ ফোল্ডারে দেখো) -- শুধু ক্লাস লিখে এখানে
ইম্পোর্ট আনকমেন্ট করলেই Alembic সেগুলো ধরবে।
"""
from app.models.base import Base, TimestampMixin
from app.models.user import User

# Module 2 (বাকি অংশ) — user.py-তেই UserDevice, Otp, Role, Permission যোগ করবে
# Module 3 — Settings, Page, Menu, MenuItem, Redirect
# from app.models.settings import Setting, Page, Menu, MenuItem, Redirect
# Module 4 — MediaAsset, MediaRendition, VideoTranscoding, Mediable, AiMetadata, ArticleEmbedding
# from app.models.media import MediaAsset, MediaRendition, VideoTranscoding, Mediable, AiMetadata, ArticleEmbedding
# Module 5 — Category, Tag, Topic
# from app.models.taxonomy import Category, Tag, Topic
# Module 6 — Article, ArticleBlock, ArticleRevision, EditorialLock, ArticleTranslation, ContentEmbargo
# from app.models.article import Article, ArticleBlock, ArticleRevision, EditorialLock, ArticleTranslation, ContentEmbargo
# Module 7 — ArticleCategory, ArticleTag, ArticleTopic, ArticleAuthor, ArticleRelated
# from app.models.article_pivot import ArticleCategory, ArticleTag, ArticleTopic, ArticleAuthor, ArticleRelated
# Module 8 — Plan, PaywallRule, UserEntitlement, Subscription, SubscriptionEvent, Transaction, InstitutionalAccount, ...
# from app.models.billing import Plan, PaywallRule, UserEntitlement, Subscription, SubscriptionEvent, Transaction
# Module 9 — Comment, CommentReaction, ArticleReaction, Bookmark, Following, Puzzle, UserPuzzleSession
# from app.models.engagement import Comment, CommentReaction, ArticleReaction, Bookmark, Following, Puzzle, UserPuzzleSession
# Module 10 — ReadHistory, BehavioralMetric, UserPreference, UserRecommendationProfile, ChurnLog, ...
# from app.models.analytics import ReadHistory, BehavioralMetric, UserPreference, UserRecommendationProfile
# Module 11 — LiveEvent, LiveUpdate, Podcast, PodcastEpisode, AudioArticle
# from app.models.multimedia import LiveEvent, LiveUpdate, Podcast, PodcastEpisode, AudioArticle
# Module 12 — Notification, NotificationLog, Newsletter, Subscriber, PushNotification, Poll, ...
# from app.models.marketing import Notification, NotificationLog, Newsletter, Subscriber, PushNotification, Poll
# Module 13 — AdZone, AdCampaign, AdAnalytics, Product, ArticleProduct, ClassifiedCategory, ClassifiedAd
# from app.models.ads import AdZone, AdCampaign, AdAnalytics, Product, ArticleProduct, ClassifiedCategory, ClassifiedAd
# Module 14 — Epaper, PrintEdition, Agency, Hawker, FreelancerContract, FreelancerInvoice, InvoiceItem, ...
# from app.models.circulation import Epaper, PrintEdition, Agency, Hawker, FreelancerContract, FreelancerInvoice
# Module 15 — FactCheck, ArticleCorrection, WireSource, WireIngestion, SocialAccount, Event, TicketTier, ...
# from app.models.integrity import FactCheck, ArticleCorrection, WireSource, WireIngestion, SocialAccount, Event
# Module 16 — UserConsent, DataDeletionRequest, SeoMetadata, ActivityLog, SupportTicket, Webhook, SecureTip, ...
# from app.models.compliance import UserConsent, DataDeletionRequest, SeoMetadata, ActivityLog, SupportTicket
# Module 17 — AbExperiment, AbExperimentAssignment, FeatureFlag
# from app.models.experiments import AbExperiment, AbExperimentAssignment, FeatureFlag
# Module 18 — EditorialDesk, StoryPitch, EditorialAssignment
# from app.models.newsroom import EditorialDesk, StoryPitch, EditorialAssignment
# Module 19 — RevenueAttribution, ContentPerformanceSnapshot
# from app.models.revenue import RevenueAttribution, ContentPerformanceSnapshot

__all__ = ["Base", "TimestampMixin", "User"]

