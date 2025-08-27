from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import shutil
import os
from pathlib import Path
import uuid
import asyncio

from models.database import create_tables, get_db, Meeting, ActionItem
from services.transcription import TranscriptionService
from services.insight_extraction import InsightExtractionService
from services.vector_store import VectorStoreService
from config import config

app = FastAPI(title="AI Meeting Intelligence Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
config.UPLOAD_DIR.mkdir(exist_ok=True)
config.PROCESSED_DIR.mkdir(exist_ok=True)

# Initialize services
transcription_service = TranscriptionService()
insight_service = InsightExtractionService()
vector_service = VectorStoreService()

# Create tables
create_tables()

async def process_meeting_background(meeting_id: str, file_path: str):
    """Background task to process uploaded meeting"""
    # Get a new database session for the background task
    from models.database import SessionLocal
    db = SessionLocal()
    
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            print(f"Meeting {meeting_id} not found")
            return
        
        print(f"Starting processing for meeting {meeting_id}")
        
        # Extract audio if video file
        audio_path = file_path
        if Path(file_path).suffix.lower() in ['.mp4', '.avi', '.mov']:
            audio_path = str(config.PROCESSED_DIR / f"{meeting_id}.wav")
            transcription_service.extract_audio_from_video(file_path, audio_path)
        
        # Transcribe
        print(f"Transcribing audio for meeting {meeting_id}")
        transcript = await transcription_service.transcribe_audio(audio_path)
        
        if not transcript:
            raise Exception("No transcript generated")
        
        print(f"Transcript generated, length: {len(transcript)} characters")
        
        # Extract insights
        print(f"Extracting insights for meeting {meeting_id}")
        action_items = await insight_service.extract_action_items(transcript)
        decisions = await insight_service.extract_decisions(transcript)
        participants = await insight_service.identify_participants(transcript)
        key_topics = await insight_service.extract_key_topics(transcript)
        
        # Update meeting record
        meeting.transcript = transcript
        meeting.action_items = action_items
        meeting.decisions = decisions
        meeting.participants = participants
        meeting.key_topics = key_topics
        meeting.processed = True
        
        # Add to vector store
        await vector_service.add_meeting(
            meeting_id, 
            transcript,
            {
                "filename": meeting.filename,
                "participants": participants,
                "key_topics": key_topics
            }
        )
        
        # Save action items separately
        for item in action_items:
            action_item = ActionItem(
                meeting_id=meeting_id,
                description=item.get("description", ""),
                assignee=item.get("assignee"),
                priority=item.get("priority", "medium")
            )
            db.add(action_item)
        
        db.commit()
        print(f"Successfully processed meeting {meeting_id}")
        
        # Cleanup temporary files
        if audio_path != file_path and Path(audio_path).exists():
            Path(audio_path).unlink()
            
    except Exception as e:
        print(f"Processing error for meeting {meeting_id}: {str(e)}")
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            meeting.processed = False
            db.commit()
    finally:
        db.close()

@app.post("/upload-meeting")
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in config.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}")
    
    # Generate unique meeting ID
    meeting_id = str(uuid.uuid4())
    file_path = config.UPLOAD_DIR / f"{meeting_id}{file_ext}"
    
    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
    
    # Create meeting record
    meeting = Meeting(
        id=meeting_id,
        filename=file.filename,
        processed=False
    )
    db.add(meeting)
    db.commit()
    
    # Start background processing
    background_tasks.add_task(process_meeting_background, meeting_id, str(file_path))
    
    return {"meeting_id": meeting_id, "message": "Upload successful. Processing started."}

@app.get("/meetings")
async def get_meetings(db: Session = Depends(get_db)):
    meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).all()
    return [
        {
            "id": meeting.id,
            "filename": meeting.filename,
            "title": meeting.title,
            "duration": meeting.duration,
            "participants": meeting.participants,
            "processed": meeting.processed,
            "created_at": meeting.created_at.isoformat() if meeting.created_at else None,
            "action_items_count": len(meeting.action_items or []),
            "decisions_count": len(meeting.decisions or [])
        }
        for meeting in meetings
    ]

@app.get("/meetings/{meeting_id}")
async def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "id": meeting.id,
        "filename": meeting.filename,
        "title": meeting.title,
        "transcript": meeting.transcript,
        "participants": meeting.participants,
        "action_items": meeting.action_items,
        "decisions": meeting.decisions,
        "key_topics": meeting.key_topics,
        "processed": meeting.processed,
        "created_at": meeting.created_at.isoformat() if meeting.created_at else None
    }

@app.get("/search")
async def search_meetings(q: str, db: Session = Depends(get_db)):
    try:
        results = await vector_service.search_meetings(q)
        
        # Get full meeting details for results
        meeting_ids = list(set([r["meeting_id"] for r in results]))
        meetings = db.query(Meeting).filter(Meeting.id.in_(meeting_ids)).all()
        meeting_dict = {m.id: m for m in meetings}
        
        return [
            {
                "meeting_id": result["meeting_id"],
                "content_snippet": result["content"][:200] + "...",
                "meeting_title": meeting_dict[result["meeting_id"]].title,
                "meeting_filename": meeting_dict[result["meeting_id"]].filename,
                "created_at": meeting_dict[result["meeting_id"]].created_at.isoformat() if meeting_dict[result["meeting_id"]].created_at else None
            }
            for result in results
            if result["meeting_id"] in meeting_dict
        ]
    except Exception as e:
        return {"error": f"Search failed: {str(e)}", "results": []}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Meeting Intelligence Platform is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)