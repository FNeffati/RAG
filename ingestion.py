import re
import pypdf 
from pathlib import Path



inputs = Path("data/raw")

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


extracted_corpus = []
for pdf_path in inputs.rglob('*.pdf'):
    if pdf_path:
        extracted_corpus.append({
    "source": pdf_path.name,
    "text": ingest_pdf_text(pdf_path)
})


print(len(extracted_corpus))

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

paragraphs = {}
for file in extracted_corpus:
    current = []
    for f in file["text"]:
        text = f["text"]
        page = f["page"]
        pars = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        chunks = []
        for p in pars:
            chunks.append({
            "source":file["source"],
            "page": page,
            "paragraph": p
            })

        current.extend(chunks)

    paragraphs[file["source"]] = current
