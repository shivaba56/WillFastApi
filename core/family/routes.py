from fastapi import APIRouter, Depends
from core.auth.models import User
from core.shared.auth import get_current_user
from .models import Address, FamilyMember
from .schema import AddressCreate, AddressResponse, FamilyMemberCreate, FamilyMemberResponse
from core.shared.middleware import JWTBearer

family_router = APIRouter()


@family_router.post("/addresses", response_model=AddressResponse, dependencies=[Depends(JWTBearer())])
async def create_address(address: AddressCreate, user: User = Depends(get_current_user) ):
    address_data = address.model_dump()
    address_data["user"] = user
    address_obj = await Address.create(**address_data)
    return address_obj

@family_router.post("/family-members", response_model=FamilyMemberResponse, dependencies=[Depends(JWTBearer())])
async def create_family_member(family_member: FamilyMemberCreate, user: User = Depends(get_current_user)):
    family_data = family_member.model_dump()
    family_data["user_id"] = user.id
    family_member_obj = await FamilyMember.create(**family_data)
    return family_member_obj