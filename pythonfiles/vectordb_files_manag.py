import glob
import os
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
ALL_FILES = "pdfs"



#agar all results ka koi use nahi hua to usse hata hi dena
def run_all_files():
    print("running this!")
    chunks = []
    all_results = []
    for file in glob.glob(os.path.join(ALL_FILES, "*")):
        # 1. getting the text form ocr
        result = ocr_text_extraction(file)

        # 2. getting the lines form the extracted text
        for res in result:
            lines = group_and_pair(res["rec_texts"], res["rec_boxes"], res["rec_scores"])
            ocr_text = "\n".join(lines)

        result = llm_call(ocr_text)

        result["ocr_text"] = ocr_text
        result["source_file"] = file

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



if __name__ == "__main__":
    final_chunks, all_results = run_all_files()
    creating_embeddings(final_chunks)
