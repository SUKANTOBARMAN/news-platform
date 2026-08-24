# News Platform — প্রজেক্ট স্ক্যাফোল্ড

Backend: **Python + FastAPI + SQLAlchemy 2.0 + Alembic + MySQL 8 + Redis**
Frontend: **React + TypeScript + Vite**
Infra: **Docker + Docker Compose + GitHub Actions CI/CD**

এই রিপোজিটরি একটা স্টার্টিং স্ক্যাফোল্ড — পুরো ১৯-মডিউল ডেটাবেজ ব্লুপ্রিন্ট এখানে
ইমপ্লিমেন্ট করা নেই, শুধু **role-based ফোল্ডার স্ট্রাকচার** (Poribar Health
প্রজেক্টের কনভেনশন অনুসরণ করে) ও একটা কার্যকরী উদাহরণ (Module 2 — register +
profile) রাখা হয়েছে, যাতে বাকি মডিউলগুলো একই প্যাটার্নে যোগ করা যায়।

## আর্কিটেকচার সিদ্ধান্ত — Role-based API ও Pages, Domain-based Models

- **`api/v1/` (backend) ও `pages/` (frontend)** — **role অনুযায়ী** ফোল্ডারে ভাগ করা:
  `public` (Guest), `auth`, `user` (Subscriber), `editorial` (Reporter/Editor),
  `admin` (Super Admin)। কারণ: কে অ্যাক্সেস করছে তার উপর ভিত্তি করে
  authorization/middleware আলাদা হয়, তাই route-লেয়ার role-ভিত্তিক হওয়া স্বাভাবিক।
- **`models/`, `schemas/`, `services/` (backend) ও `api/`, `types/`, `hooks/`
  (frontend)** — **ডোমেইন/মডিউল অনুযায়ী** ফ্ল্যাট ফাইল (article.py, billing.py...)।
  কারণ: ডেটার আকার (schema) কে জিজ্ঞেস করছে তার উপর নির্ভর করে না, শুধু কী ডেটা
  তার উপর নির্ভর করে — তাই এগুলো domain-ভিত্তিক রাখা হয়েছে (ORM Maintenance Guide-এর
  কনভেনশন অনুযায়ী)।

## ফোল্ডার স্ট্রাকচার

```
news-platform/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/                    # config.py, security.py
│   │   ├── db/                      # session.py (get_db), base.py (Alembic-এর জন্য)
│   │   ├── models/                  # SQLAlchemy মডেল — ডোমেইন-ভিত্তিক ফ্ল্যাট ফাইল
│   │   │   ├── base.py              # Base, TimestampMixin
│   │   │   ├── user.py              # Module 2 (কার্যকরী উদাহরণ)
│   │   │   ├── article.py           # Module 6
│   │   │   ├── billing.py           # Module 8
│   │   │   └── ... (মোট ১৯টা মডিউলের জন্য ফাইল)
│   │   ├── schemas/                 # Pydantic schema — models/-এর সাথে ১:১ মিল
│   │   ├── api/v1/                  # রাউট — role-ভিত্তিক সাব-ফোল্ডার
│   │   │   ├── router.py            # সব role router mount করে
│   │   │   ├── health.py
│   │   │   ├── public/              # Guest অ্যাক্সেস (articles, taxonomy, search...)
│   │   │   │   ├── router.py
│   │   │   │   └── articles.py, taxonomy.py, search.py, ...
│   │   │   ├── auth/                # register, login, OTP, token
│   │   │   │   ├── router.py
│   │   │   │   └── auth.py
│   │   │   ├── user/                # Subscriber নিজের ডেটা (profile, billing, engagement...)
│   │   │   │   ├── router.py
│   │   │   │   └── profile.py, billing.py, engagement.py, notifications.py
│   │   │   ├── editorial/           # Reporter/Editor CMS (articles CRUD, media, newsroom...)
│   │   │   │   ├── router.py
│   │   │   │   └── articles.py, media.py, newsroom.py, integrity.py
│   │   │   └── admin/               # Super Admin (settings, users, ads, compliance...)
│   │   │       ├── router.py
│   │   │       └── settings.py, users.py, ads.py, revenue.py, ...
│   │   └── services/                # বিজনেস লজিক — ডোমেইন-ভিত্তিক + cross-cutting
│   │       ├── article_service.py, billing_service.py, ...
│   │       └── cache_service.py, search_service.py, paywall_service.py, ...
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt / requirements-dev.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   └── src/
│       ├── main.tsx / App.tsx
│       ├── index.css
│       ├── layouts/                 # AppLayout.tsx (header/footer/nav shell)
│       ├── lib/                     # utils.ts (হেল্পার ফাংশন)
│       ├── routes/                  # index.tsx (কেন্দ্রীয় route config)
│       ├── api/                     # axios কল — ডোমেইন-ভিত্তিক ফ্ল্যাট ফাইল
│       ├── types/                   # TypeScript ইন্টারফেস — backend schema-র সাথে মিল
│       ├── hooks/                   # react-query hooks — ডোমেইন-ভিত্তিক
│       ├── components/
│       │   └── common/              # Loading.tsx ইত্যাদি শেয়ার্ড কম্পোনেন্ট
│       └── pages/                   # role-ভিত্তিক সাব-ফোল্ডার
│           ├── Home.tsx, NotFound.tsx    # role-নিরপেক্ষ ফ্ল্যাট পেজ
│           ├── public/              # Login, Register, ArticleDetail, CategoryPage...
│           ├── user/                # Profile, Bookmarks, SubscriptionPlans, Checkout
│           ├── editorial/           # EditorialDashboard
│           └── admin/               # AdminDashboard
│
├── .github/workflows/               # backend-ci, frontend-ci, docker-build, deploy
├── docker-compose.yml                # লোকাল ডেভেলপমেন্ট (hot-reload)
├── docker-compose.prod.yml           # প্রোডাকশন
└── docs/                             # আগের প্রজেক্ট নোটগুলো (PDF) রেফারেন্সের জন্য
```

