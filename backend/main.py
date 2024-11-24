from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fitz  # PyMuPDF for PDF text extraction
import os
from sqlalchemy.orm import Session
from transformers import T5Tokenizer, T5ForConditionalGeneration
from sentence_transformers import SentenceTransformer, util
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# FastAPI app setup
app = FastAPI()

# CORS setup for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database setup
DATABASE_URL = "sqlite:///./pdfquerybot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model for storing chat history
class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True)
    pdf_filename = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize models
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
roberta_tokenizer = T5Tokenizer.from_pretrained("t5-small")
roberta_model = T5ForConditionalGeneration.from_pretrained("t5-small")

# Pydantic models
class QuestionRequest(BaseModel):
    filename: str
    question: str

class ChatRequest(BaseModel):
    pdf_filename: str
    question: str
    answer: str

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Endpoint to upload a PDF file."""
    file_path = os.path.join("./uploads", file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded successfully", "filename": file.filename}

@app.post("/ask")
async def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    """Endpoint to process a question based on an uploaded PDF."""
    filename = request.filename
    question = request.question

    file_path = os.path.join("./uploads", filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"message": "File not found"})

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")

    if not text.strip():
        return JSONResponse(status_code=400, content={"message": "No text extracted from PDF"})

    # Text chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)

    # Embed chunks and find the most relevant
    question_embedding = embedding_model.encode(question, convert_to_tensor=True)
    chunk_embeddings = embedding_model.encode(chunks, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(question_embedding, chunk_embeddings)
    best_chunk_index = similarity_scores.argmax().item()
    most_relevant_chunk = chunks[best_chunk_index]

    t5_input_text = f"question: {question} context: {most_relevant_chunk}"
    t5_input_ids = roberta_tokenizer.encode(t5_input_text, return_tensors="pt", truncation=True, max_length=512)
    t5_outputs = roberta_model.generate(t5_input_ids, max_length=150)
    
    generative_answer = roberta_tokenizer.decode(t5_outputs[0], skip_special_tokens=True)

    if generative_answer.strip() == "<s>":
        return {"answer": "Sorry, I could not generate an answer from the document."}
    
    # Save the question/answer in the database
    db_chat = ChatHistory(pdf_filename=filename, question=question, answer=generative_answer)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return {"answer": generative_answer}

@app.get("/get_chats/{pdf_filename}")
async def get_chats(pdf_filename: str, db: Session = Depends(get_db)):
    """Get all chats for a specific PDF."""
    chats = db.query(ChatHistory).filter(ChatHistory.pdf_filename == pdf_filename).all()
    chat_entries = []
    for chat in chats:
        chat_entries.append(
            {
                "type": "user",  # Assuming the question is from the user
                "content": chat.question
            }
        )
        chat_entries.append(
            {
                "type": "bot",  # Assuming the answer is from the bot
                "content": chat.answer
            }
        )
    return {"chats": chat_entries}

@app.get("/get_pdf_text/{pdf_filename}")
async def get_pdf_text(pdf_filename: str):
    """Endpoint to retrieve and print the text of a PDF."""
    file_path = os.path.join("./uploads", pdf_filename)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"message": "File not found"})

    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text")

    if not text.strip():
        return JSONResponse(status_code=400, content={"message": "No text extracted from PDF"})

    print("Extracted Text:", text)  # Print to console
    return {"text": text}
