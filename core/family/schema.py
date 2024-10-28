from pydantic import BaseModel, EmailStr, Field, constr
from pydantic.types import Annotated, StringConstraints
from typing import Optional
from datetime import date
from .enum import (
    Gender,
)  



class AddressCreate(BaseModel):
    street: str = Field(max_length=255)
    city: str = Field(max_length=100)
    state: str = Field(max_length=100)
    zip_code: str = Field(max_length=20)
    country: str = Field(max_length=100)


class AddressResponse(BaseModel):
    id: int
    street: str
    city: str
    state: str
    zip_code: str
    country: str
    user: int

    class Config:
        from_attributes = True  # Update from orm_mode to from_attributes


class FamilyMemberCreate(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    relationship: str = Field(max_length=50)
    birthdate: date
    gender: Gender
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(default=None, max_length=15)
    address: Optional[AddressCreate] = None
    user_id: int  # Reference to the User


class FamilyMemberResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    relationship: str
    birthdate: date
    gender: Gender
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    address: Optional[AddressResponse] = None
    user_id: int  # Reference to the User

    class Config:
        from_attributes = True