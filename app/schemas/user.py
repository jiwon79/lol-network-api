from decimal import Decimal
from typing import List
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    profile_image: str
    level: Decimal
    tier_class: str
    division: Decimal
    league_points: Decimal

class FriendModel(BaseModel):
    username: str
    weight: Decimal
    
class UserNetwork(BaseModel):
    username: str
    profileImage: str
    friend: List[FriendModel]