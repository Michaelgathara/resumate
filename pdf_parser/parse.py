# !pip install pymupdf

import fitz

fpath = "../resumes/resume_0/resume_0.pdf"

doc = fitz.open(fpath)
text = ""
for page in doc:
    text += page.get_text()

print(text)