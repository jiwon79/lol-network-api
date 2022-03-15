from decimal import Decimal
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    profile_image: str
    level: Decimal
    tier_class: str
    division: Decimal
    league_points: Decimal