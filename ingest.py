from pathlib import Path
import fitz
import numpy as np
from paddleocr import PaddleOCR
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

DOCUMENT_DIR = Path("documents")
CHROMA_DIR = "chroma_db"

# Initialize PaddleOCR globally so it loads into memory only once
ocr = PaddleOCR(
    use_textline_orientation=True,
    lang='en'
)

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    documents = []

    for page_number, page in enumerate(doc):
        # First try normal PDF text extraction
        text = page.get_text().strip()

        # If there is little/no text, trigger PaddleOCR
        if len(text) < 20:
            print(f"OCR processing: {pdf_path.name} - page {page_number + 1}")
            
            # Extract image without alpha channel (RGB)
            pix = page.get_pixmap(dpi=300, alpha=False)
            
            # Convert directly to numpy array for PaddleOCR
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, 3)
            
            # Execute PaddleOCR
            ocr_result = ocr.predict(img_array)
            
            if ocr_result and ocr_result[0]:
                text = "\n".join([line[1][0] for line in ocr_result[0]])
            else:
                text = ""

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
# CHUNK & EMBED
# -----------------------------
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(documents)
print(f"Created {len(chunks)} chunks")

if not chunks:
    raise ValueError("No text was extracted from the documents.")

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DIR
)
print("\nDocuments successfully stored in Chroma!")