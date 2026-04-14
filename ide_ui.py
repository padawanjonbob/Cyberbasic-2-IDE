import tkinter as tk
from tkinter import ttk
import pywinstyles

from cyberbasic_config import COLORS, THEMES, FONT_FAMILY, FONT_SIZE


class LineNumbers(tk.Canvas):
    """Canvas for line numbers"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textwidget = None

    def redraw(self, *args):
        self.delete("all")

        if not self.textwidget:
            return

        i = self.textwidget.index("@0,0")

        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break

            y = dline[1]
            linenum = str(i).split(".")[0]

            self.create_text(
                38, y,
                anchor="ne",
                text=linenum,
                fill="#858585",
                font=(FONT_FAMILY, FONT_SIZE)
            )

            i = self.textwidget.index(f"{i}+1line")


class CyberUI:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("CyberBasic 2 IDE")
        self.root.geometry("1200x850")

        # Native Windows styling
        pywinstyles.apply_style(self.root, "dark")
        pywinstyles.change_header_color(self.root, color="#2d2d2d")

        # =========================
        # 📋 MENU BAR
        # =========================
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # --- FILE MENU ---
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=controller.new_file)
        self.file_menu.add_command(label="Open Folder", command=controller.open_folder)
        self.file_menu.add_command(label="Save", command=controller.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # --- RUN MENU ---
        self.run_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.run_menu.add_command(label="Run (F5)", command=controller.run_code)
        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)

        # --- VIEW MENU ---
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Themes submenu
        self.theme_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Themes", menu=self.theme_menu)

        for theme_name in THEMES.keys():
            self.theme_menu.add_command(
                label=theme_name,
                command=lambda t=theme_name: controller.change_theme(t)
            )

        # Font size submenu
        self.font_menu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Font Size", menu=self.font_menu)

        for size in [10, 11, 12, 14, 16, 18, 20, 24]:
            self.font_menu.add_command(
                label=str(size),
                command=lambda s=size: controller.change_font_size(s)
            )

        # 🎨 NEW: Color Editor
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label="Customize Colors",
            command=controller.open_color_editor
        )

        # =========================
        # 🧰 TOOLBAR
        # =========================
        self.toolbar = tk.Frame(self.root, bg="#2d2d2d", pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(
            self.toolbar,
            text="💾 Save",
            command=controller.save_file,
            bg="#3d3d3d",
            fg="white",
            relief=tk.FLAT,
            padx=12
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.toolbar,
            text="▶ Run",
            command=controller.run_code,
            bg="#28a745",
            fg="white",
            relief=tk.FLAT,
            padx=12
        ).pack(side=tk.LEFT, padx=5)

        # =========================
        # 🧱 MAIN LAYOUT
        # =========================
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#2d2d2d", sashwidth=4)
        self.paned.pack(fill=tk.BOTH, expand=True)

        # --- SIDEBAR ---
        self.sidebar_frame = tk.Frame(self.paned, bg="#252526")

        self.sidebar = ttk.Treeview(
            self.sidebar_frame,
            show="tree",
            selectmode="browse"
        )
        self.sidebar.pack(fill=tk.BOTH, expand=True)

        self.paned.add(self.sidebar_frame, width=220)

        # --- RIGHT SIDE ---
        self.right_frame = tk.Frame(self.paned, bg=COLORS["bg"])
        self.paned.add(self.right_frame)

        # =========================
        # ✏️ EDITOR AREA
        # =========================
        self.edit_container = tk.Frame(self.right_frame, bg=COLORS["bg"])
        self.edit_container.pack(fill=tk.BOTH, expand=True)

        # Line numbers
        self.line_nums = LineNumbers(
            self.edit_container,
            width=45,
            bg="#1e1e1e",
            bd=0,
            highlightthickness=0
        )
        self.line_nums.pack(side=tk.LEFT, fill=tk.Y)

        # Text editor
        self.editor = tk.Text(
            self.edit_container,
            undo=True,
            font=(FONT_FAMILY, FONT_SIZE),
            bg=COLORS["bg"],
            fg=COLORS["fg"],
            insertbackground="white",
            bd=0,
            padx=5
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.line_nums.textwidget = self.editor

        # =========================
        # 🖥️ CONSOLE
        # =========================
        self.console = tk.Text(
            self.right_frame,
            height=12,
            bg="black",
            fg="#00ff00",
            font=(FONT_FAMILY, 10),
            state='disabled',
            bd=0,
            padx=10
        )
        self.console.pack(fill=tk.X)
