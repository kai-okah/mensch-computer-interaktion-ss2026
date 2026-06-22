# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Coursework for the university course *Mensch-Computer Interaktion* (Human-Computer Interaction), SS 2026. It is a collection of standalone Python practice scripts, not a single application. Each `.py` file is independent and runnable on its own.

## Environment

- Python 3.13 (CPython), virtualenv at `.venv/` (Windows layout: `.venv/Scripts/`).
- Activate: `.venv\Scripts\activate` (cmd/bat) or `.venv\Scripts\activate.ps1` (PowerShell).
- `Code-Template/requirements.txt` declares the data/plotting dependencies (`pandas~=3.0.3`, `numpy~=2.4.6`, `matplotlib~=3.10.9`), matching the venv. Add imports to `requirements.txt` when introducing new dependencies. The Tkinter scripts need nothing here — Tkinter is stdlib.
- GUI scripts use **Tkinter**, which ships with the system Python — it is not a pip package and is not in the venv site-packages.

## Running

```bash
# Any script runs directly; no build step.
python mosh.py
python Code-Template/saccadic.py    # Tkinter window — needs a display
```

Tkinter scripts (`saccadic.py`, `vergence.py`, `persuit.py`) open a window and block on `mainloop()`; they cannot be verified headlessly. Non-GUI scripts (`mosh.py`, and any pandas/matplotlib data exercises) run to completion and *can* be verified headlessly — matplotlib scripts here write a file (e.g. `scatter.png`) rather than opening a window.

## Conventions

Tkinter apps follow a consistent pattern worth matching in new GUI scripts:
- Subclass `ttk.Frame` as `MyApp`, take `root` in `__init__`, call `super().__init__(root)` then `self.grid(...)`.
- Lay widgets out with `.grid()` (not `.pack()`).
- Canvas drawing clears with `self.canvas.delete("all")` before redrawing; interactive shapes are given `tags` and wired with `self.canvas.tag_bind(...)`.
- Animation is driven by a self-rescheduling `self.after(ms, ...)` loop (never `time.sleep`, which freezes the event loop). A `self.running` flag is the source of truth; a single toggle button starts/stops the loop and mirrors its label; stopping calls `after_cancel(self.timer_id)`. The loop method is conventionally named `tick()` (`persuit.py` names it `move()`).
- Recompute geometry from `self.canvas.winfo_width()`/`winfo_height()` inside the loop (not once at startup) so resizing the window is handled live.
- Standard entry point: `app_root = tk.Tk(); app = MyApp(app_root); app_root.mainloop()` under `if __name__ == "__main__":`.

## Notes

- Under git version control. The eye-movement scripts were renamed during the rework: the committed `saccades.py`/`convergence.py` are superseded by `saccadic.py`/`vergence.py` (plus the new `persuit.py`), which are not yet committed. The `.venv/`, sample data, and generated output are untracked.
- `Code-Template/` holds the working exercises plus sample data (`iris_dataset.csv`, `data.csv`, both the standard Iris schema) and `scatter.png` (generated matplotlib output).
- The three Tkinter eye-movement tests share the structure above and differ only in stimulus motion: `saccadic.py` jumps a circle to random positions (saccades), `vergence.py` moves two dots apart and back together along the midline (convergence/fusion), and `persuit.py` sweeps one dot left-to-right and back (smooth pursuit). `Code-Template/README.md` documents the saccades exercise.
- `mosh.py` is a smaller standalone exercise (plain Python, no GUI).
