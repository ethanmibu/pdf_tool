# pdf-toolkit

Small Python ClI tool for merging and splitting PDF files.

## Why I built this
I wanted a lightweight, local alternative to online “merge your PDFs” websites (which are sketchy for things like transcripts, IDs, contracts, etc.). This project is written in pure Python, uses `pypdf`, and exposes a simple CLI so you can do common PDF ops from the Terminal.

This repository is also structured like a proper Python project:
- Isolated virtual environment
- Clean package layout (`pdf_toolkit/`)
- Automated tests (`pytest`)
- CLI entry point (`python -m pdf_toolkit ...`)

It was good for learning:
- virtualenv / dependency management
- file I/O
- packaging Python code as a module
- argument parsing with `argparse`

---

## Features

- **Merge PDFs**
  - Combine multiple PDFs in a specific order into one output file
- **Split PDFs**
  - Export every single page as its own PDF
  - OR extract just a selected page range
  
- **CLI-first design**
  - No GUI needed, just run commands
- **Tested**
  - Includes pytest tests for both merge and split logic

---

## Project structure

```text
pdf-toolkit/
├─ pdf_toolkit/
│  ├─ __init__.py
│  ├─ __main__.py      # allows `python -m pdf_toolkit ...`
│  ├─ cli.py           # command-line parsing / routing
│  ├─ merge.py         # merge_pdfs()
│  └─ split.py         # split_pdf()
├─ tests/
│  ├─ test_merge.py
│  └─ test_split.py
├─ examples/
│  ├─ sample1.pdf
│  ├─ sample2.pdf
│  └─ demo_output.pdf  (generated example, usually gitignored)
├─ requirements.txt
├─ .gitignore
├─ README.md
└─ LICENSE