import re
import fitz # PyMuPDF
from typing import List, Tuple


EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
CPF_REGEX = re.compile(r"(?:\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})")
ADDRESS_REGEX = re.compile(
r"\b(?:Rua:|R\.|Avenida:|Av:\.|Av:|Travessa:|Praça:|Praca:|Rodovia:|Rod:|Alameda:|Pagador:  |Al:\.)\s+[^\n,]{3,60}\s*(?:,\s*\d{1,5})?",
re.IGNORECASE,
)
TARJA_FILL = (0, 0, 0)




def find_matches_in_words(words: List[Tuple[float, float, float, float, str]], regex: re.Pattern):
    """
    Procura o padrão nas palavras e retorna apenas os retângulos (bboxes)
    diretamente sobre as palavras que contêm o match.
    """
    bboxes = []
    for x0, y0, x1, y1, text in words:
        if regex.search(text):
            bboxes.append((x0, y0, x1, y1))
    return bboxes




def merge_close_bboxes(bboxes: List[Tuple[float, float, float, float]], gap=1.0):
    if not bboxes:
        return []
    boxes = [list(b) for b in bboxes]
    boxes.sort(key=lambda b: (b[0], b[1]))
    merged = []
    cur = boxes[0]
    for b in boxes[1:]:
        if (b[0] <= cur[2] + gap) and (b[1] <= cur[3] + gap) and (b[3] >= cur[1] - gap):
            cur[2] = max(cur[2], b[2])
            cur[3] = max(cur[3], b[3])
            cur[0] = min(cur[0], b[0])
            cur[1] = min(cur[1], b[1])
        else:
            merged.append(tuple(cur))
            cur = b
    merged.append(tuple(cur))
    return merged




def redact_pdf(input_path: str, output_path: str, redact_email=True, redact_cpf=True, redact_address=True):
    doc = fitz.open(input_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        words = page.get_text("words")
        words = [(w[0], w[1], w[2], w[3], w[4]) for w in words]
        all_bboxes = []


        if redact_email:
            all_bboxes.extend(find_matches_in_words(words, EMAIL_REGEX))
        if redact_cpf:
            all_bboxes.extend(find_matches_in_words(words, CPF_REGEX))
        if redact_address:
            all_bboxes.extend(find_matches_in_words(words, ADDRESS_REGEX))


        merged = merge_close_bboxes(all_bboxes, gap=0.5)


        for bbox in merged:
            x0, y0, x1, y1 = bbox
            pad = 0.8
            rect = fitz.Rect(x0 - pad, y0 - pad, x1 + pad, y1 + pad)
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(fill=TARJA_FILL, color=TARJA_FILL)
            shape.commit()


    doc.save(output_path, deflate=True)
    doc.close()