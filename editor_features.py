class EditorFeatures:
    def __init__(self, controller):
        self.app = controller
        self.text = None

    @property
    def ui(self):
        return self.app.ui

    def attach(self):
        self.text = self.ui.editor

        self.text.bind("<KeyRelease>", lambda e: self.update_ui())
        self.text.bind("<ButtonRelease>", lambda e: self.update_ui())

    def update_ui(self):
        self.highlight_line()
        self.ui.line_nums.redraw()

    def highlight_line(self):
        self.text.tag_remove("current_line", "1.0", "end")

        line = self.text.index("insert").split(".")[0]
        self.text.tag_add("current_line", f"{line}.0", f"{line}.end")
