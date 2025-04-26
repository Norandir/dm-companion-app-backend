from pydantic import BaseModel
from typing import Optional

# For reading a campaign (e.g. GET requests)
class Campaign(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy objects

# For creating a new campaign (e.g. POST request)
class CampaignCreate(BaseModel):
    name: str
    description: str

# For updating an existing campaign (e.g. PUT request)
class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