## দ্রুত শুরু করা (লোকাল ডেভেলপমেন্ট)

```bash
# ১. এনভায়রনমেন্ট ফাইল কপি করো
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# ২. .env-এ SECRET_KEY বদলে একটা র‍্যান্ডম স্ট্রিং দাও

# ৩. সব সার্ভিস চালু করো (db, redis, backend, frontend)
docker compose up --build

# ব্যাকএন্ড: http://localhost:8001/api/v1/docs  (Swagger UI)
# ফ্রন্টএন্ড: http://localhost:5173
```

## প্রথম মাইগ্রেশন চালানো

```bash
docker compose exec backend alembic revision --autogenerate -m "create users table"
docker compose exec backend alembic upgrade head
```

## টেস্ট চালানো

```bash
# Backend (register/profile-এর কার্যকরী উদাহরণ টেস্ট আগে থেকেই আছে)
docker compose exec backend pytest

# Frontend
docker compose exec frontend npm run lint
```

## API path প্যাটার্ন

```
/api/v1/health
/api/v1/auth/register          (role: auth — role নিজেই resource, তাই সাব-প্রিফিক্স নেই)
/api/v1/public/articles/...    (role: public → resource: articles)
/api/v1/user/profile/{id}      (role: user → resource: profile)
/api/v1/editorial/articles/... (role: editorial → resource: articles — public-এর articles থেকে আলাদা ফাইল, কারণ ভিন্ন পারমিশন)
/api/v1/admin/settings/...     (role: admin → resource: settings)
```

লক্ষণীয়: `public/articles.py` ও `editorial/articles.py` — দুটো আলাদা ফাইল, একই
`articles` টেবিল নিয়ে কাজ করলেও ভিন্ন ভিন্ন পারমিশন/লজিক (public শুধু পড়ে,
editorial তৈরি/এডিট করে) — তাই route-লেয়ারে আলাদা রাখা হয়েছে, কিন্তু
`models/article.py` একটাই (ডেটা একই)।

## Module-by-Module ইমপ্লিমেন্টেশন চেকলিস্ট

প্রতিটা নতুন মডিউল যোগ করার সময়:

