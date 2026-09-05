import glob
import os
import sys
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from .llmcall import llm_call
from .ocrstructure import ocr_text_extraction, group_and_pair
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

DB_DIRECTORY = "faiss_chunks"
ALL_FILES = "twopdf"



#agar all results ka koi use nahi hua to usse hata hi dena
def run_all_files(allfiles):
    print("running this!")
    chunks = []
    all_results = []
    for file in glob.glob(os.path.join(allfiles, "*")):
        # 1. getting the text form ocr
        result = ocr_text_extraction(file)

        # 2. getting the lines form the extracted text
        for res in result:
            lines = group_and_pair(res["rec_texts"], res["rec_boxes"], res["rec_scores"])
            ocr_text = "\n".join(lines)

        result = llm_call(ocr_text)


        result["ocr_text"] = ocr_text
        base_path = os.path.basename(file)
        result["source_file"] = os.path.join("pdfs", base_path)

        page_content = (
            f"applicant_name : {result['applicant_name']}\n"
            f"application_number: {result['application_number']}\n"
            f"form_id: {result['form_id']}\n"
            f"form_type: {result['form_type']}\n"
            f"ocr_text: {result['ocr_text']}\n"
        )


        metadata = {
            "source_file" : result["source_file"],
            "form_id": result["form_id"],
            "form_type": result["form_type"],
            "applicant_name": result["applicant_name"],
            "application_number": result["application_number"],
            "submission_date": result["submission_date"],
            "gender": result["gender"],
            "contact_number": result["contact_number"],
            "email": result["email"],
            "complete_address": result["complete_address"],
            "martial_status": result["martial_status"],
        }

        chunks.append(Document(page_content = page_content, metadata = metadata))
        all_results.append(result)

        print(len(chunks))

    return chunks, all_results


#creating embeddings
def creating_embeddings(chunks):
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(DB_DIRECTORY)
    print(f"index saved to {DB_DIRECTORY}")


def add_embedidngs(new_chunks):
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    if os.path.exists(os.path.join(DB_DIRECTORY, "index.faiss")):
        vectorstore = FAISS.load_local(
            DB_DIRECTORY, embedding_model, allow_dangerous_deserialization=True
        )
        vectorstore.add_documents(new_chunks)
        print(f"appended {len(new_chunks)} new_chunks to existing index")
    else:
        vectorstore = FAISS.from_documents(new_chunks, embedding_model)
        print(f"created new index with {len(new_chunks)} chunks")

    vectorstore.save_local(DB_DIRECTORY)
    print(f"index saved to {DB_DIRECTORY}")


def check_if_exists_in_VDB(file):
    if not os.path.exists(os.path.join(DB_DIRECTORY, "index.faiss")):
        return False
    
    embedding_model  = GoogleGenerativeAIEmbeddings(model="models/gemini-embeddings-001")
    vectorstore = FAISS.load_local(DB_DIRECTORY, embedding_model, allow_dangerous_deserialization=True)
    print("filepath",os.path.join("pdfs", file))
    for doc in vectorstore.docstore._dict.values():
        if doc.metadata.get("source_file") == os.path.join("pdfs", file):
            return True

    return False