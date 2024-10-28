from tortoise.models import Model
from tortoise import fields
from .enum import (
    Gender,
) 


class Address(Model):
    id = fields.IntField(pk=True)
    street = fields.CharField(max_length=255)
    city = fields.CharField(max_length=100)
    state = fields.CharField(max_length=100)
    zip_code = fields.CharField(max_length=20)
    country = fields.CharField(max_length=100)
    user = fields.ForeignKeyField("models.User", related_name="addresses")  


class FamilyMember(Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    relationship = fields.CharField(max_length=50)
    birthdate = fields.DateField()
    email = fields.CharField(max_length=255, unique=True, null=True)
    phone_number = fields.CharField(max_length=15, unique=True, null=True)
    address = fields.ForeignKeyField("models.Address", related_name="family_members", null=True)
    user = fields.ForeignKeyField("models.User", related_name="family_members")
    gender = fields.CharEnumField(Gender)


