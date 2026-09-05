from paddleocr import PaddleOCR

ocr = PaddleOCR(
return_word_box=True,
text_detection_model_name="PP-OCRv5_mobile_det",
text_recognition_model_name="PP-OCRv5_mobile_rec",
use_doc_orientation_classify=False,
use_doc_unwarping=False,
use_textline_orientation=False,
text_det_limit_side_len=960,
enable_mkldnn=False,
cpu_threads=4,
)


def ocr_text_extraction(file_path):
    return ocr.predict(file_path)



#ocr raw_text preprocessing
def group_and_pair(rec_texts, rec_boxes, rec_scores, score_threshold=0.5, y_tolerance=10):

    print("Group and pair function is Running!!")
    items = [
        (text, box, score)
        for text, box, score in zip(rec_texts, rec_boxes, rec_scores)
        if score >= score_threshold
    ] #items ka confidence filter ke according content banao

    if not items:
        return []

    items.sort(key=lambda i: (i[1][1], i[1][0]))        # y then x


    lines = []
    current_line = [items[0]]
    current_y = items[0][1][1]

    for item in items[1:]:
        y1 = item[1][1]
        if abs(y1 - current_y) <= y_tolerance:
            current_line.append(item)
        else:
            lines.append(current_line)
            current_line = [item]
            current_y = y1
    lines.append(current_line)



    result = []
    for line in lines:
        line.sort(key=lambda i: i[1][0])
        line_text = " ".join(text for text, box, score in line)
        result.append(line_text)

    return result


if __name__ == "__main__":
    rec_texts = [
        "APP-2025-0001", "Application No.:",
        "Divya Kapoor", "Applicant Name:",
        "51 Civil Lines", "Address:",
    ]
    rec_boxes = [
        [160, 148, 280, 166], [47, 148, 140, 166],
        [160, 178, 280, 196], [47, 178, 140, 196],
        [160, 208, 280, 226], [47, 208, 140, 226],
    ]
    rec_scores = [0.98, 0.95, 0.97, 0.96, 0.94, 0.93]

    lines = group_and_pair(rec_texts, rec_boxes, rec_scores)
    for line in lines:
        print(line)