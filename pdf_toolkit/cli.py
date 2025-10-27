import argparse
from pathlib import Path
from .merge import merge_pdfs
from .split import split_pdf
from .config import load_config


def resolve_input_path(p: str, input_dir: Path, output_dir: Path) -> Path:
    """
    Try to resolve a user-supplied file path.
    Priority:
    1. literal path they gave
    2. <input_dir>/<their path>
    3. <output_dir>/<their path>
    """
    path = Path(p)
    if path.exists():
        return path

    alt_in = input_dir / path
    if alt_in.exists():
        return alt_in

    alt_out = output_dir / path
    if alt_out.exists():
        return alt_out

    # fall back to whatever they gave; downstream code will raise a clean error
    return path


def main():
    config = load_config()
    input_dir = Path(config["input_dir"])
    output_dir = Path(config["output_dir"])

    parser = argparse.ArgumentParser(
        prog="pdf_toolkit",
        description="Merge and split PDF files from the command line."
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # MERGE subcommand
    merge_parser = subparsers.add_parser("merge", help="Merge multiple PDFs")
    merge_parser.add_argument(
        "inputs",
        nargs="+",
        help="Input PDF paths in order (will search input_dir and output_dir)"
    )
    merge_parser.add_argument(
        "-o", "--output",
        required=False,
        default=str(output_dir / "merged.pdf"),
        help=f"Output PDF path (default: {output_dir}/merged.pdf)"
    )

    # SPLIT subcommand
    split_parser = subparsers.add_parser("split", help="Split a PDF")
    split_parser.add_argument(
        "input",
        help="Input PDF path (will search input_dir and output_dir)"
    )

    split_mode = split_parser.add_mutually_exclusive_group(required=True)
    split_mode.add_argument(
        "--all",
        action="store_true",
        help="Export each page separately"
    )
    split_mode.add_argument(
        "--range",
        nargs=2,
        metavar=("START", "END"),
        help="Page range (1-based inclusive). Example: --range 3 10"
    )

    split_parser.add_argument(
        "-d", "--dir",
        required=False,
        default=str(output_dir),
        help=f"Output directory for split pages (default: {output_dir})"
    )

    args = parser.parse_args()

    # handle merge
    if args.command == "merge":
        resolved_inputs = [
            resolve_input_path(p, input_dir, output_dir)
            for p in args.inputs
        ]
        merge_pdfs(resolved_inputs, args.output)
        print(f"✅ Merged into {args.output}")
        return

    # handle split
    if args.command == "split":
        resolved_input = resolve_input_path(args.input, input_dir, output_dir)

        if args.all:
            paths = split_pdf(resolved_input, args.dir)
        else:
            start, end = map(int, args.range)
            paths = split_pdf(resolved_input, args.dir, start_page=start, end_page=end)

        print("✅ Created:")
        for p in paths:
            print(f" - {Path(p)}")
        return


if __name__ == "__main__":
    main()