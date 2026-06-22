# Eye Movement Tests

A small set of Tkinter apps that put a moving target on screen to trigger and let
you observe different kinds of eye movement. Each test animates a coloured shape on
a white canvas. You follow it with your eyes, and you can film your eyes to record
the corresponding eye movements.

This is part of the coursework for the course Mensch-Computer Interaction
(Human-Computer Interaction), SS 2026.

## The tests

- **Saccades** (`saccadic.py`). A single circle jumps to a new random position on a
  fixed interval. Each jump is a saccade, the fast flick the eye makes to bring a
  new target onto the fovea.
- **Convergence** (`vergence.py`). Two dots start fused at the centre, drift apart
  along the midline, then come back together. Keeping them fused as they separate is
  what exercises convergence and fusion.
- **Smooth pursuit** (`persuit.py`). One dot glides steadily from one side to the
  other and back. Tracking it smoothly, without your eyes jumping, is smooth pursuit.
- **Combined launcher** (`eye_movements.py`). Runs any one of the three tests in a
  single window, with a button for each and a label that tells you what is running.

## Requirements

You need Python 3.13, though any recent Python 3 should be fine. The tests use only
Tkinter, which already ships with the standard CPython installer, so it is not a pip
package. On most Linux distributions you install it separately, for example with
`sudo apt install python3-tk`. Nothing else is required.

## Running

Run any single test directly:

```bash
python saccadic.py
python vergence.py
python persuit.py
```

The combined launcher imports the other three as siblings, so run it from inside
this folder:

```bash
python eye_movements.py
```

Every window opens maximised.

## Usage

Each single test has one button that both starts and stops it. Click **Start ...**
and the target begins moving, and the button then reads **End ...**. Click it again
to stop. In the saccades test you can also click the circle directly to force an
early jump.

The combined launcher shows three buttons instead. Click one to start that test. Its
button changes to **Stop** while it runs, and the others stay idle, since only one
test can run at a time on the shared canvas. Click **Stop**, or pick a different
test, to switch.

## How it works

The animation in every test lives in a `tick()` method. It updates the target, then
uses Tkinter's `after(ms, ...)` to schedule itself again. Since `after` fires only
once, this self rescheduling is what creates the loop. `time.sleep` is deliberately
avoided because it would block Tkinter's single event loop and freeze the window.

A `self.running` flag is the source of truth for whether a test is going, and the
button label simply mirrors it. Stopping calls `after_cancel()` on the saved timer
id to break the loop.

The canvas fills the screen because the window starts maximised and every container
level uses grid `weight` together with `sticky="nsew"`. The target geometry is
recomputed from the live canvas size on every tick, so resizing the window keeps
working.

The combined launcher reuses the three tests without copying their animation. Each
test gets a thin controller that inherits the real app's `tick` and drawing methods
but skips the widget building constructor, so all three can share the one canvas.

## Known limitations

`root.state("zoomed")` only works on Windows, and on Linux or macOS it raises an
error. You can replace it with `root.attributes("-zoomed", True)` on Linux, or build
a `geometry()` call from `winfo_screenwidth()` and `winfo_screenheight()` for
something that works everywhere.
