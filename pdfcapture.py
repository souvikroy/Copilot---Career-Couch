import fitz, time, re
from langchain_community.docstore.document import Document

class pdfreadercapture:

    def __init__(self):
        super().__init__()

    def read_pdf_reader(self, file_path):
        documents = []
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        text = text.replace("\n", "")
        text = re.sub(r"([a-z\.!?])([A-Z])", r"\1 \2", text)
        return text