# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    notes = relationship("Note", back_populates="campaign", cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)

    # Optional campaign linkage
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    # Relationship (optional for later use)
    campaign = relationship("Campaign", back_populates="notes")