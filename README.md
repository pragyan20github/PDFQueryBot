# PDFQueryBot

PDFQueryBot is a web application that allows users to upload PDF files, ask questions based on the content of the PDFs, and receive answers in a chatbot format. Built with a **React.js** frontend and a **FastAPI** backend, it uses **Sentence-BERT** for embedding and **T5** for generative question-answering.

---

## Getting Started

Follow these steps to set up and run PDFQueryBot locally:

### Prerequisites

1. **Python 3.x** (for the backend)
2. **Node.js** and **npm** (for the frontend)

### Backend Setup (FastAPI)

1. Clone the repository or download the project files.
2. Navigate to the backend directory and create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` should contain the following dependencies:

   ```
   fastapi
   uvicorn
   sqlalchemy
   pydantic
   PyMuPDF
   transformers
   sentence-transformers
   langchain
   ```

4. Create the SQLite database:

   ```bash
   python main.py
   ```

5. Run the FastAPI server with `uvicorn`:

   ```bash
   uvicorn backend.main:app --reload
   ```

   The backend will now be available at `http://localhost:8000`.

### Frontend Setup (React.js)

1. Navigate to the frontend directory and install dependencies:

   ```bash
   npm install
   ```

2. Run the React app:

   ```bash
   npm start
   ```

   The frontend will now be available at `http://localhost:3000`.

---

## Project Structure

### Backend (`main.py`)

The backend is built using **FastAPI** and is responsible for the following functionalities:

1. **Uploading PDFs**: The `/upload` endpoint allows users to upload PDF files, which are saved to the server.
2. **Asking Questions**: The `/ask` endpoint allows users to ask questions based on the uploaded PDF's content. The backend processes the question using **Sentence-BERT** embeddings and generates an answer with the **T5** model.
3. **Storing Chat History**: The `/get_chats/{pdf_filename}` endpoint retrieves chat history for a specific PDF. The chat history (questions and answers) is stored in an SQLite database.
4. **PDF Text Extraction**: The `/get_pdf_text/{pdf_filename}` endpoint extracts text from PDFs for debugging and preview purposes.

### Frontend (`Apps.js`)

The frontend is built with **React.js** and allows users to interact with the backend. Here’s how the main components work:

1. **File Upload**: Users can select and upload PDFs using an HTML file input. The `handleUpload` function handles the PDF upload, sending the file to the backend.
2. **Chat Interface**: Users can select a PDF from a sidebar to view the chat history. The `handleSelectPdf` function fetches the previous chat entries for the selected PDF from the backend.
3. **Question Input**: Below the conversation, there’s an input field where users can type questions. When the user submits a question, the `handleAskQuestion` function sends the question to the backend for processing and displays the answer in a conversation format.
4. **Sidebar**: The left sidebar displays the list of uploaded PDFs. Clicking on a PDF name loads its respective chat history.
5. **New Chat Button**: Clicking on the "New Chat" button clears the conversation and allows the user to start a fresh chat.

### Styling (`styles.css`)

The application uses **CSS** to provide a clean and responsive user interface. Some notable sections include:

- **Taskbar**: A header with the title and "New Chat" button.
- **Sidebar**: A list of uploaded PDFs with hover effects.
- **Main Content**: Displays the PDF upload section, the conversation, and the question input field.
- **Chat Bubbles**: Messages from the user and the bot are displayed in different colored bubbles for clarity.
- **Error Display**: A red message is shown when something goes wrong (e.g., file upload or question submission).

---

## Working

1. **Upload a PDF**: Click the "Upload PDF" button to browse and select a PDF. Once uploaded, the PDF is stored on the server, and its filename is displayed in the sidebar.
2. **Ask Questions**: Type a question in the input field at the bottom and click the "Ask" button. The system processes the question based on the selected PDF’s content and responds in a chatbot-style format.
3. **View Chat History**: When you click on a PDF in the sidebar, the system loads previous questions and answers associated with that PDF. You can continue the conversation from where you left off.
4. **Start a New Chat**: Click the "New Chat" button to clear the conversation and ask questions about a new or different PDF.

---

## Tech Stack

- **Frontend**: React.js
- **Backend**: FastAPI
- **NLP**: 
  - Sentence-BERT (for embeddings)
  - T5 (for question answering)
- **Database**: SQLite (for storing chat history)
- **PDF Parsing**: PyMuPDF for extracting text from PDFs

---

## Future Improvements

- Support for multiple users (authentication and authorization).
- Support for more advanced PDF parsing (e.g., handling complex layouts or images).
- More sophisticated error handling and user feedback.
- Adding additional NLP models for more accurate or diverse answers.

---

## License

This project is open-source and available under the MIT License.

## Author
This project was created by Pragyan Srivastava. 
You can reach out to me via https://www.linkedin.com/in/pragyan-srivastava-2400b1259/.
