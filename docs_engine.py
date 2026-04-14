import os
import re

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


class DocsEngine:
    def __init__(self, controller):
        self.app = controller
        self.ui = None

        self.root = None
        self.index = []
        self.current_file = None

        # history: (path, scroll_position)
        self.history = []
        self.history_index = -1
        self._nav_lock = False

    # =========================
    # ATTACH UI
    # =========================
    def attach_ui(self, ui):
        self.ui = ui
        self.ui.doc_search.bind("<KeyRelease>", self.search)
        self.ui.doc_results.bind("<<ListboxSelect>>", self.open_result)

    # =========================
    # LOAD DOCS
    # =========================
    def load_folder(self, folder):
        self.root = folder
        self.index.clear()

        for file in os.listdir(folder):
            if file.endswith(".md"):
                path = os.path.join(folder, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                except:
                    continue

                self.index.append((file, content.lower()))

        if self.index:
            self.open_file(self.index[0][0])

    # =========================
    # PATH RESOLUTION
    # =========================
    def resolve_path(self, filename):
        if not filename:
            return None

        path = os.path.join(self.root, filename)

        if not os.path.exists(path):
            parent = os.path.dirname(self.root)
            path = os.path.join(parent, filename.replace("../", ""))

        if not os.path.exists(path):
            path = os.path.join(self.root, os.path.basename(filename))

        return path

    # =========================
    # SCROLL HELPERS
    # =========================
    def get_scroll(self):
        if not self.ui:
            return 0.0
        return self.ui.docs.yview()[0]

    # =========================
    # OPEN FILE
    # =========================
    def open_file(self, link):
        if not self.root or not self.ui:
            return

        # split file + anchor
        if "#" in link:
            filename, anchor = link.split("#", 1)
        else:
            filename, anchor = link, None

        # same-file anchor (no reload, no history)
        if not filename and self.current_file:
            if anchor:
                self.scroll_to_anchor(anchor)
            return

        path = self.resolve_path(filename)

        if not path or not os.path.exists(path):
            self.render(f"[Missing file: {link}]")
            return

        # update current scroll before leaving page
        if not self._nav_lock:
            if self.history and self.history_index >= 0:
                current_path, _ = self.history[self.history_index]
                self.history[self.history_index] = (current_path, self.get_scroll())

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return

        self.current_file = path
        self.render(content)

        # anchor scroll AFTER render
        if anchor:
            self.scroll_to_anchor(anchor)

        # add to history (page only)
        if not self._nav_lock:
            entry = (path, 0.0)

            if not self.history or self.history[-1][0] != path:
                self.history.append(entry)
                self.history_index = len(self.history) - 1

    # =========================
    # HISTORY NAV
    # =========================
    def go_back(self):
        if self.history_index <= 0:
            return

        # save current scroll
        path, _ = self.history[self.history_index]
        self.history[self.history_index] = (path, self.get_scroll())

        self.history_index -= 1
        path, scroll = self.history[self.history_index]

        self._nav_lock = True
        self._open_from_history(path, scroll)
        self._nav_lock = False

    def go_forward(self):
        if self.history_index >= len(self.history) - 1:
            return

        # save current scroll
        path, _ = self.history[self.history_index]
        self.history[self.history_index] = (path, self.get_scroll())

        self.history_index += 1
        path, scroll = self.history[self.history_index]

        self._nav_lock = True
        self._open_from_history(path, scroll)
        self._nav_lock = False

    def _open_from_history(self, path, scroll):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return

        self.current_file = path
        self.render(content)

        if scroll is not None:
            self.ui.docs.yview_moveto(scroll)

    # =========================
    # RENDER
    # =========================
    def render(self, content):
        w = self.ui.docs
        w.config(state="normal")
        w.delete("1.0", "end")

        pos = 0

        for m in LINK_PATTERN.finditer(content):
            start, end = m.span()
            text, link = m.groups()

            w.insert("end", content[pos:start])

            tag = f"link_{start}"
            w.insert("end", text, tag)

            w.tag_config(tag, foreground="cyan", underline=True)

            def click(e, link=link):
                self.open_file(link)

            w.tag_bind(tag, "<Button-1>", click)

            pos = end

        w.insert("end", content[pos:])
        w.config(state="disabled")

        # reapply search highlight
        q = self.ui.doc_search.get().lower()
        if q and q != "search":
            self.highlight_in_doc(q)

    # =========================
    # ANCHOR SCROLL + HIGHLIGHT
    # =========================
    def scroll_to_anchor(self, anchor):
        text = self.ui.docs

        def normalize(s):
            return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

        anchor = anchor.strip().lower()

        lines = text.get("1.0", "end").splitlines()

        for i, line in enumerate(lines):
            line_clean = line.strip()

            if line_clean.startswith("#"):
                header = line_clean.lstrip("#").strip()

                if normalize(header) == anchor:
                    index = f"{i+1}.0"

                    text.see(index)
                    text.yview_scroll(-2, "units")

                    # highlight header
                    start = index
                    end = f"{i+1}.end"

                    text.tag_remove("anchor_highlight", "1.0", "end")
                    text.tag_add("anchor_highlight", start, end)

                    text.tag_config(
                        "anchor_highlight",
                        background="#264f78",
                        foreground="white"
                    )

                    text.after(
                        1200,
                        lambda: text.tag_remove("anchor_highlight", "1.0", "end")
                    )

                    return

    # =========================
    # SEARCH
    # =========================
    def search(self, event=None):
        q = self.ui.doc_search.get().lower()

        if q == "search" or not q:
            return

        self.ui.doc_results.delete(0, "end")

        for name, content in self.index:
            if q in name.lower() or q in content:
                self.ui.doc_results.insert("end", name)

        self.highlight_in_doc(q)

    # =========================
    # SEARCH HIGHLIGHT
    # =========================
    def highlight_in_doc(self, query):
        text = self.ui.docs

        text.tag_remove("search_highlight", "1.0", "end")

        if not query:
            return

        content = text.get("1.0", "end").lower()
        start = 0

        while True:
            idx = content.find(query, start)
            if idx == -1:
                break

            start_index = f"1.0+{idx}c"
            end_index = f"1.0+{idx + len(query)}c"

            text.tag_add("search_highlight", start_index, end_index)

            start = idx + len(query)

        text.tag_config("search_highlight", background="yellow", foreground="black")

    # =========================
    # RESULT CLICK
    # =========================
    def open_result(self, event):
        sel = self.ui.doc_results.curselection()
        if not sel:
            return

        filename = self.ui.doc_results.get(sel[0])
        self.open_file(filename)
