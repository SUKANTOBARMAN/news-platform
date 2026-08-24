"""
PUBLIC role router — লগইন ছাড়াই অ্যাক্সেসযোগ্য — যেকোনো ভিজিটর/পাঠক (Guest)
এই ফোল্ডারের সব endpoint ফাইলকে একত্রিত করে api/v1/router.py-তে mount হয়।
"""
from fastapi import APIRouter

from app.api.v1.public import articles
from app.api.v1.public import taxonomy
from app.api.v1.public import search
from app.api.v1.public import multimedia
from app.api.v1.public import events
from app.api.v1.public import classifieds

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["Public - Articles"])
api_router.include_router(taxonomy.router, prefix="/taxonomy", tags=["Public - Taxonomy"])
api_router.include_router(search.router, prefix="/search", tags=["Public - Search"])
api_router.include_router(multimedia.router, prefix="/multimedia", tags=["Public - Multimedia"])
api_router.include_router(events.router, prefix="/events", tags=["Public - Events"])
api_router.include_router(classifieds.router, prefix="/classifieds", tags=["Public - Classifieds"])
