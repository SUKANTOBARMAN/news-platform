"""
Shared FastAPI dependencies -- get_db, get_current_user ইত্যাদি এখানে থাকবে।
"""
from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db as _get_db
from app.models.user import User

# re-exported so routes can do: from app.api.deps import get_db
get_db = _get_db

# tokenUrl শুধু Swagger UI-এর "Authorize" বাটনের জন্য দরকার (ডকুমেন্টেশন পারপাসে)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    JWT টোকেন ডিকোড করে বর্তমান লগইন-করা ইউজার রিটার্ন করে।
    যেকোনো route-এ ব্যবহার করতে: current_user: User = Depends(get_current_user)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="অথেন্টিকেশন ব্যর্থ — লগইন করা প্রয়োজন",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception
    try:
        payload = decode_access_token(token)
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError) as e:
        raise credentials_exception from e

    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise credentials_exception
    return user


def require_permission(permission_name: str):
    """
    নির্দিষ্ট পারমিশন থাকা বাধ্যতামূলক করে এমন একটা dependency ফ্যাক্টরি।
    ব্যবহার: current_user: User = Depends(require_permission("articles.publish"))
    """

    def checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.has_permission(permission_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"এই কাজের জন্য '{permission_name}' পারমিশন দরকার",
            )
        return current_user

    return checker