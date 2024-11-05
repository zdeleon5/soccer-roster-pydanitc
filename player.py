from pydantic import BaseModel, Field
from typing_extensions import Optional


class Player(BaseModel):
    id: int
    name: str
    position: str
    team: str
    year_born: int

class PlayerRequest(BaseModel):
    id: Optional[int] = Field(description="ID not needed on post.", default=None)
    name: str = Field(min_length=1, max_length=50)
    position: str
    team: str
    year_born: int = Field(gt=1900, lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Zini",
                "position": "Attacker",
                "team": "N/A",
                "year_born": 2000
            }
        }
    }
