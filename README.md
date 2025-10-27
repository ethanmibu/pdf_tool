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

## Configuration

Defaults are controlled by `config.json` in the project root:

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

```bash
git clone https://github.com/ethanmibu/pdf_tool.git
cd pdf_tool
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Merge PDFs

Combine multiple PDFs (from your configured input_dir) into one:
```bash
python -m pdf_toolkit merge input1.pdf input2.pdf
```

Output:
Merged into output/merged.pdf

---

You can also specify a custom output filename:
```bash
python -m pdf_toolkit merge input1.pdf input2.pdf -o output/custom_name.pdf
```

---

## Split PDF

all pages:
```bash
python -m pdf_toolkit split input.pdf --all
```

Output:
Created:
 - output/page_1.pdf
 - output/page_2.pdf
 - ...

---

## Split PDF (Page Range)

Extract a specific range:
```bash
python -m pdf_toolkit split input.pdf --range 3 10
```

Output:
Created:
 - output/pages_3_to_10.pdf

---

## Works with any directory

For example, if your PDFs are in your downloads folder:
```bash
python -m pdf_toolkit merge ~/Downloads/input1.pdf ~/Downloads/input2.pdf -o ~/Desktop/merged.pdf
```

---

## Graphical Interface (GUI)

You can also launch a simple drag-and-drop style interface built with tkinter:
```bash
python -m pdf_toolkit gui
```

---

## Install as a CLI tool

You can also install this project directly using pip (no need to clone the repo):

```bash
python3 -m venv pdfenv
source pdfenv/bin/activate
pip install git+https://github.com/ethanmibu/pdf_tool.git
pdf_toolkit --help
```

Once installed, you can use CLI commands:
```bash
pdf_toolkit merge input1.pdf input2.pdf -o output/merged.pdf
pdf_toolkit split input.pdf --range 3 10
pdf_toolkit gui
```
--- 

### macOS note
On some macOS Python builds (especially the Xcode/Command Line Tools Python), launching the Tk GUI can fail with a Tcl/Tk version error.  
If that happens, you can still use the full CLI, or create a virtual environment from a Homebrew-installed Python (which bundles a compatible Tk), then run:

```bash
brew install python@3.12
/opt/homebrew/bin/python3.12 -m venv gui_venv
source gui_venv/bin/activate
pip install -r requirements.txt
python -m pdf_toolkit gui
```

---

## Project structure


```text
pdf_project/
├─ pdf_toolkit/
│  ├─ __init__.py
│  ├─ __main__.py      # allows `python -m pdf_toolkit ...`
│  ├─ cli.py           # CLI entry point / subcommands
│  ├─ config.py        # loads config.json defaults
│  ├─ merge.py         # merge_pdfs()
│  ├─ split.py         # split_pdf()
│  └─ gui.py           # tkinter GUI launcher / UI logic
├─ tests/
│  ├─ test_merge.py
│  └─ test_split.py
├─ input/              # default input folder (you drop PDFs here)
│  ├─ sample1.pdf
│  └─ sample2.pdf
├─ output/             # default output folder (tool writes here)
│  └─ merged.pdf
├─ config.json         # user config for default dirs
├─ requirements.txt
├─ .gitignore
├─ README.md
├─ Makefile
└─ LICENSE