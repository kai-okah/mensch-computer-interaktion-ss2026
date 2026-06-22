import tkinter as tk
from tkinter import ttk
import random as rnd


class MyApp(ttk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.circle = None
        self.running = False
        self.timer_id = None

        # weight = a grid cell is allowed to grow; sticky = the widget stretches to
        # fill its cell. Both are needed at every level for the canvas to fill the window.
        self.grid(column=0, row=0, sticky="nsew")
        self.root.title("Saccades - Eye Movement Test")
        self.configure(padding=(20, 10))

        self.root.state("zoomed")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.label = ttk.Label(self, text="Follow the circle with your eyes.")
        self.label.grid(column=0, row=0)

        self.canvas = tk.Canvas(self, bg="white", width=1400, height=600)
        self.canvas.grid(column=0, row=1, sticky="nsew")

        self.button = ttk.Button(
            self, text="Start Saccades", command=self.toggle)
        self.button.grid(column=0, row=2)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)   # only the canvas row grows

    def toggle(self):
        # Start or stop the saccade loop, and flip the button label to match.
        if self.running:
            self.running = False
            self.button.configure(text="Start Saccades")
            if self.timer_id is not None:
                self.after_cancel(self.timer_id)
                self.timer_id = None
        else:
            self.tick()
            self.running = True
            self.button.configure(text="End Saccades")

    def tick(self):
        # Draw a circle then queue the next one. after() (not time.sleep) keeps the
        # loop going without freezing the window. 750 ms is the interval; tune here.
        self.draw_circle()
        self.timer_id = self.after(750, self.tick)

    def draw_circle(self, event=None):
        # Place one circle at a random spot. Also bound to a click, so clicking the
        # circle forces an early jump.
        coordinates = self.random_circle_coordinates()
        colors = ["blue", "red"]
        self.canvas.delete("all")
        self.circle = self.canvas.create_oval(
            *coordinates, fill=rnd.choice(colors), tags=("c",))
        self.canvas.tag_bind("c", "<Button-1>", self.draw_circle)

    def random_circle_coordinates(self):
        # Pick a random position that fits inside the current canvas.
        max_x = self.canvas.winfo_width()
        max_y = self.canvas.winfo_height()
        diameter = 35
        radius = diameter // 2

        if max_x <= diameter or max_y <= diameter:   # window too small to place it
            return 0, 0, diameter, diameter

        x = rnd.randint(radius + 1, max_x - radius - 1)
        y = rnd.randint(radius + 1, max_y - radius - 1)
        return x - radius, y - radius, x + radius, y + radius


if __name__ == "__main__":
    app_root = tk.Tk()
    app = MyApp(app_root)
    app_root.mainloop()
