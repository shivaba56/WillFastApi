from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr, validator
from .enum import AccountType

class BankDetailsCreate(BaseModel):
    bank_name: str = Field(max_length=255)
    account_number: str = Field(max_length=50)
    routing_number: str = Field(max_length=50, null=True)
    account_type: AccountType
    family_member: Optional[int] = None

    @validator('bank_name')
    def bank_name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Bank name must not be empty')
        return v

    @validator('account_number')
    def account_number_must_be_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('Account number must be numeric')
        return v

    @validator('routing_number')
    def routing_number_must_be_numeric_if_provided(cls, v):
        if v and not v.isdigit():
            raise ValueError('Routing number must be numeric if provided')
        return v

    @validator('account_type')
    def account_type_is_valid(cls, v):
        if v not in AccountType:
            raise ValueError('Invalid account type')
        return v
    

class BankCreateResponse(BaseModel):
    id: int 
    bank_name: str 
    account_number: str 
    routing_number: str 
    account_type: AccountType
    user: int 
    family_member: int
    
    class Config:
        from_attributes = True 