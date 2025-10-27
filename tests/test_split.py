from pdf_toolkit.split import split_pdf
from pypdf import PdfWriter, PdfReader
from pathlib import Path

def _make_pdf(path, n_pages=3):
    w = PdfWriter()
    for _ in range(n_pages):
        w.add_blank_page(width=200, height=200)
    with open(path, "wb") as f:
        w.write(f)

def test_split_all_pages(tmp_path):
    src = tmp_path / "src.pdf"
    _make_pdf(src, n_pages=4)

    outputs = split_pdf(src, tmp_path, start_page=None, end_page=None)

    assert len(outputs) == 4
    for p in outputs:
        assert Path(p).exists()
        r = PdfReader(p)
        assert len(r.pages) == 1

def test_split_range(tmp_path):
    src = tmp_path / "src.pdf"
    _make_pdf(src, n_pages=5)

    outputs = split_pdf(src, tmp_path, start_page=2, end_page=4)

    assert len(outputs) == 1
    r = PdfReader(outputs[0])
    assert len(r.pages) == 3  # pages 2,3,4