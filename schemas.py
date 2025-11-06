import uuid

from fastapi import Form
from pydantic import BaseModel


class ReturnSchema(BaseModel):
    id: uuid.UUID


class UserSchemaIn(BaseModel):
    name: str
    password: str

    @classmethod
    def as_form(cls, name: str = Form(...), password: str = Form(...)) -> Form:
        return cls(name=name, password=password)


class UserSchema(BaseModel):
    name: str
    password: str

    @classmethod
    def as_form(cls, name: str = Form(...), password: str = Form(...)) -> Form:
        return cls(name=name, password=password)


class UserSchemaOut(UserSchema, ReturnSchema):
    pass
