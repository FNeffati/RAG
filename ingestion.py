import re
import pypdf 
from pathlib import Path



inputs = Path("data/raw")
MAX_CHARS = 1000

# Parse
def ingest_pdf_text(pdf_path):
    """
    Reads a PDF file and extracts all text content.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: All extracted text combined into a single string.
    """
    pages = []
    with open(pdf_path, 'rb') as file:
        reader = pypdf.PdfReader(file)
        # extract text
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text: 
                pages.append({
                    "page": i,
                    "text": text
                })
                
    return pages


def extract():
    extracted_corpus = []
    for pdf_path in inputs.rglob('*.pdf'):
        if pdf_path:
            extracted_corpus.append({
        "source": pdf_path.name,
        "pages": ingest_pdf_text(pdf_path)
    })
    return extracted_corpus


# Chunk
"""
    Converts extracted PDF text into paragraph-level chunks with metadata.

    This function takes a corpus of parsed PDF documents (where each document
    contains page-level text) and splits each page into paragraphs using blank
    line separation. Each paragraph is then stored as an individual chunk with
    associated metadata for traceability.

    Args:
        extracted_corpus (list[dict]): A list of documents, where each document
            has the structure:
            {
                "source": str,           # file name or document identifier
                "text": list[dict]      # list of pages
                    [
                        {
                            "page": int,
                            "text": str
                        },
                        ...
                    ]
            }

    Returns:
        dict[str, list[dict]]: A dictionary mapping each source document name
        to a list of paragraph chunks. Each chunk has the structure:
            {
                "source": str,         # document name
                "page": int,           # page number
                "paragraph": str       # paragraph text
            }

    Notes:
        - Paragraphs are split using blank lines (regex: r"\\n\\s*\\n").
        - Empty or whitespace-only paragraphs are removed.
        - Output is flattened (no nesting by page).
        - No merging, overlap, or size control is applied.
"""

def split_text(text):
    return [text[i:i+MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]

def chunk():
    extracted_corpus = extract()
    paragraphs = []
    for file in extracted_corpus:
        current = []
        for f in file["pages"]:
            text = f["text"]
            page = f["page"]
            pars = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            chunks = []
            for p in pars:
                if len(p) > MAX_CHARS:
                    pieces = split_text(p)
                else:
                    pieces = [p]

                for piece in pieces:
                    chunks.append({
                        "source": file["source"],
                        "page": page,
                        "text": piece
                    })

            current.extend(chunks)
        paragraphs.append(current)
    return [item for sublist in paragraphs for item in sublist]