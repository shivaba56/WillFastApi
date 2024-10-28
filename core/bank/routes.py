from fastapi import APIRouter, HTTPException, Depends
from tortoise.exceptions import IntegrityError
from tortoise import Tortoise
from typing import List, Optional
from pydantic import BaseModel

from core.auth.models import User
from core.bank.models import BankDetails
from core.bank.schemas import BankCreateResponse, BankDetailsCreate
from core.shared.auth import get_current_user
from core.shared.middleware import JWTBearer

bank_routes = APIRouter()


@bank_routes.post(
    "/bank-details",
    response_model=BankCreateResponse,
    dependencies=[Depends(JWTBearer())],
)
async def create_bank_detail(
    bank_details: BankDetailsCreate, user: User = Depends(get_current_user) 
):
    try:
        # Determine the family member ID or default to user ID

        family_member_id = (
            bank_details.family_member if bank_details.family_member else None
        )
        if family_member_id:
            bank_obj = BankDetails.filter(user = user).exists()
            if not bank_obj:
                raise HTTPException(status_code=400, detail= "You need to add your bank first") 

        # Create a new BankDetail instance
        new_bank_detail = await BankDetails.create(
            bank_name=bank_details.bank_name,
            account_number=bank_details.account_number,
            routing_number=bank_details.routing_number,
            account_type=bank_details.account_type,
            user=user,
            family_member_id=family_member_id,
        )
        return new_bank_detail
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=str(e))


@bank_routes.get(
    "/bank-details",
    response_model=List[BankCreateResponse],
    dependencies=[Depends(JWTBearer())],
)
async def get_bank_details(user: User = Depends(get_current_user)):
    try:
        # Fetch bank details associated with the user and their family members
        bank_details = await BankDetails.filter(
            user=user
        ).all()
        return bank_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))