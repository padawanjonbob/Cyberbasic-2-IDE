import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
import os, threading, subprocess
import pywinstyles

from ide_ui import CyberUI
from highlighter import CyberHighlighter
from cyberbasic_config import COLORS, THEMES, FONT_FAMILY

CYBERBASIC_PATH = "cyberbasic.exe"


class CyberController:
    def __init__(self):
        self.root = tk.Tk()

        pywinstyles.apply_style(self.root, "dark")
        self.setup_styles()

        self.ui = CyberUI(self.root, self)
        self.highlighter = CyberHighlighter(self.ui.editor)

        self.file_path = None

        # Highlight visuals
        self.ui.editor.tag_configure("current_line", background="#2a2d2e")
        self.ui.editor.tag_configure("current_word", background="#3a3d3e")

        # Events
        self.ui.editor.bind("<<Modified>>", self.on_change)
        self.ui.editor.bind("<KeyRelease>", self.update_cursor_ui)
        self.ui.editor.bind("<ButtonRelease>", self.update_cursor_ui)
        self.ui.editor.bind("<MouseWheel>", lambda e: self.ui.line_nums.redraw())

        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<F5>", lambda e: self.run_code())

        self.ui.sidebar.bind("<<TreeviewSelect>>", self.on_file_select)

        self.update_sidebar()
        self.highlight_current_line()

        self.root.mainloop()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    # =========================
    # FILES
    # =========================
    def new_file(self):
        self.ui.editor.delete("1.0", tk.END)
        self.file_path = None
        self.root.title("Untitled")

    def open_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            os.chdir(folder)
            self.update_sidebar()

    def update_sidebar(self):
        self.ui.sidebar.delete(*self.ui.sidebar.get_children())

        for file in os.listdir():
            path = os.path.abspath(file)
            self.ui.sidebar.insert("", "end", text=file, values=(path,))

    def on_file_select(self, event):
        selection = self.ui.sidebar.selection()
        if not selection:
            return

        values = self.ui.sidebar.item(selection, "values")
        if values:
            self.file_path = values[0]

            if os.path.isfile(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.ui.editor.delete("1.0", tk.END)
                    self.ui.editor.insert(tk.END, f.read())

                total = int(self.ui.editor.index("end-1c").split(".")[0])
                for i in range(1, total + 1):
                    self.highlighter.apply_line(i)

    def save_file(self):
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".bas")

        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.ui.editor.get("1.0", "end-1c"))

    # =========================
    # RUN
    # =========================
    def run_code(self):
        self.save_file()

        # clear console
        self.ui.console.config(state='normal')
        self.ui.console.delete("1.0", "end")
        self.ui.console.config(state='disabled')

        if self.file_path and os.path.exists(CYBERBASIC_PATH):
            threading.Thread(target=self.execute, daemon=True).start()

    def execute(self):
        proc = subprocess.Popen(
            [CYBERBASIC_PATH, self.file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in proc.stdout:
            self.root.after(0, self.log, line.strip())

    def log(self, msg):
        self.ui.console.config(state='normal')
        self.ui.console.insert("end", msg + "\n")
        self.ui.console.config(state='disabled')

    # =========================
    # THEMES & FONT
    # =========================
    def change_theme(self, theme_name):
        theme = THEMES[theme_name]

        self.ui.editor.config(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground="white"
        )

        self.highlighter.update_colors(theme)

        self.ui.editor.tag_configure("current_line", background=theme["current_line"])

        total = int(self.ui.editor.index("end-1c").split(".")[0])
        for i in range(1, total + 1):
            self.highlighter.apply_line(i)

    def change_font_size(self, size):
        self.ui.editor.config(font=(FONT_FAMILY, size))
        self.ui.console.config(font=(FONT_FAMILY, max(8, size - 2)))
        self.ui.line_nums.redraw()

    # =========================
    # COLOR EDITOR
    # =========================
    def open_color_editor(self):
        popup = tk.Toplevel(self.root)
        popup.title("Customize Colors")

        theme = {
            "bg": self.ui.editor["bg"],
            "fg": self.ui.editor["fg"],
            "keyword": self.ui.editor.tag_cget("keyword", "foreground"),
            "function": self.ui.editor.tag_cget("function", "foreground"),
            "comment": self.ui.editor.tag_cget("comment", "foreground"),
            "string": self.ui.editor.tag_cget("string", "foreground"),
        }

        def pick(key):
            color = colorchooser.askcolor()[1]
            if color:
                theme[key] = color
                apply()

        def apply():
            self.ui.editor.config(bg=theme["bg"], fg=theme["fg"])
            self.highlighter.update_colors(theme)

            total = int(self.ui.editor.index("end-1c").split(".")[0])
            for i in range(1, total + 1):
                self.highlighter.apply_line(i)

        for key in theme:
            tk.Button(popup, text=key, command=lambda k=key: pick(k)).pack(fill="x")

    # =========================
    # CURSOR UI
    # =========================
    def update_cursor_ui(self, e=None):
        self.highlight_current_line()
        self.highlight_current_word()
        self.ui.line_nums.redraw()

    def highlight_current_line(self):
        self.ui.editor.tag_remove("current_line", "1.0", tk.END)
        line = self.ui.editor.index("insert").split(".")[0]
        self.ui.editor.tag_add("current_line", f"{line}.0", f"{line}.end")

    def highlight_current_word(self):
        self.ui.editor.tag_remove("current_word", "1.0", tk.END)

        word = self.ui.editor.get("insert wordstart", "insert wordend")
        if not word.strip():
            return

        start = "1.0"
        while True:
            pos = self.ui.editor.search(rf'\y{word}\y', start, stopindex=tk.END, regexp=True)
            if not pos:
                break

            end = f"{pos}+{len(word)}c"
            self.ui.editor.tag_add("current_word", pos, end)
            start = end

    # =========================
    # EDIT EVENTS
    # =========================
    def on_change(self, event=None):
        if self.ui.editor.edit_modified():
            line = self.ui.editor.index("insert").split(".")[0]
            self.highlighter.apply_line(line)
            self.ui.editor.edit_modified(False)


if __name__ == "__main__":
    CyberController()
