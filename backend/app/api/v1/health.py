"""
Health-check endpoint -- Docker healthcheck ও লোড ব্যালান্সার এটা ব্যবহার করে।
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}
