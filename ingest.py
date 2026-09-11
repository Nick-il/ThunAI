from pathlib import Path
from io import BytesIO

import fitz
import pytesseract

from PIL import Image

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


DOCUMENT_DIR = Path("documents")
CHROMA_DIR = "chroma_db"


def extract_pdf_text(pdf_path):

    doc = fitz.open(pdf_path)

    documents = []

    for page_number, page in enumerate(doc):

        # First try normal PDF text extraction
        text = page.get_text().strip()

        # If there is little/no text, use OCR
        if len(text) < 20:

            print(
                f"OCR processing: "
                f"{pdf_path.name} - page {page_number + 1}"
            )

            pix = page.get_pixmap(dpi=300)

            image = Image.open(
                BytesIO(pix.tobytes("png"))
            )

            text = pytesseract.image_to_string(image)

        if text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": pdf_path.name,
                        "page": page_number + 1
                    }
                )
            )

    return documents


# -----------------------------
# LOAD DOCUMENTS
# -----------------------------

documents = []

for pdf_file in DOCUMENT_DIR.glob("*.pdf"):

    print(f"\nProcessing: {pdf_file.name}")

    docs = extract_pdf_text(pdf_file)

    documents.extend(docs)


print(f"\nLoaded {len(documents)} pages")


# -----------------------------
# CHUNK
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")


if not chunks:
    raise ValueError(
        "No text was extracted from the documents."
    )


# -----------------------------
# EMBEDDINGS
# -----------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# -----------------------------
# CHROMA
# -----------------------------

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DIR
)

print("\nDocuments successfully stored in Chroma!")