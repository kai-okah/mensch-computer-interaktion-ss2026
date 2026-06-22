import tkinter as tk
from tkinter import ttk


class MyApp(ttk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.running = False
        self.timer_id = None

        # Two dots oscillate apart and back together; `closing` is the direction.
        self.separation = 0
        self.min_separation = 0
        self.max_separation = 600
        self.step = 6
        self.diameter = 40
        self.closing = False

        # weight = a grid cell is allowed to grow; sticky = the widget stretches to
        # fill its cell. Both are needed at every level for the canvas to fill the window.
        self.grid(column=0, row=0, sticky="nsew")
        self.root.title("Convergence - Eye Movement Test")
        self.configure(padding=(20, 10))
        # start maximized (Windows-only)
        self.root.state("zoomed")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.label = ttk.Label(
            self, text="Keep the two dots fused into one as they move apart and back together.")
        self.label.grid(column=0, row=0)

        self.canvas = tk.Canvas(self, bg="white", width=1400, height=600)
        self.canvas.grid(column=0, row=1, sticky="nsew")

        self.button = ttk.Button(
            self, text="Start Convergence", command=self.toggle)
        self.button.grid(column=0, row=2)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)   # only the canvas row grows

    def toggle(self):
        # Start or stop the convergence loop, and flip the button label to match.
        if self.running:
            self.running = False
            self.button.configure(text="Start Convergence")
            if self.timer_id is not None:
                self.after_cancel(self.timer_id)
                self.timer_id = None
        else:
            self.running = True
            self.button.configure(text="End Convergence")
            self.tick()

    def tick(self):
        # Step the separation toward its bound, reverse at the ends, then redraw.
        # after() (not time.sleep) keeps the loop going without freezing the window.
        if self.closing:
            self.separation -= self.step
            if self.separation <= self.min_separation:
                self.separation = self.min_separation
                self.closing = False
        else:
            self.separation += self.step
            # Turn back early if the window is too narrow to fit max_separation;
            # recomputed each tick so shrinking the window is handled.
            limit = min(self.max_separation,
                        self.canvas.winfo_width() - self.diameter)
            if self.separation >= limit:
                self.separation = limit
                self.closing = True

        self.draw_dots()
        self.timer_id = self.after(25, self.tick)

    def draw_dots(self):
        # Two dots straddle the midline, each separation/2 from center, so they
        # merge into one when the separation reaches 0.
        center_x = self.canvas.winfo_width() // 2
        center_y = self.canvas.winfo_height() // 2
        radius = self.diameter // 2
        offset = self.separation // 2

        self.canvas.delete("all")
        self.draw_dot(center_x - offset, center_y, radius, "red")
        self.draw_dot(center_x + offset, center_y, radius, "blue")

    def draw_dot(self, x, y, radius, color):
        self.canvas.create_oval(x - radius, y - radius,
                                x + radius, y + radius, fill=color)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = MyApp(app_root)
    app_root.mainloop()
