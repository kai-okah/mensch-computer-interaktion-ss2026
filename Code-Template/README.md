# Saccades, an Eye Movement Test

A small Tkinter app that shows a coloured circle at random positions on a fixed time
interval. It is meant to trigger and let you observe saccades, the fast jumps the
eye makes to bring a new target onto the fovea. You can film your eyes to record the 
corresponding eye movements.

This is the first exercise I committed for the course Mensch-Computer Interaction
(Human-Computer Interaction), SS 2026. More coursework will follow over time.

## Requirements

You need Python 3.13, though any recent Python 3 should be fine. Tkinter is also
required, and it already ships with the standard CPython installer, so it is not a
pip package. On most Linux distributions you install it separately, for example, with
`sudo apt install python3-tk`. Beyond that, the script needs no third party packages.

## Running

```bash
python saccades.py
```

The window opens maximised. Run it from inside the `Code-Template/` folder, or pass
the full path to the file.

## Usage

Click **Start Saccades**. A circle appears and jumps to a new random position every
0.75 seconds. Follow the circle with your eyes, and each jump is a saccade. 
Click **End Saccades** to stop. Clicking a circle directly also forces an early jump.

## How it works

The timed loop lives in `tick()`. It draws one circle, then uses Tkinter's
`after(750, ...)` to schedule itself again. Since `after` fires only once, this
self rescheduling is what creates the loop. `time.sleep` is deliberately avoided
because it would block Tkinter's single event loop and freeze the window.

For starting and stopping, a `self.running` flag is the source of truth, and the
button label simply mirrors it. Stopping calls `after_cancel()` on the saved timer
id to break the loop.

The canvas fills the screen because the window starts maximised and every container
level uses grid `weight` together with `sticky="nsew"`. This lets the targets span
the whole screen, and the circles keep following the canvas when the window is
resized.

## Known limitations

`root.state("zoomed")` only works on Windows, and on Linux or macOS it raises an
error. You can replace it with `root.attributes("-zoomed", True)` on Linux, or build
a `geometry()` call from `winfo_screenwidth()` and `winfo_screenheight()` for
something that works everywhere.

