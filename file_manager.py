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
                for item in sorted(os.listdir(path)):
                    self.insert_node(node, os.path.join(path, item))
            except:
                pass

    def on_file_select(self, event):
        selected = self.ui.sidebar.focus()
        if not selected:
            return

        values = self.ui.sidebar.item(selected, "values")
        if not values:
            return

        path = values[0]

        if os.path.isfile(path):
            self.open_file(path)

    def open_file(self, path):
        # Markdown → docs
        if path.lower().endswith(".md"):
            if hasattr(self.app, "docs"):
                filename = os.path.basename(path)
                self.app.docs.open_file(filename)
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print("Error:", e)
            return

        self.ui.editor.delete("1.0", "end")
        self.ui.editor.insert("1.0", content)

        self.app.file_path = path

        if hasattr(self.app, "highlighter"):
            self.app.highlighter.highlight_all()

    def save_file(self):
        # =========================
        # ASK FOR PATH (NEW FILE)
        # =========================
        if not self.app.file_path:
            path = filedialog.asksaveasfilename(
                defaultextension=".bas",
                filetypes=[
                    ("CyberBasic", "*.bas"),
                    ("Markdown", "*.md"),
                    ("All Files", "*.*")
                ]
            )
    
            if not path:
                return  # user canceled
    
            self.app.file_path = path
    
        # =========================
        # WRITE FILE
        # =========================
        try:
            content = self.ui.editor.get("1.0", "end-1c")
    
            with open(self.app.file_path, "w", encoding="utf-8") as f:
                f.write(content)
    
        except Exception as e:
            print("Save error:", e)
            return
    
        # =========================
        # REFRESH SIDEBAR (IMPORTANT)
        # =========================
        if self.app.root_folder:
            self.update_sidebar(self.app.root_folder)
