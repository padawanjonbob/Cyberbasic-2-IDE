import subprocess
import threading


class Runner:
    def __init__(self, controller):
        self.app = controller
        self.proc = None

    @property
    def ui(self):
        return self.app.ui

    def run_code(self):
        if not self.app.file_path:
            return

        threading.Thread(target=self.execute, daemon=True).start()

    def execute(self):
        try:
            self.proc = subprocess.Popen(
                ["cyberbasic.exe", self.app.file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace"
            )

            for line in iter(self.proc.stdout.readline, ''):
                if not line:
                    break
                self.log(line)

            self.proc.wait()
            self.log(f"\nProcess exited with code {self.proc.returncode}\n")

        except Exception as e:
            self.log(str(e))

    def log(self, msg):
        self.ui.console.after(0, self._log_ui, msg)

    def _log_ui(self, msg):
        self.ui.console.config(state="normal")
        self.ui.console.insert("end", msg)
        self.ui.console.see("end")
        self.ui.console.config(state="disabled")