1. **Backend**
   - `app/models/<domain>.py` — SQLAlchemy মডেল লেখো (Base, TimestampMixin ইনহেরিট করে)
   - `app/models/__init__.py`-এ ইম্পোর্ট আনকমেন্ট/যোগ করো (নাহলে Alembic দেখবে না)
   - `app/schemas/<domain>.py` — Pydantic schema
   - `app/api/v1/<role>/<domain>.py`-তে রাউট লেখো (কোন role, তা উপরের ম্যাপিং টেবিল দেখো)
   - `app/api/v1/<role>/router.py`-তে সেই ফাইলের router include করো
   - প্রয়োজনে `app/services/<domain>_service.py` — জটিল বিজনেস লজিক
   - `alembic revision --autogenerate` → রিভিউ করো → `alembic upgrade head`
   - `tests/test_<domain>.py`

2. **Frontend**
   - `src/types/<domain>.ts` — TypeScript টাইপ (backend schema-র সাথে মেলানো)
   - `src/api/<domain>.ts` — axios কল
   - `src/hooks/use<Domain>.ts` — react-query hook
   - `src/pages/<role>/<Page>.tsx` — UI
   - `src/routes/index.tsx`-এ route আনকমেন্ট/যোগ করো

## Module → File ম্যাপিং

| # | মডিউল | Backend models/schemas/services | Backend route (role/file) | Frontend |
|---|--------|-----------------------------------|------------------------------|-----------|
| 2 | Identity & Access Management | `models/user.py`\* · `schemas/user.py`\* · `services/user_service.py` | `auth/auth.py`\* (register) · `user/profile.py`\* (profile) · `admin/users.py` (ইউজার ম্যানেজমেন্ট) | `api/auth.ts`, `api/users.ts`\* · `types/auth.ts` · `hooks/useAuth.ts`, `useUser.ts`\* · `pages/public/Login.tsx`, `Register.tsx` · `pages/user/Profile.tsx` |
| 3 | Global UI, Pages & Settings | `models/settings.py` · `schemas/settings.py` | `admin/settings.py` | `api/settings.ts` · `types/settings.ts` · `hooks/useSettings.ts` |
| 4 | Digital Asset Management & AI | `models/media.py` · `schemas/media.py` · `services/media_service.py` | `editorial/media.py` | `api/media.ts` · `types/media.ts` · `hooks/useMedia.ts` |
| 5 | Taxonomy & Discovery | `models/taxonomy.py` · `schemas/taxonomy.py` | `public/taxonomy.py` | `api/taxonomy.ts` · `types/taxonomy.ts` · `hooks/useTaxonomy.ts` · `pages/public/CategoryPage.tsx` |
| 6 | Core Editorial Engine | `models/article.py` · `schemas/article.py` · `services/article_service.py` | `public/articles.py` (রিড) · `editorial/articles.py` (CRUD) | `api/articles.ts` · `types/articles.ts` · `hooks/useArticles.ts` · `pages/public/ArticleDetail.tsx`, `SearchResults.tsx` |
| 7 | Content Pivots | `models/article_pivot.py` · `schemas/article_pivot.py` | (editorial/articles.py-এর অংশ) | (articles.ts-এর অংশ) |
| 8 | Monetization, Paywall & B2B | `models/billing.py` · `schemas/billing.py` · `services/billing_service.py`, `paywall_service.py` | `user/billing.py` (subscribe/checkout) | `api/billing.ts` · `types/billing.ts` · `hooks/useBilling.ts` · `pages/user/SubscriptionPlans.tsx`, `Checkout.tsx` |
| 9 | Reader Engagement & Gamification | `models/engagement.py` · `schemas/engagement.py` · `services/engagement_service.py` | `user/engagement.py` | `api/engagement.ts` · `types/engagement.ts` · `hooks/useEngagement.ts` · `pages/user/Bookmarks.tsx` |
| 10 | Behavioral Analytics & Retention | `models/analytics.py` · `schemas/analytics.py` · `services/analytics_service.py`, `recommendation_service.py`, `trending_service.py` | `admin/analytics.py` | `api/analytics.ts` · `types/analytics.ts` · `hooks/useAnalytics.ts` |
| 11 | Multimedia & Live News | `models/multimedia.py` · `schemas/multimedia.py` · `services/multimedia_service.py` | `public/multimedia.py` | `api/multimedia.ts` · `types/multimedia.ts` · `hooks/useMultimedia.ts` · `pages/public/PodcastDetail.tsx`, `LiveEventPage.tsx` |
| 12 | Marketing, Notifications & Interactive | `models/marketing.py` · `schemas/marketing.py` · `services/marketing_service.py`, `notification_dispatch_service.py` | `user/notifications.py` (নিজের) · `admin/marketing.py` (ক্যাম্পেইন) | `api/marketing.ts` · `types/marketing.ts` · `hooks/useMarketing.ts` |
| 13 | Ads, Commerce & Classifieds | `models/ads.py` · `schemas/ads.py` · `services/ads_service.py` | `public/classifieds.py` (ব্রাউজ) · `admin/ads.py` (ক্যাম্পেইন) | `api/ads.ts` · `types/ads.ts` · `hooks/useAds.ts` |
| 14 | Offline Circulation & Freelancers | `models/circulation.py` · `schemas/circulation.py` · `services/circulation_service.py` | `admin/circulation.py` | `api/circulation.ts` · `types/circulation.ts` · `hooks/useCirculation.ts` |
| 15 | Integrity, Syndication & Events | `models/integrity.py` · `schemas/integrity.py` · `services/integrity_service.py` | `editorial/integrity.py` (fact-check/correction) · `public/events.py` (ইভেন্ট ব্রাউজ) | `api/integrity.ts` · `types/integrity.ts` · `hooks/useIntegrity.ts` |
| 16 | Compliance, Logs & Mobile App | `models/compliance.py` · `schemas/compliance.py` · `services/compliance_service.py` | `admin/compliance.py` | `api/compliance.ts` · `types/compliance.ts` · `hooks/useCompliance.ts` · `pages/admin/AdminDashboard.tsx` |
| 17 | A/B Testing & Feature Flags | `models/experiments.py` · `schemas/experiments.py` · `services/experiments_service.py` | `admin/experiments.py` | `api/experiments.ts` · `types/experiments.ts` · `hooks/useExperiments.ts` |
| 18 | Editorial Workflow (Newsroom CMS) | `models/newsroom.py` · `schemas/newsroom.py` · `services/newsroom_service.py` | `editorial/newsroom.py` | `api/newsroom.ts` · `types/newsroom.ts` · `hooks/useNewsroom.ts` · `pages/editorial/EditorialDashboard.tsx` |
| 19 | Revenue Analytics & Attribution | `models/revenue.py` · `schemas/revenue.py` · `services/revenue_service.py` | `admin/revenue.py` | `api/revenue.ts` · `types/revenue.ts` · `hooks/useRevenue.ts` |

