from tortoise import Tortoise
from core.shared.conf import settings

Tortoise.init_models(["core.auth.models"], "models")

def init_db():
    db_url = settings.DATABASE
    return Tortoise.init(
        db_url=db_url,
        modules={"models": ["app.models"]},
    )
