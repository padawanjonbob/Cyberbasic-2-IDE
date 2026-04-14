import subprocess
import threading


class Runner:
    def __init__(self, controller):
        self.app = controller

    @property
    def ui(self):
        return self.app.ui

    def run_code(self):
        if not self.app.file_path:
            return

        threading.Thread(target=self.execute, daemon=True).start()

    def execute(self):
        try:
            proc = subprocess.Popen(
                ["cyberbasic.exe", self.app.file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in proc.stdout:
                self.log(line)

        except Exception as e:
            self.log(str(e))

    def log(self, msg):
        self.ui.console.config(state="normal")
        self.ui.console.insert("end", msg)
        self.ui.console.see("end")
        self.ui.console.config(state="disabled")
