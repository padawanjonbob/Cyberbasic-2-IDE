import os
from tkinter import filedialog


class FileManager:
    def __init__(self, controller):
        self.app = controller

    @property
    def ui(self):
        return self.app.ui

    def open_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.app.root_folder = folder
        self.update_sidebar(folder)

    def update_sidebar(self, folder):
        self.ui.sidebar.delete(*self.ui.sidebar.get_children())
        self.insert_node("", folder)

    def insert_node(self, parent, path):
        name = os.path.basename(path) or path
        node = self.ui.sidebar.insert(parent, "end", text=name, values=(path,))

        if os.path.isdir(path):
            try:
                for item in os.listdir(path):
                    self.insert_node(node, os.path.join(path, item))
            except:
                pass

    def on_file_select(self, event):
        sel = self.ui.sidebar.selection()
        if not sel:
            return

        path = self.ui.sidebar.item(sel[0], "values")[0]

        if os.path.isfile(path):
            self.open_file(path)

    def open_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        self.ui.editor.delete("1.0", "end")
        self.ui.editor.insert("1.0", content)

        self.app.file_path = path

        if hasattr(self.app, "highlighter"):
            self.app.highlighter.highlight_all()

    def save_file(self):
        if not self.app.file_path:
            self.app.file_path = filedialog.asksaveasfilename(
                defaultextension=".bas",
                filetypes=[("CyberBasic", "*.bas"), ("All Files", "*.*")]
            )

        if not self.app.file_path:
            return

        content = self.ui.editor.get("1.0", "end-1c")

        with open(self.app.file_path, "w", encoding="utf-8") as f:
            f.write(content)
