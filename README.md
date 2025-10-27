# pdf-toolkit

Small Python CLI tool for merging and splitting PDF files.
![tests](https://github.com/ethanmibu/pdf_tool/actions/workflows/tests.yml/badge.svg)

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
pdf_project/
├─ pdf_toolkit/
│  ├─ __init__.py
│  ├─ __main__.py      # allows `python -m pdf_toolkit ...`
│  ├─ cli.py           # command-line parsing / routing
│  ├─ merge.py         # merge_pdfs()
│  └─ split.py         # split_pdf()
├─ tests/
│  ├─ test_merge.py
│  └─ test_split.py
├─ input/              # included in gitignore
│  ├─ sample1.pdf
│  └─ sample2.pdf
├─ output/             # included in gitignore
│  └─ output.pdf
├─ requirements.txt
├─ .gitignore
├─ README.md
├─ MakeFile
└─ LICENSE

---

## Configuration

Defaults are controlled by `config.json` in the project root:

```json
{
  "input_dir": "input",
  "output_dir": "output"
}

you can change these anytime, just rename "input_dir" and "output_dir" to your input and output folders in the root

example:
{
  "input_dir": "incoming_pdfs",
  "output_dir": "processed_pdfs"
}

---

## Setup

git clone https://github.com/ethanmibu/pdf_tool.git
cd pdf_tool
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

--- 

## Merge PDFs

Combine multiple PDFs (from your configured input_dir) into one:
python -m pdf_toolkit merge input1.pdf input2.pdf

Output:
Merged into output/merged.pdf

You can also specify a custom output filename:
python -m pdf_toolkit merge input1.pdf input2.pdf -o output/custom_name.pdf

---

## Split PDF

all pages:
python -m pdf_toolkit split input.pdf --all

Output:
Created:
 - output/page_1.pdf
 - output/page_2.pdf
 - ...

---

## Split PDF (Page Range)

Extract a specific range:
python -m pdf_toolkit split input.pdf --range 3 10

Output:
Created:
 - output/pages_3_to_10.pdf

---

## Works with any directory

For example, if your PDFs are in your downloads folder:
python -m pdf_toolkit merge ~/Downloads/input1.pdf ~/Downloads/input2.pdf -o ~/Desktop/merged.pdf