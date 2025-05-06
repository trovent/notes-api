#!/usr/bin/env python3

import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Depends, Response
from typing import List



"""
FastAPI application that provides a RESTful API for a note application.
GET /nodes - Get all notes
GET /nodes/{id} - Get a note by ID
POST /nodes - Create a new note
PUT /nodes/{id} - Update a note by ID
DELETE /nodes/{id} - Delete a note by ID
"""

# create "data" directory if it doesn't exist

if not os.path.exists("data"):
    os.makedirs("data")

# Database setup
DATABASE_URL = "sqlite:///./data/notes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Note model
class NoteDB(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    category = Column(String, nullable=True)
    icon = Column(String, nullable=True)  # New field
    duedate = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

# Pydantic model
class NoteCreate(BaseModel):
    title: str
    content: str
    category: str | None = None
    icon: str | None = None
    duedate: str | None = None

class NoteResponse(NoteCreate):
    id: int

    class Config:
        orm_mode = True

# FastAPI app
app = FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(NoteDB).all()

@app.get("/notes/{id}", response_model=NoteResponse)
def get_note_by_id(id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).filter(NoteDB.id == id).first()
    if not note:
        return Response(status_code=404, content="Note not found")
    return note

@app.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = NoteDB(**note.dict())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.put("/notes/{id}", response_model=NoteResponse)
def update_note(id: int, note: NoteCreate, db: Session = Depends(get_db)):
    existing_note = db.query(NoteDB).filter(NoteDB.id == id).first()
    if not existing_note:
        return Response(status_code=404, content="Note not found")
    for key, value in note.dict().items():
        setattr(existing_note, key, value)
    db.commit()
    db.refresh(existing_note)
    return existing_note

@app.delete("/notes/{id}")
def delete_note(id: int, db: Session = Depends(get_db)):
    note = db.query(NoteDB).filter(NoteDB.id == id).first()
    if not note:
        return Response(status_code=404, content="Note not found")
    db.delete(note)
    db.commit()
    return Response(status_code=204)