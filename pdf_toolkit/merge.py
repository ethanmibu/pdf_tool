from pypdf import PdfReader, PdfWriter
from pathlib import Path

def merge_pdfs(input_paths, output_path):
    """
    Merge multiple PDFs into a single PDF.
    input_paths : list[str | Path]
        PDFs in the order you want them merged.
    output_path : str | Path
        Output PDF file path.
    """
    writer = PdfWriter()

    for pdf in input_paths:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path