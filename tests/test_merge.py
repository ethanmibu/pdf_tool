from pdf_toolkit.merge import merge_pdfs
from pypdf import PdfReader
from pathlib import Path

def test_merge_creates_pdf(tmp_path):
    # setup: make two tiny one-page PDFs for testing
    from pypdf import PdfWriter

    p1 = tmp_path / "a.pdf"
    p2 = tmp_path / "b.pdf"

    for path, text in [(p1, "A"), (p2, "B")]:
        w = PdfWriter()
        w.add_blank_page(width=200, height=200)  # simple blank page
        with open(path, "wb") as f:
            w.write(f)

    out = tmp_path / "merged.pdf"
    merge_pdfs([p1, p2], out)

    reader = PdfReader(out)
    assert len(reader.pages) == 2
    assert out.exists()