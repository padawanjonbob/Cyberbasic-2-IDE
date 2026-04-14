import tkinter as tk
from tkinter import ttk, colorchooser
import pywinstyles

from cyberbasic_config import THEMES, FONT_FAMILY, FONT_SIZE


# =========================
# LINE NUMBERS
# =========================
class LineNumbers(tk.Canvas):
    def __init__(self, master, text):
        super().__init__(master, width=50, bg="#1e1e1e", highlightthickness=0)
        self.text = text

    def redraw(self):
        self.delete("all")

        if not self.text:
            return

        i = self.text.index("@0,0")

        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break

            y = dline[1]
            linenum = str(i).split(".")[0]

            self.create_text(
                45,
                y,
                text=linenum,
                anchor="ne",
                fill="gray",
                font=self.text["font"]
            )

            i = self.text.index(f"{i}+1line")


# =========================
# UI
# =========================
class CyberUI:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("CyberBasic 2 IDE")
        self.root.geometry("1400x900")

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
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Themes", menu=theme_menu)

        for name in THEMES:
            theme_menu.add_command(
                label=name,
                command=lambda n=name: controller.change_theme(n)
            )

        view_menu.add_separator()
        view_menu.add_command(label="Customize Colors", command=self.open_color_editor)

        # =========================
        # MAIN LAYOUT (RESIZABLE)
        # =========================
        main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=6)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # =========================
        # SIDEBAR (FILES)
        # =========================
        sidebar_frame = tk.Frame(main_pane, bg="#111")

        tk.Label(sidebar_frame, text="FILES", bg="#2d2d2d", fg="white").pack(fill=tk.X)

        self.sidebar = ttk.Treeview(sidebar_frame)
        self.sidebar.pack(fill=tk.BOTH, expand=True)

        self.sidebar.bind("<<TreeviewSelect>>", controller.files.on_file_select)

        main_pane.add(sidebar_frame, width=250)

        # =========================
        # RIGHT SIDE (EDITOR + DOCS)
        # =========================
        right_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL, sashwidth=6)
        main_pane.add(right_pane)

        # =========================
        # TOP (EDITOR + DOCS SPLIT)
        # =========================
        top_pane = tk.PanedWindow(right_pane, orient=tk.HORIZONTAL, sashwidth=6)
        right_pane.add(top_pane)

        # =========================
        # EDITOR PANEL
        # =========================
        editor_container = tk.Frame(top_pane, bg="#1e1e1e")

        tk.Label(editor_container, text="EDITOR", bg="#2d2d2d", fg="white").pack(fill=tk.X)

        editor_frame = tk.Frame(editor_container)
        editor_frame.pack(fill=tk.BOTH, expand=True)

        self.line_nums = LineNumbers(editor_frame, None)
        self.line_nums.pack(side=tk.LEFT, fill=tk.Y)

        self.editor = tk.Text(
            editor_frame,
            wrap="none",
            undo=True,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=(FONT_FAMILY, FONT_SIZE)
        )
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.line_nums.text = self.editor

        scrollbar = tk.Scrollbar(editor_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def on_scroll(*args):
            self.editor.yview(*args)
            self.line_nums.yview(*args)

        def on_text_scroll(*args):
            scrollbar.set(*args)
            self.line_nums.yview_moveto(args[0])
            self.line_nums.redraw()

        self.editor.config(yscrollcommand=on_text_scroll)
        scrollbar.config(command=on_scroll)

        self.editor.bind("<KeyRelease>", lambda e: self.line_nums.redraw())
        self.editor.bind("<MouseWheel>", lambda e: self.line_nums.redraw())

        # syntax colors
        self.editor.tag_configure("keyword", foreground="cyan")
        self.editor.tag_configure("function", foreground="yellow")
        self.editor.tag_configure("comment", foreground="green")
        self.editor.tag_configure("string", foreground="orange")

        top_pane.add(editor_container)

        # =========================
        # DOCS PANEL
        # =========================
        docs_container = tk.Frame(top_pane, bg="#020617")

        tk.Label(docs_container, text="DOCS", bg="#2d2d2d", fg="white").pack(fill=tk.X)

        # NAV BUTTONS
        nav = tk.Frame(docs_container, bg="#020617")
        nav.pack(fill=tk.X)

        tk.Button(nav, text="←", command=self.controller.docs.go_back).pack(side=tk.LEFT)
        tk.Button(nav, text="→", command=self.controller.docs.go_forward).pack(side=tk.LEFT)

        # SEARCH
        self.doc_search = tk.Entry(docs_container, bg="#020617")
        self.doc_search.pack(fill=tk.X)

        self.doc_search.insert(0, "search")
        self.doc_search.config(fg="gray")

        def clear(e):
            if self.doc_search.get() == "search":
                self.doc_search.delete(0, "end")
                self.doc_search.config(fg="white")

        def restore(e):
            if not self.doc_search.get():
                self.doc_search.insert(0, "search")
                self.doc_search.config(fg="gray")

        self.doc_search.bind("<FocusIn>", clear)
        self.doc_search.bind("<FocusOut>", restore)

        # RESULTS
        self.doc_results = tk.Listbox(docs_container, height=6)
        self.doc_results.pack(fill=tk.X)

        # DOC TEXT
        self.docs = tk.Text(
            docs_container,
            wrap="word",
            bg="#020617",
            fg="white",
            state="disabled"
        )
        self.docs.pack(fill=tk.BOTH, expand=True)

        top_pane.add(docs_container, width=400)

        # =========================
        # CONSOLE
        # =========================
        console_container = tk.Frame(right_pane, bg="black")

        tk.Label(console_container, text="CONSOLE", bg="#2d2d2d", fg="white").pack(fill=tk.X)

        self.console = tk.Text(
            console_container,
            height=10,
            bg="black",
            fg="green",
            font=(FONT_FAMILY, max(8, FONT_SIZE - 2))
        )
        self.console.pack(fill=tk.BOTH, expand=True)

        tk.Button(console_container, text="▶ Run", command=controller.run_code).pack(fill=tk.X)

        right_pane.add(console_container, height=200)

    # =========================
    # COLOR EDITOR
    # =========================
    def open_color_editor(self):
        popup = tk.Toplevel(self.root)
        popup.title("Color Editor")

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

            self.controller.highlighter.update_colors(theme)
            self.controller.highlighter.highlight_all()
            self.line_nums.redraw()

        def pick(key):
            c = colorchooser.askcolor()[1]
            if c:
                theme[key] = c
                apply()

        tk.Button(popup, text="Background", command=lambda: pick("bg")).pack(fill="x")
        tk.Button(popup, text="Foreground", command=lambda: pick("fg")).pack(fill="x")

        for k in ["keyword", "function", "comment", "string"]:
            tk.Button(popup, text=k, command=lambda kk=k: pick(kk)).pack(fill="x")

        tk.Button(popup, text="Apply", command=apply).pack(fill="x")
