import tkinter as tk
from tkinter import ttk, colorchooser
import pywinstyles

from cyberbasic_config import THEMES, FONT_FAMILY, FONT_SIZE


class LineNumbers(tk.Canvas):
    def __init__(self, master, text):
        super().__init__(master, width=40, bg="#1e1e1e", highlightthickness=0)
        self.text = text

    def redraw(self):
        self.delete("all")

        if not self.text:
            return

        font = self.text["font"]

        i = self.text.index("@0,0")

        while True:
            d = self.text.dlineinfo(i)
            if d is None:
                break

            y = d[1]
            line = str(i).split(".")[0]

            self.create_text(
                30,
                y,
                text=line,
                fill="gray",
                anchor="ne",
                font=font
            )

            i = self.text.index(f"{i}+1line")


class CyberUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("CyberBasic 2 IDE")
        self.root.geometry("1200x800")

        pywinstyles.apply_style(self.root, "dark")

        # =========================
        # MENU
        # =========================
        menu = tk.Menu(root)
        root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=controller.new_file)
        file_menu.add_command(label="Open Folder", command=controller.open_folder)
        file_menu.add_command(label="Save", command=controller.save_file)
        file_menu.add_command(label="Run", command=controller.run_code)
        menu.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="View", menu=view_menu)

        # Themes
        self.theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Themes", menu=self.theme_menu)

        for name in THEMES:
            self.theme_menu.add_command(
                label=name,
                command=lambda n=name: controller.change_theme(n)
            )

        view_menu.add_separator()
        view_menu.add_command(
            label="Customize Colors",
            command=self.open_color_editor
        )

        # Font sizes
        font_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Font Size", menu=font_menu)

        for size in [10, 12, 14, 16, 18, 20, 24, 28]:
            font_menu.add_command(
                label=str(size),
                command=lambda s=size: controller.change_font(s)
            )

        # =========================
        # LAYOUT
        # =========================
        self.paned = tk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.sidebar = ttk.Treeview(self.paned, show="tree")
        self.sidebar.bind("<<TreeviewSelect>>", controller.files.on_file_select)
        self.paned.add(self.sidebar, width=250)

        self.right = tk.Frame(self.paned)
        self.paned.add(self.right)

        self.editor_frame = tk.Frame(self.right)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

        self.line_nums = LineNumbers(self.editor_frame, None)
        self.line_nums.pack(side=tk.LEFT, fill=tk.Y)

        self.editor = tk.Text(
            self.editor_frame,
            wrap="none",
            undo=True,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=(FONT_FAMILY, FONT_SIZE)
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.line_nums.text = self.editor

        self.editor.config(yscrollcommand=lambda *a: self.line_nums.redraw())

        # Syntax tags
        self.editor.tag_configure("keyword", foreground="cyan")
        self.editor.tag_configure("function", foreground="yellow")
        self.editor.tag_configure("comment", foreground="green")
        self.editor.tag_configure("string", foreground="orange")

        # Console
        self.console = tk.Text(
            self.right,
            height=10,
            bg="black",
            fg="green",
            font=(FONT_FAMILY, max(8, FONT_SIZE - 2))
        )
        self.console.pack(fill=tk.X)

        tk.Button(
            self.right,
            text="▶ Run",
            command=controller.run_code
        ).pack(fill=tk.X)

    # =========================
    # COLOR EDITOR
    # =========================
    def open_color_editor(self):
        popup = tk.Toplevel(self.root)
        popup.title("Color Editor")
        popup.geometry("340x420")

        theme = {
            "bg": self.editor["bg"],
            "fg": self.editor["fg"],
            "keyword": self.editor.tag_cget("keyword", "foreground"),
            "function": self.editor.tag_cget("function", "foreground"),
            "comment": self.editor.tag_cget("comment", "foreground"),
            "string": self.editor.tag_cget("string", "foreground"),
        }

        def apply():
            self.editor.config(
                bg=theme["bg"],
                fg=theme["fg"],
                insertbackground=theme["fg"]
            )

            self.controller.highlighter.update_colors({
                "keyword": theme["keyword"],
                "function": theme["function"],
                "comment": theme["comment"],
                "string": theme["string"]
            })

            self.controller.highlighter.highlight_all()
            self.line_nums.redraw()

        def pick(key):
            c = colorchooser.askcolor()[1]
            if c:
                theme[key] = c
                apply()

        tk.Label(popup, text="UI Colors").pack()
        tk.Button(popup, text="Background", command=lambda: pick("bg")).pack(fill="x")
        tk.Button(popup, text="Foreground", command=lambda: pick("fg")).pack(fill="x")

        tk.Label(popup, text="Syntax Colors").pack()

        for k in ["keyword", "function", "comment", "string"]:
            tk.Button(popup, text=f"{k}", command=lambda kk=k: pick(kk)).pack(fill="x")

        tk.Button(popup, text="Apply", bg="green", fg="white", command=apply).pack(fill="x")
