import glob
import os
import json
from llmcall import llm_call
from ocrstructure import ocr_text_extraction, group_and_pair
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

DB_DIRECTORY = "faiss_chunks"
ALL_FILES = "pdfs"



def run_all_files():
    chunks = []
    for file in glob.glob(os.path.join(ALL_FILES, "*")):
        print(file)
        # 1. getting the text form ocr
        result = ocr_text_extraction(file)

        # 2. getting the lines form the extracted text
        for res in result:
            lines = group_and_pair(res["rec_texts"], res["rec_boxes"], res["rec_scores"])
            ocr_text = "\n".join(lines)

        result = llm_call(ocr_text)
        result["ocr_text"] = ocr_text

        chunks.append(Document(page_content = json.dumps(result), metadata={"source" : file}))
        print(chunks)

    return chunks

#creating embeddings
def creating_embeddings(chunks):
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vectorstore = FAISS.from_documents(chunks, embedding_model)
    vectorstore.save_local(DB_DIRECTORY)
    print(f"index saved to {DB_DIRECTORY}")



final_chunks = run_all_files()
print(len(final_chunks))
creating_embeddings(final_chunks)


