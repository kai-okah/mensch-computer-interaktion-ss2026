# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Coursework for the university course _Mensch-Computer Interaktion_ (Human-Computer Interaction), SS 2026. It is a collection of standalone Python practice scripts, not a single application. Each `.py` file is independent and runnable on its own.

## Environment

- Python 3.13 (CPython), virtualenv at `.venv/` (Windows layout: `.venv/Scripts/`).
- Activate: `.venv\Scripts\activate` (cmd/bat) or `.venv\Scripts\activate.ps1` (PowerShell).
- `uebung_2_teil_2/requirements.txt` declares data/plotting dependencies (`pandas~=3.0.3`, `numpy~=2.4.6`, `matplotlib~=3.10.9`) that match the venv but are left over from earlier data exercises — nothing currently in the repo imports them. Add imports to `requirements.txt` when introducing new dependencies. The Tkinter scripts need nothing here — Tkinter is stdlib.
- GUI scripts use **Tkinter**, which ships with the system Python — it is not a pip package and is not in the venv site-packages.

## Running

```bash
# Any script runs directly; no build step.
python uebung_2_teil_2/saccadic.py    # Tkinter window — needs a display
```

All current scripts (`saccadic.py`, `vergence.py`, `persuit.py`, `eye_movements.py`) are Tkinter: they open a window and block on `mainloop()`, so none can be verified headlessly. There are no non-GUI scripts left in the project at the moment.

## Conventions

Tkinter apps follow a consistent pattern worth matching in new GUI scripts:

- Subclass `ttk.Frame` as `MyApp`, take `root` in `__init__`, call `super().__init__(root)` then `self.grid(...)`.
- Lay widgets out with `.grid()` (not `.pack()`).
- Canvas drawing clears with `self.canvas.delete("all")` before redrawing; interactive shapes are given `tags` and wired with `self.canvas.tag_bind(...)`.
- Animation is driven by a self-rescheduling `self.after(ms, ...)` loop (never `time.sleep`, which freezes the event loop). A `self.running` flag is the source of truth; a single toggle button starts/stops the loop and mirrors its label; stopping calls `after_cancel(self.timer_id)`. The loop method is conventionally named `tick()`.
- Recompute geometry from `self.canvas.winfo_width()`/`winfo_height()` inside the loop (not once at startup) so resizing the window is handled live.
- Standard entry point: `app_root = tk.Tk(); app = MyApp(app_root); app_root.mainloop()` under `if __name__ == "__main__":`.

## Notes

- Under git version control, with a remote at `github.com/kai-okah/mensch-computer-interaktion-ss2026`. The eye-movement exercise lives in `uebung_2_teil_2/` (Übung 2, Teil 2); `.venv/` and editor folders are gitignored or untracked.
- `uebung_2_teil_2/` holds the four eye-movement scripts plus `requirements.txt` and `README.md`. The earlier sample data (`iris_dataset.csv`, `data.csv`), the generated `scatter.png`, and the standalone `mosh.py` exercise are no longer in the project.
- Three of the scripts are standalone Tkinter eye-movement tests that share the structure above and differ only in stimulus motion: `saccadic.py` jumps a circle to random positions (saccades), `vergence.py` moves two dots apart and back together along the midline (convergence/fusion), and `persuit.py` sweeps one dot left-to-right and back (smooth pursuit). `uebung_2_teil_2/README.md` documents all of them.
- `eye_movements.py` is a combined launcher: it imports the three tests unchanged and runs any one of them (only one at a time) on a single shared canvas, with three bottom buttons and a top label that reflects what is running. It reuses each app's animation via thin `_Controller` subclasses that inherit the `tick`/`draw_*` methods but skip the widget-building `__init__` (the canvas and `after` are injected). Run it from inside `uebung_2_teil_2/` so the sibling imports resolve.
