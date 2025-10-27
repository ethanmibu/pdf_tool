import argparse
from pathlib import Path
from .merge import merge_pdfs
from .split import split_pdf

def main():
    parser = argparse.ArgumentParser(
        prog="pdf_toolkit",
        description="Merge and split PDF files from the command line."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # merge subcommand
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs")
    merge_parser.add_argument("inputs", nargs="+", help="Input PDF paths in order")
    merge_parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output PDF path (e.g. output/merged.pdf)"
    )

    # split subcommand
    split_parser = subparsers.add_parser("split", help="Split a PDF")
    split_parser.add_argument("input", help="Input PDF path")
    split_mode = split_parser.add_mutually_exclusive_group(required=True)
    split_mode.add_argument("--all", action="store_true", help="Export each page separately")
    split_mode.add_argument("--range", nargs=2, metavar=("START", "END"), help="Page range (1-based)")
    split_parser.add_argument(
        "-d", "--dir",
        default="output",
        help="Output directory (default: output)"
    )

    args = parser.parse_args()

    if args.command == "merge":
        merge_pdfs(args.inputs, args.output)
        print(f"Merged into {args.output}")

    elif args.command == "split":
        if args.all:
            paths = split_pdf(args.input, args.dir)
        else:
            start, end = map(int, args.range)
            paths = split_pdf(args.input, args.dir, start_page=start, end_page=end)

        print("Created:")
        for p in paths:
            print(f" - {Path(p)}")

if __name__ == "__main__":
    main()