import glob
import os
from llmcall import llm_call
from ocrstructure import ocr_text_extraction, group_and_pair

DB_DIRECTORY = "faiss_chunks"
ALL_FILES = "twopdf"

print("running")
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
        result["source_path"] = file

        chunks.append(result)
        print(chunks)

    return chunks


chunks = run_all_files()
print(len(chunks))