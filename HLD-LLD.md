# High-Level Design (HLD) and Low-Level Design (LLD)

## 1. High-Level Design (HLD)

### System Architecture
The architecture of the system consists of the following major components:
- **Frontend (React.js):** Manages the user interface and handles user interactions.
- **Backend (FastAPI):** Provides REST APIs for uploading PDFs, querying data, and retrieving answers.
- **NLP Models (T5 and Sentence Transformers):** Process user queries based on PDF content.
- **Database (SQLite):** Stores chat history related to each PDF.

### Technology Stack:
- **Frontend:** React.js
- **Backend:** FastAPI
- **NLP:** T5 Model (for text generation), Sentence Transformers (for embeddings)
- **Database:** SQLite

---

## 2. Low-Level Design (LLD)

### API Endpoints
#### 1. **POST /upload**
- **Description:** Handles PDF file uploads.
- **Request:**
  - `file` (PDF file)
- **Response:**
  - `message: "File uploaded successfully"`
  - `filename: "uploaded-file.pdf"`

#### 2. **POST /ask**
- **Description:** Handles user questions related to a PDF.
- **Request:**
  - `filename: "uploaded-file.pdf"`
  - `question: "What is the main idea?"`
- **Response:**
  - `answer: "The main idea of the document is..."`

#### 3. **GET /get_chats/{pdf_filename}**
- **Description:** Retrieves the chat history for a specific PDF.
- **Response:**
  - A list of questions and answers for the given PDF.

### Database Schema
- **Table: `ChatHistory`**
  - `id`: Integer (Primary Key)
  - `pdf_filename`: String
  - `question`: Text
  - `answer`: Text

### Detailed Workflow
1. **File Upload:**
   - User uploads a PDF via the `/upload` endpoint.
   - The backend saves the file and extracts the text content.
2. **Question Handling:**
   - User sends a question to the `/ask` endpoint.
   - The backend extracts relevant text chunks from the PDF.
   - The NLP model generates an answer based on the text chunks.
3. **Answer Storage:**
   - The answer is stored in the `ChatHistory` table in the database.

### Error Handling
- **File Upload:** If no file is provided, return an error message.
- **Invalid Questions:** If the question cannot be answered, return a default response like "Sorry, I could not generate an answer."

### Security Considerations
- Input validation to avoid malicious file uploads.
- CORS handling to ensure secure interactions between frontend and backend.

### UI/UX Design
The user interface is designed to provide the following features:
1. **File Upload Interface**
2. **Chat Interface**
3. **Ask a Question Bar**
