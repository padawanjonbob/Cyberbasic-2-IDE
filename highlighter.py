import re


class CyberHighlighter:
    def __init__(self, text):
        self.text = text

        self.kw = re.compile(r"\b(IF|THEN|ELSE|FOR|WHILE|FUNCTION|RETURN|END)\b", re.I)
        self.comment = re.compile(r"//.*|REM.*", re.I)
        self.string = re.compile(r'"[^"]*"')
        self.func = re.compile(r"\b[A-Z_]+(?=\()", re.I)

    def update_colors(self, theme):
        self.text.tag_configure("keyword", foreground=theme["keyword"])
        self.text.tag_configure("function", foreground=theme["function"])
        self.text.tag_configure("comment", foreground=theme["comment"])
        self.text.tag_configure("string", foreground=theme["string"])

    def highlight_all(self):
        txt = self.text.get("1.0", "end-1c")

        for tag in ["keyword", "function", "comment", "string"]:
            self.text.tag_remove(tag, "1.0", "end")

        for m in self.string.finditer(txt):
            self.text.tag_add("string", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

        for m in self.comment.finditer(txt):
            self.text.tag_add("comment", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

        for m in self.kw.finditer(txt):
            self.text.tag_add("keyword", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

        for m in self.func.finditer(txt):
            self.text.tag_add("function", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