\* Module 2-এর register + profile কার্যকরী উদাহরণ হিসেবে লেখা আছে — বাকি অংশ
(login, OTP, user_devices, roles/permissions) একই ফাইলে/প্যাটার্নে যোগ করবে।

**cross-cutting services** (কোনো একটা মডিউলের না): `services/cache_service.py`,
`search_service.py`, `paywall_service.py`, `recommendation_service.py`,
`trending_service.py`, `notification_dispatch_service.py`।

## নোট

- কনভেনশন ও ডিজাইন-সিদ্ধান্তের ব্যাখ্যার জন্য আগে বানানো নোটগুলো দেখো (Module-wise
  Revision Notes, Query Concepts Note, SQL Mastery Note) — `docs/` ফোল্ডারে আছে।
- মূল প্রজেক্ট ডকুমেন্টেশনে ব্যাকএন্ড স্ট্যাক হিসেবে PHP/Laravel উল্লেখ ছিল; এই
  স্ক্যাফোল্ড Python/FastAPI/SQLAlchemy দিয়ে বানানো — টেবিল ডিজাইন ও কনভেনশনের
  লজিক একই থাকবে, শুধু ভাষা/ফ্রেমওয়ার্ক বদলেছে।
- role-based routing স্ট্রাকচারটা Poribar Health প্রজেক্টের `api/v1/{admin,auth,
  director,public,user,volunteer}/` কনভেনশন অনুসরণ করে বানানো হয়েছে।
