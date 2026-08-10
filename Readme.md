# FormQuery AI: OCR and RAG-Based Scanned Form Information Assistant

An AI-powered assistant that extracts text from scanned application forms using **Optical Character Recognition (OCR)** and answers natural-language questions about them using **Retrieval-Augmented Generation (RAG)**.

## Problem Statement

Banks, hospitals, insurance companies, schools, and government offices frequently store customer information in scanned application forms. These forms may contain personal details, application numbers, dates, addresses, selected options, handwritten notes, and other important information.

Finding a particular detail across hundreds of scanned forms requires employees to manually open and inspect each document — a process that is slow, repetitive, and prone to human error.

FormQuery AI solves this by extracting text from form images and enabling users to ask questions in plain English, with answers grounded strictly in the uploaded documents.

## Example Queries

- "What is the applicant's name in form 25?"
- "Which application contains the address New Delhi?"
- "Find the form submitted on March 15."
- "What contact number was provided by Rahul Sharma?"
- "Which applicants selected the premium plan?"
- "Summarize the information present in this application."
- "Which forms are missing an email address?"

For every response, the system retrieves the relevant form, answers only from the available document content, and displays the source form image or filename.

## Real-World Use Cases

- Insurance claim forms
- Bank account applications
- Loan application forms
- Hospital registration forms
- School admission forms
- Employee onboarding documents
- Government application forms

## How It Works

The application:

1. Accepts scanned form images.
2. Preprocesses the image to improve text visibility.
3. Uses OCR to extract text from the form.
4. Organizes the extracted text into fields and sections.
5. Stores the text with metadata (Form ID, applicant name, form type, submission date, source filename).
6. Converts the extracted content into embeddings.
7. Stores the embeddings in a vector database.
8. Retrieves the most relevant forms for a user question.
9. Sends the retrieved form content to an LLM.
10. Generates a grounded answer with document references.
11. Returns "Information not available in the uploaded forms" when sufficient evidence is not found.

### RAG Pipeline

```
Scanned Form Image
        ↓
Image Preprocessing
        ↓
OCR Text Extraction
        ↓
Field and Section Identification
        ↓
Text Chunking
        ↓
Embedding Generation
        ↓
FAISS or Chroma Vector Database
        ↓
User Question
        ↓
Relevant Form Retrieval
        ↓
LLM Generates Grounded Answer
        ↓
Answer + Source Form
```

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| OCR | PaddleOCR |
| Image Processing | OpenCV |
| Embeddings | sentence-transformers |
| Vector Database | FAISS |
| RAG Framework | LangChain and RAG |
| LLM | Gemini, Groq or a small local model |
| Frontend | React.js (Future Implementaion) |
| Metadata Storage | SQLite Database(Pydantic) |

## Dataset

This project uses the **FUNSD dataset** (Form Understanding in Noisy Scanned Documents), which contains 199 annotated scanned forms with annotations for questions, answers, headers, other text, and relationships between fields.

- The dataset is small enough for a beginner project but realistic enough to demonstrate document understanding.
- Start with 30–50 forms rather than processing the complete dataset.

### Example Stored Document

```json
{
  "form_id": "form_025",
  "form_type": "application_form",
  "applicant_name": "Rahul Sharma",
  "submission_date": "2025-03-15",
  "ocr_text": "Applicant Name: Rahul Sharma Address: New Delhi Phone: 9876543210",
  "source_image": "form_025.png"
}
```

## Project Structure

```
formquery-ai/
├── faiss_chunks/
│   ├── index.pkl           
│   └── index.faiss           
├── pythonfiles/
│   ├── llmcall                # Image preprocessing (OpenCV)
│   ├── ocr_text_extraction    # OCR extraction (PaddleOCR)
│   ├── group_and_pair         # Text structuring
│   └── vectordb_files_manag   # FAISS / Chroma indexing & retrieval
|
├── pdfs/
│   └── Sample Data

├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

```bash
git clone <repository-url>
cd formquery-ai
pip install -r requirements.txt
```

### Running the App

```bash
# Start the FastAPI backend
uvicorn src.api.main:app --reload

# Start the Streamlit frontend
streamlit run app/streamlit_app.py
```

## Evaluation

The project is evaluated across four dimensions:

1. **OCR Accuracy** — Checks whether names, dates, addresses, and form fields are extracted correctly.
2. **Retrieval Accuracy** — Checks whether the correct form appears in the top three retrieved documents.
3. **Answer Accuracy** — Verifies whether the answer matches the information in the source form.
4. **Grounding** — Ensures the model does not provide information that is absent from the retrieved document.

## Roadmap

- [ ] Image preprocessing pipeline
- [ ] OCR extraction and field/section parsing
- [ ] Metadata storage (SQLite/JSON)
- [ ] Embedding generation and vector store indexing
- [ ] RAG query pipeline with source attribution
- [ ] Streamlit UI for upload and Q&A
- [ ] Evaluation scripts for OCR, retrieval, and grounding accuracy

## License

MIT License

Copyright (c) 2026 Harsh Raj

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.