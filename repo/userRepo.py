import uuid

from models import User


class UserRepository:
    def __init__(self, db):
        self.db = db

    def save(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_name(self, name: str):
        return self.db.query(User).filter_by(name=name).first()

    def find_by_id(self, id: uuid.UUID):
        return self.db.query(User).filter_by(id=id).first()
