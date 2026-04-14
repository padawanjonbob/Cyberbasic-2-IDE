import tkinter as tk
import os
import pywinstyles

from ide_ui import CyberUI
from highlighter import CyberHighlighter
from file_manager import FileManager
from runner import Runner
from editor_features import EditorFeatures
from docs_engine import DocsEngine

from cyberbasic_config import THEMES, FONT_FAMILY, FONT_SIZE


class CyberController:
    def __init__(self):
        self.root = tk.Tk()
        pywinstyles.apply_style(self.root, "dark")

        # =========================
        # STATE
        # =========================
        self.file_path = None
        self.font_family = FONT_FAMILY
        self.font_size = FONT_SIZE

        # =========================
        # MODULES
        # =========================
        self.files = FileManager(self)
        self.runner = Runner(self)
        self.editor_features = EditorFeatures(self)

        # =========================
        # 🔥 CREATE DOCS FIRST
        # =========================
        self.docs = DocsEngine(self)

        # =========================
        # UI (NOW SAFE)
        # =========================
        self.ui = CyberUI(self.root, self)

        # =========================
        # CONNECT DOCS TO UI
        # =========================
        self.docs.attach_ui(self.ui)

        docs_path = "docs"
        if os.path.exists(docs_path):
            self.docs.load_folder(docs_path)

        # =========================
        # HIGHLIGHTER
        # =========================
        self.highlighter = CyberHighlighter(self.ui.editor)

        self.editor_features.attach()

        self.root.mainloop()

    # =========================
    # FILES
    # =========================
    def new_file(self):
        self.ui.editor.delete("1.0", "end")
        self.file_path = None

    def open_folder(self):
        self.files.open_folder()

    def save_file(self):
        self.files.save_file()

    # =========================
    # RUN
    # =========================
    def run_code(self):
        self.runner.run_code()

    # =========================
    # THEMES
    # =========================
    def change_theme(self, name):
        theme = THEMES[name]

        self.ui.editor.config(
            bg=theme["bg"],
            fg=theme["fg"],
            insertbackground=theme["fg"]
        )

        self.highlighter.update_colors(theme)
        self.highlighter.highlight_all()
        self.ui.line_nums.redraw()

    # =========================
    # FONT SYSTEM
    # =========================
    def change_font(self, size):
        self.font_size = size
        font = (self.font_family, self.font_size)

        self.ui.editor.config(font=font)

        self.ui.console.config(
            font=(self.font_family, max(8, self.font_size - 2))
        )

        self.ui.line_nums.redraw()

    # =========================
    # COLOR EDITOR
    # =========================
    def open_color_editor(self):
        self.ui.open_color_editor()
