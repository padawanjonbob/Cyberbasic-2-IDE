import re
from cyberbasic_config import KEYWORDS, FUNCTIONS, COLORS


class CyberHighlighter:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.update_colors(COLORS)

        self.kw_regex = re.compile(r'\b(' + '|'.join(KEYWORDS) + r')\b', re.IGNORECASE)
        self.fn_regex = re.compile(r'\b(' + '|'.join(FUNCTIONS) + r')\b|\b[a-zA-Z_][a-zA-Z0-9_]*(?=\()')
        self.str_regex = re.compile(r'"[^"\\]*"')
        self.comment_regex = re.compile(r'(//|REM).*', re.IGNORECASE)

    def update_colors(self, palette):
        self.colors = palette

        self.text_widget.tag_configure("keyword", foreground=palette["keyword"])
        self.text_widget.tag_configure("function", foreground=palette["function"])
        self.text_widget.tag_configure("comment", foreground=palette["comment"])
        self.text_widget.tag_configure("string", foreground=palette["string"])

    def apply_line(self, line_number):
        start = f"{line_number}.0"
        end = f"{line_number}.end"

        text = self.text_widget.get(start, end)

        for tag in ["keyword", "function", "comment", "string"]:
            self.text_widget.tag_remove(tag, start, end)

        for m in self.str_regex.finditer(text):
            self.text_widget.tag_add("string", f"{line_number}.{m.start()}", f"{line_number}.{m.end()}")

        for m in self.comment_regex.finditer(text):
            self.text_widget.tag_add("comment", f"{line_number}.{m.start()}", f"{line_number}.{m.end()}")

        for m in self.kw_regex.finditer(text):
            self.text_widget.tag_add("keyword", f"{line_number}.{m.start()}", f"{line_number}.{m.end()}")

        for m in self.fn_regex.finditer(text):
            self.text_widget.tag_add("function", f"{line_number}.{m.start()}", f"{line_number}.{m.end()}")
