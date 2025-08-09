import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from analyzer import analyze_job_description
from pdf_detector import export_analysis_to_pdf
import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "competencies.db")

class JobAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Job Analyzer")
        try:
            self.master.state('zoomed')
        except Exception:
            try:
                self.master.attributes('-fullscreen', True)
            except Exception:
                pass

        main = ttk.Frame(master, padding=12)
        main.pack(fill='both', expand=True)

        header = ttk.Frame(main)
        header.pack(fill='x')
        ttk.Label(header, text="🔍 Job Analyzer", font=("Segoe UI", 18, "bold")).pack(side='left')

        form = ttk.LabelFrame(main, text="Input Jabatan", padding=10)
        form.pack(fill='x', pady=8)

        ttk.Label(form, text="Nama Jabatan:").grid(row=0, column=0, sticky='w', padx=4, pady=4)
        self.entry_title = ttk.Entry(form, width=80)
        self.entry_title.grid(row=0, column=1, sticky='ew', padx=4, pady=4)

        ttk.Label(form, text="Uraian Jabatan:").grid(row=1, column=0, sticky='nw', padx=4, pady=4)
        self.txt_desc = tk.Text(form, height=10, wrap='word')
        self.txt_desc.grid(row=1, column=1, sticky='ew', padx=4, pady=4)

        form.columnconfigure(1, weight=1)

        btns = ttk.Frame(main)
        btns.pack(fill='x', pady=6)
        ttk.Button(btns, text="Analisa", command=self.do_analyze).pack(side='left', padx=6)
        ttk.Button(btns, text="Export to PDF", command=self.do_export_pdf).pack(side='left', padx=6)
        ttk.Button(btns, text="Exit", command=master.quit).pack(side='right', padx=6)

        result_frame = ttk.LabelFrame(main, text="Hasil Analisa", padding=10)
        result_frame.pack(fill='both', expand=True, pady=8)
        self.txt_result = tk.Text(result_frame, wrap='word', state='disabled')
        self.txt_result.pack(fill='both', expand=True)

    def do_analyze(self):
        title = self.entry_title.get().strip()
        desc = self.txt_desc.get("1.0", "end").strip()
        if not title or not desc:
            messagebox.showwarning("Input kurang", "Isi nama jabatan dan uraian.")
            return

        res = analyze_job_description(title, desc)
        self.display_result(res)

    def display_result(self, res):
        self.txt_result.config(state='normal')
        self.txt_result.delete("1.0", "end")
        lines = []
        lines.append(f"Nama Jabatan: {res.get('job_title')}")
        lines.append(f"Level Jabatan: {res.get('job_level')}")
        lines.append(f"Pendidikan: {res.get('education')}")
        lines.append(f"Usia: {res.get('age_range')}")
        lines.append(f"Pengalaman: {res.get('experience_range')}")
        lines.append("")
        lines.append("Standar Kompetensi:")
        for i, c in enumerate(res.get('competencies', []), 1):
            lines.append(f"{i}. {c.get('name')}")
            lines.append(f"   - {c.get('definition')}")
        self.txt_result.insert("1.0", "\\n".join(lines))
        self.txt_result.config(state='disabled')

    def do_export_pdf(self):
        title = self.entry_title.get().strip()
        desc = self.txt_desc.get("1.0", "end").strip()
        if not title or not desc:
            messagebox.showwarning("Input kurang", "Isi nama jabatan dan uraian.")
            return
        res = analyze_job_description(title, desc)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
        if not file_path:
            return
        export_analysis_to_pdf(file_path, res.get('job_title'), desc, res.get('education'), res.get('age_range'), res.get('experience_range'), res.get('job_level'), res.get('competencies'))
        messagebox.showinfo("Sukses", f"PDF tersimpan di: {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JobAnalyzerApp(root)
    root.mainloop()
