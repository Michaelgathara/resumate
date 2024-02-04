# !pip install pymupdf

import fitz
import re


# rnum = 18
# fpath = f"../resumes/resume_{rnum}/resume_{rnum}.pdf"

# doc = fitz.open(fpath)
# text = ""
# # toks = []
# for page in doc:
#     text += re.sub(r"/\d\.\s+|[a-z]\)\s+|•\s+|[A-Z]\.\s+|[IVX]+\.\s+/g", "", page.get_text())
#     # toks.append(page.get_text("words", delimiters=None))

# print(rnum, rnum, rnum, rnum, rnum)
# print(text)


for rnum in range(20):
    fpath = f"../resumes/resume_{rnum}/resume_{rnum}.pdf"

    doc = fitz.open(fpath)
    text = ""
    for page in doc:
        # text += re.sub(r"/\d\.\s+|[a-z]\)\s+|•\s+|[A-Z]\.\s+|[IVX]+\.\s+/g", "", page.get_text())
        text += re.sub(r"●( |\n)|\||-( |\n)|▪( |\n)|•( |\n)|‑( |\n)", "", page.get_text())
    print("RESUME NUMBER", rnum)
    print(text)