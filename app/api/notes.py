from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.session import SessionLocal
from app.schemas import notes as schemas

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all notes
@router.get("/notes/", response_model=list[schemas.Note])
def get_all_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).all()

# Get notes by campaign ID
@router.get("/notes/campaign/{campaign_id}", response_model=list[schemas.Note])
def get_notes_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    return db.query(models.Note).filter(models.Note.campaign_id == campaign_id).all()

# Get generic notes only
@router.get("/notes/generic/", response_model=list[schemas.Note])
def get_generic_notes(db: Session = Depends(get_db)):
    return db.query(models.Note).filter(models.Note.campaign_id.is_(None)).all()

# Create a note
@router.post("/notes/", response_model=schemas.Note)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    new_note = models.Note(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# Update a note
@router.put("/notes/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, payload: schemas.NoteUpdate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)
    return note

# Delete a note
@router.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}
