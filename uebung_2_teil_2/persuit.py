import tkinter as tk
from tkinter import ttk


class MyApp(ttk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root = root

        self.running = False
        self.timer_id = None

        self.step = 6
        self.diameter = 40
        self.radius = self.diameter // 2
        self.circle_center = None
        self.move_right = True

        # weight = a grid cell is allowed to grow; sticky = the widget stretches to
        # fill its cell. Both are needed at every level for the canvas to fill the window.
        self.grid(column=0, row=0, sticky="nsew")
        self.root.title("Pursuit - Eye Movement Test")
        self.configure(padding=(20, 10))
        self.root.state("zoomed")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.label = ttk.Label(
            self, text="Follow the dot with your eyes as it moves from one side to the next.")
        self.label.grid(column=0, row=0)

        self.canvas = tk.Canvas(self, bg="white", width=1400, height=600)
        self.canvas.grid(column=0, row=1, sticky="nsew")

        self.button = ttk.Button(
            self, text="Start Pursuit", command=self.toggle)
        self.button.grid(column=0, row=2)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)   # only the canvas row grows

    def toggle(self):
        # Start or stop the pursuit loop, and flip the button label to match.
        if self.running:
            self.running = False
            self.button.configure(text="Start Pursuit")
            if self.timer_id is not None:
                self.after_cancel(self.timer_id)
                self.timer_id = None
        else:
            self.running = True
            self.button.configure(text="End Pursuit")
            self.circle_center = self.canvas.winfo_width() // 2   # re-centre on every start
            self.move_right = True
            self.tick()

    def tick(self):
        if self.circle_center > (self.canvas.winfo_width() - self.radius):
            self.circle_center = self.canvas.winfo_width() - self.radius
            self.move_right = False

        elif self.circle_center <= self.radius:
            self.circle_center = self.radius
            self.move_right = True

        if self.move_right:
            self.circle_center += self.step
        else:
            self.circle_center -= self.step

        self.draw_dots()
        self.timer_id = self.after(25, self.tick)

    def draw_dots(self):
        center_x = self.circle_center
        center_y = self.canvas.winfo_height() // 2

        self.canvas.delete("all")
        self.draw_dot(center_x, center_y, self.radius, "red")

    def draw_dot(self, x, y, radius, color):
        self.canvas.create_oval(x - radius, y - radius,
                                x + radius, y + radius, fill=color)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = MyApp(app_root)
    app_root.mainloop()
