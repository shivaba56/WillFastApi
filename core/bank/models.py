from tortoise.models import Model
from tortoise import fields
from core.bank.enum import AccountType


class BankDetails(Model):
    id = fields.IntField(pk=True)
    bank_name = fields.CharField(max_length=255)
    account_number = fields.CharField(max_length=50)
    routing_number = fields.CharField(max_length=50, null=True)
    account_type = fields.CharEnumField(AccountType)
    user = fields.ForeignKeyField("models.User", related_name="bank_details", null=True)
    family_member = fields.ForeignKeyField(
        "models.FamilyMember", related_name="bank_details", null=True
    )

    class Meta:
        unique_together = (("account_number", "user"),) 