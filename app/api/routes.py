from fastapi import APIRouter, UploadFile, File
from app.services.doc_ingestion import embed_uploaded_file
from app.services.qa_engine import ask_question

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    result = embed_uploaded_file(content, filename)
    return {"status": "uploaded", "chunks_stored": result}

@router.post("/ask")
async def ask(query: str):
    return ask_question(query)
