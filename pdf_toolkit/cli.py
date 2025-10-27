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

    # gui subcommand
    gui_parser = subparsers.add_parser(
        "gui",
        help="Open the PDF Toolkit GUI (may require a Tk-compatible Python install)"
    )
    gui_parser.add_argument(
        "--force",
        action="store_true",
        help="Actually attempt to start the tkinter GUI. "
             "Without this flag, we just print guidance instead of launching."
    )

    # merge subcommand
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

    # split subcommand
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

    # ----- GUI MODE -----
    if args.command == "gui":
        if not args.force:
            print(
                "GUI mode is optional and requires a Tk-compatible Python build.\n"
                "Your system Python may terminate when initializing tkinter on some macOS versions.\n\n"
                "To attempt launching the GUI anyway, run:\n"
                "    python -m pdf_toolkit gui --force\n\n"
                "All PDF merge/split features are still available via the CLI."
            )
            return

        # Only import tkinter and attempt launch if explicitly forced
        try:
            from .gui import launch_gui
        except Exception as e:
            print(
                "Could not import GUI components. You can still use the CLI.\n"
                f"Details: {e}"
            )
            return

        # launch_gui may still crash the interpreter on broken Tk setups.
        # That's now an opt-in risk.
        launch_gui()
        return

    # ----- MERGE MODE -----
    if args.command == "merge":
        resolved_inputs = [
            resolve_input_path(p, input_dir, output_dir)
            for p in args.inputs
        ]
        merge_pdfs(resolved_inputs, args.output)
        print(f"✅ Merged into {args.output}")
        return

    # ----- SPLIT MODE -----
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