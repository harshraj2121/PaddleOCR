from pythonfiles import group_and_pair, ocr_text_extraction
from pythonfiles import llm_call
import os
from pprint import pprint

print("code is running")

# 1. getting the text form ocr
filepath = "./pdfs/form_006.pdf"
source_name = os.path.basename(filepath)
result = ocr_text_extraction(filepath)

# 2. getting the lines form the extracted text
for res in result:
    lines = group_and_pair(res["rec_texts"], res["rec_boxes"], res["rec_scores"])
    ocr_text = "\n".join(lines)


result = llm_call(ocr_text)
result["ocr_text"] = ocr_text
result["source_path"] = source_name

pprint(result)