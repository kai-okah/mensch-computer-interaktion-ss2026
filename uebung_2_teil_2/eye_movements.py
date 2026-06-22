import tkinter as tk
from tkinter import ttk

import saccadic
import vergence
import persuit


class _Controller:
    # Drives one eye-movement test on a canvas it does NOT own. It subclasses the
    # real app (for its tick/draw_* methods) but never runs that app's __init__, so
    # no widgets are built. Instead we inject the two widget capabilities the
    # inherited animation code actually uses: the shared canvas, and after/after_cancel.
    def __init__(self, canvas):
        self.canvas = canvas
        self.after = canvas.after                 # shadows Frame.after; used by tick()
        self.after_cancel = canvas.after_cancel
        self.running = False
        self.timer_id = None

    def start(self):
        self.running = True
        self.tick()                               # inherited from the real app class

    def stop(self):
        self.running = False
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)
            self.timer_id = None


class _Saccades(_Controller, saccadic.MyApp):
    # Inherits tick / draw_circle / random_circle_coordinates from saccadic.MyApp.
    def __init__(self, canvas):
        super().__init__(canvas)                  # -> _Controller.__init__ (no widgets)
        self.circle = None


class _Vergence(_Controller, vergence.MyApp):
    # Inherits tick / draw_dots / draw_dot from vergence.MyApp. The values below
    # mirror the non-widget state set in vergence.MyApp.__init__.
    def __init__(self, canvas):
        super().__init__(canvas)
        self.separation = 0
        self.min_separation = 0
        self.max_separation = 600
        self.step = 6
        self.diameter = 40
        self.closing = False


class _Pursuit(_Controller, persuit.MyApp):
    # Inherits tick / draw_dots / draw_dot from persuit.MyApp.
    def __init__(self, canvas):
        super().__init__(canvas)
        self.step = 6
        self.diameter = 40
        self.radius = self.diameter // 2
        self.circle_center = None
        self.move_right = True

    def start(self):
        # Re-centre on every start, the same thing persuit.toggle does (which we bypass).
        self.circle_center = self.canvas.winfo_width() // 2
        self.move_right = True
        super().start()


class Combined(ttk.Frame):

    DEFAULT_TEXT = "Test various eye movements."

    def __init__(self, root):
        super().__init__(root)
        self.root = root

        # weight = a grid cell is allowed to grow; sticky = the widget stretches to
        # fill its cell. Both are needed at every level for the canvas to fill the window.
        self.grid(column=0, row=0, sticky="nsew")
        self.root.title("Eye Movement Tests")
        self.configure(padding=(20, 10))
        # start maximized (Windows-only)
        self.root.state("zoomed")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.label = ttk.Label(self, text=self.DEFAULT_TEXT)
        self.label.grid(column=0, row=0)

        self.canvas = tk.Canvas(self, bg="white", width=1400, height=600)
        self.canvas.grid(column=0, row=1, sticky="nsew")

        # One controller per test, all sharing the single canvas above. Each entry is
        # (button label, controller, instruction text shown while it runs).
        self.tests = [
            ("Saccades", _Saccades(self.canvas),
             "Follow the circle with your eyes."),
            ("Convergence", _Vergence(self.canvas),
             "Keep the two dots fused into one as they move apart and back together."),
            ("Pursuit", _Pursuit(self.canvas),
             "Follow the dot with your eyes as it moves from one side to the next."),
        ]
        self.active = None
        self.buttons = {}

        bar = ttk.Frame(self)
        bar.grid(column=0, row=2)
        for col, (name, controller, text) in enumerate(self.tests):
            button = ttk.Button(bar, text=name,
                                command=lambda c=controller: self.select(c))
            button.grid(column=col, row=0, padx=6)
            self.buttons[controller] = (button, name, text)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)   # only the canvas row grows

    def select(self, controller):
        # Only one test runs at a time (one canvas). Clicking the running test stops
        # it; clicking another stops the current one first, then starts the new one.
        if self.active is controller:
            self._stop(controller)
        else:
            if self.active is not None:
                self._stop(self.active)
            self._start(controller)

    def _start(self, controller):
        controller.start()
        self.active = controller
        button, _name, text = self.buttons[controller]
        button.configure(text="Stop")
        self.label.configure(text=text)

    def _stop(self, controller):
        controller.stop()
        self.canvas.delete("all")
        if self.active is controller:
            self.active = None
        button, name, _text = self.buttons[controller]
        button.configure(text=name)
        self.label.configure(text=self.DEFAULT_TEXT)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = Combined(app_root)
    app_root.mainloop()
