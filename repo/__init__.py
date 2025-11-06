from fastapi import Depends
from sqlalchemy.orm import Session

from db import get_db
from repo.userRepo import UserRepository


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)
