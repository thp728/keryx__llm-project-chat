from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash  # We'll create this next


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return (
            db.query(User).filter(func.lower(User.email) == func.lower(email)).first()
        )

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,  # Default to false for new users
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        return super().update(db, db_obj=db_obj, obj_in=update_data)


user = CRUDUser(User)
