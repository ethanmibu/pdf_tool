from pypdf import PdfReader, PdfWriter
from pathlib import Path

def split_pdf(input_path, output_dir, start_page=None, end_page=None):
    """
    Split a PDF.
    input_path : str | Path
        Source PDF.
    output_dir : str | Path
        Folder where output PDFs go.
    start_page : int | None
        1-based first page to extract. If None, will split into single-page PDFs.
    end_page : int | None
        1-based last page to extract (inclusive). Ignored if start_page is None.
    Returns list[Path] of generated files.
    """
    reader = PdfReader(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    created_files = []

    # Case 1: no range → export each page to its own file
    if start_page is None and end_page is None:
        for i, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)
            out_path = output_dir / f"page_{i}.pdf"
            with open(out_path, "wb") as f:
                writer.write(f)
            created_files.append(out_path)
        return created_files

    # normalize + bounds check
    if start_page is None or end_page is None:
        raise ValueError("If you provide a range, you must give both start_page and end_page.")

    if start_page < 1 or end_page < start_page or end_page > len(reader.pages):
        raise ValueError("Invalid page range.")

    writer = PdfWriter()
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    out_path = output_dir / f"pages_{start_page}_to_{end_page}.pdf"
    with open(out_path, "wb") as f:
        writer.write(f)

    created_files.append(out_path)
    return created_files