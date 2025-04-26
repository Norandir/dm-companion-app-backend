from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.session import SessionLocal
from app.schemas import campaigns as schemas

router = APIRouter()

# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all campaigns
@router.get("/campaigns/", response_model=list[schemas.Campaign])
def get_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).all()

# Get a specific campaign by ID
@router.get("/campaigns/{campaign_id}", response_model=schemas.Campaign)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

# Create a new campaign
@router.post("/campaigns/", response_model=schemas.Campaign)
def create_campaign(payload: schemas.CampaignCreate, db: Session = Depends(get_db)):
    new_campaign = models.Campaign(name=payload.name, description=payload.description)
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

# Update an existing campaign
@router.put("/campaigns/{campaign_id}", response_model=schemas.Campaign)
def update_campaign(campaign_id: int, payload: schemas.CampaignUpdate, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if payload.name is not None:
        campaign.name = payload.name
    if payload.description is not None:
        campaign.description = payload.description

    db.commit()
    db.refresh(campaign)
    return campaign

# Delete an existing campaign
@router.delete("/campaigns/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()
    return {"message": "Campaign deleted successfully"}
