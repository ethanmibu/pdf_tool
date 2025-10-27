import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from .merge import merge_pdfs
from .split import split_pdf
from .config import load_config

def can_launch_tkinter():
    """
    Return True if we can safely import tkinter AND create a root window
    without exploding or triggering macOS dev tools prompts.

    Return False if anything looks sketchy.
    """
    try:
        import tkinter as tk  # try importing
    except Exception:
        return False

    try:
        # Try to create a root window in a "headless" way.
        # We destroy it immediately. This will typically be the point
        # where macOS's system python freaks out if Tk isn't configured.
        root = tk.Tk()
        root.withdraw()  # don't show it
        root.destroy()
    except Exception:
        return False

    return True

class PDFToolkitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Toolkit")
        self.root.geometry("500x500")

        # load config for defaults
        self.config = load_config()
        self.input_dir = Path(self.config["input_dir"])
        self.output_dir = Path(self.config["output_dir"])

        # tabs (Merge / Split)
        self.tab_var = tk.StringVar(value="merge")

        tab_frame = tk.Frame(self.root)
        tab_frame.pack(fill="x", pady=8)

        self.merge_tab_btn = tk.Radiobutton(
            tab_frame, text="Merge PDFs", variable=self.tab_var, value="merge",
            indicatoron=False, width=15, command=self._switch_tab
        )
        self.split_tab_btn = tk.Radiobutton(
            tab_frame, text="Split PDF", variable=self.tab_var, value="split",
            indicatoron=False, width=15, command=self._switch_tab
        )

        self.merge_tab_btn.pack(side="left", padx=5)
        self.split_tab_btn.pack(side="left", padx=5)

        # containers for each tab content
        self.merge_frame = tk.Frame(self.root, borderwidth=1, relief="groove")
        self.split_frame = tk.Frame(self.root, borderwidth=1, relief="groove")

        self.merge_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # build each tab's UI
        self._build_merge_tab()
        self._build_split_tab()

        # start on merge tab
        self._show_merge()

    # merge tab UI + logic
    def _build_merge_tab(self):
        # Listbox of selected PDFs
        list_frame = tk.Frame(self.merge_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(list_frame, text="Files to merge (in order):").pack(anchor="w")

        self.merge_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.merge_listbox.pack(fill="both", expand=True, pady=5)

        # buttons to add/remove/reorder
        btn_frame = tk.Frame(list_frame)
        btn_frame.pack(fill="x")

        tk.Button(btn_frame, text="Add PDFs", command=self._merge_add_files).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Remove Selected", command=self._merge_remove_selected).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Move Up", command=lambda: self._merge_move(-1)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Move Down", command=lambda: self._merge_move(1)).pack(side="left", padx=3)

        # output file name input
        out_frame = tk.Frame(self.merge_frame)
        out_frame.pack(fill="x", padx=10, pady=(0,10))

        tk.Label(out_frame, text="Output filename (will go in output_dir):").pack(anchor="w")
        self.merge_output_entry = tk.Entry(out_frame)
        self.merge_output_entry.insert(0, "merged_gui.pdf")
        self.merge_output_entry.pack(fill="x", pady=5)

        # merge button
        tk.Button(
            self.merge_frame,
            text="Merge PDFs",
            command=self._merge_execute
        ).pack(pady=5)

    def _merge_add_files(self):
        # let user pick multiple PDFs
        selected = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for path in selected:
            self.merge_listbox.insert(tk.END, path)

    def _merge_remove_selected(self):
        sel = self.merge_listbox.curselection()
        if not sel:
            return
        self.merge_listbox.delete(sel[0])

    def _merge_move(self, direction):
        sel = self.merge_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        new_idx = idx + direction
        if new_idx < 0 or new_idx >= self.merge_listbox.size():
            return
        text = self.merge_listbox.get(idx)
        self.merge_listbox.delete(idx)
        self.merge_listbox.insert(new_idx, text)
        self.merge_listbox.select_set(new_idx)

    def _merge_execute(self):
        # collect input paths in listbox order
        inputs = [self.merge_listbox.get(i) for i in range(self.merge_listbox.size())]
        if not inputs:
            messagebox.showerror("Error", "No input PDFs selected.")
            return

        out_name = self.merge_output_entry.get().strip()
        if not out_name.endswith(".pdf"):
            out_name += ".pdf"

        output_path = self.output_dir / out_name

        try:
            merge_pdfs(inputs, output_path)
        except Exception as e:
            messagebox.showerror("Merge Failed", str(e))
            return

        messagebox.showinfo("Success", f"Merged into:\n{output_path}")

    # split tab UI + logic
    def _build_split_tab(self):
        # input file selection
        in_frame = tk.Frame(self.split_frame)
        in_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(in_frame, text="PDF to split:").pack(anchor="w")

        path_row = tk.Frame(in_frame)
        path_row.pack(fill="x", pady=5)

        self.split_input_entry = tk.Entry(path_row)
        self.split_input_entry.pack(side="left", fill="x", expand=True)
        tk.Button(path_row, text="Browse", command=self._split_browse_file).pack(side="left", padx=5)

        # split mode
        mode_frame = tk.Frame(self.split_frame)
        mode_frame.pack(fill="x", padx=10, pady=(0,10))

        tk.Label(mode_frame, text="Split mode:").pack(anchor="w")

        self.split_mode_var = tk.StringVar(value="all")

        # "All pages" radio
        tk.Radiobutton(
            mode_frame, text="All pages (1 PDF per page)",
            variable=self.split_mode_var, value="all"
        ).pack(anchor="w")

        # "Range" radio
        range_row = tk.Frame(mode_frame)
        range_row.pack(fill="x", pady=5)
        tk.Radiobutton(
            range_row, text="Page range:",
            variable=self.split_mode_var, value="range"
        ).pack(side="left")

        tk.Label(range_row, text="Start").pack(side="left", padx=(10,2))
        self.range_start_entry = tk.Entry(range_row, width=5)
        self.range_start_entry.insert(0, "1")
        self.range_start_entry.pack(side="left")

        tk.Label(range_row, text="End").pack(side="left", padx=(10,2))
        self.range_end_entry = tk.Entry(range_row, width=5)
        self.range_end_entry.insert(0, "2")
        self.range_end_entry.pack(side="left")

        # output directory override (optional)
        outdir_frame = tk.Frame(self.split_frame)
        outdir_frame.pack(fill="x", padx=10, pady=(0,10))

        tk.Label(outdir_frame, text="Output directory (optional):").pack(anchor="w")
        self.split_outdir_entry = tk.Entry(outdir_frame)
        self.split_outdir_entry.insert(0, str(self.output_dir))
        self.split_outdir_entry.pack(fill="x", pady=5)

        # split button
        tk.Button(
            self.split_frame,
            text="Split PDF",
            command=self._split_execute
        ).pack(pady=5)

    def _split_browse_file(self):
        chosen = filedialog.askopenfilename(
            title="Select PDF to split",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if chosen:
            self.split_input_entry.delete(0, tk.END)
            self.split_input_entry.insert(0, chosen)

    def _split_execute(self):
        input_path = self.split_input_entry.get().strip()
        if not input_path:
            messagebox.showerror("Error", "No input PDF selected.")
            return

        outdir = self.split_outdir_entry.get().strip()
        if not outdir:
            outdir = str(self.output_dir)

        mode = self.split_mode_var.get()

        try:
            if mode == "all":
                paths = split_pdf(input_path, outdir)
            else:
                # range mode
                try:
                    start_page = int(self.range_start_entry.get().strip())
                    end_page = int(self.range_end_entry.get().strip())
                except ValueError:
                    messagebox.showerror("Error", "Start and End must be integers.")
                    return
                paths = split_pdf(input_path, outdir, start_page=start_page, end_page=end_page)

        except Exception as e:
            messagebox.showerror("Split Failed", str(e))
            return

        # show summary
        msg_lines = ["Created:"]
        for p in paths[:5]:
            msg_lines.append(f"- {p}")
        if len(paths) > 5:
            msg_lines.append(f"... ({len(paths)} files total)")

        messagebox.showinfo("Success", "\n".join(msg_lines))

    # Tab switching
    def _switch_tab(self):
        if self.tab_var.get() == "merge":
            self._show_merge()
        else:
            self._show_split()

    def _show_merge(self):
        self.split_frame.forget()
        self.merge_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def _show_split(self):
        self.merge_frame.forget()
        self.split_frame.pack(fill="both", expand=True, padx=10, pady=10)


def launch_gui():
    root = tk.Tk()
    app = PDFToolkitGUI(root)
    root.mainloop()