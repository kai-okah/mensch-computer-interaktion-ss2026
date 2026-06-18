# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Coursework for the university course *Mensch-Computer Interaktion* (Human-Computer Interaction), SS 2026. It is a collection of standalone Python practice scripts, not a single application. Each `.py` file is independent and runnable on its own.

## Environment

- Python 3.13 (CPython), virtualenv at `.venv/` (Windows layout: `.venv/Scripts/`).
- Activate: `.venv\Scripts\activate` (cmd/bat) or `.venv\Scripts\activate.ps1` (PowerShell).
- Installed packages include pandas 3.0, numpy 2.4, matplotlib 3.10. Only `Code-Template/requirements.txt` (`pandas`) is declared — the rest are present in the venv but undeclared, so add imports to `requirements.txt` when introducing new dependencies.
- GUI scripts use **Tkinter**, which ships with the system Python — it is not a pip package and is not in the venv site-packages.

## Running

```bash
# Any script runs directly; no build step.
python mosh.py
python Code-Template/saccades.py    # Tkinter window — needs a display
```

Tkinter scripts (`Code-Template/saccades.py`) open a window and block on `mainloop()`; they cannot be verified headlessly.

## Conventions

Tkinter apps follow a consistent pattern worth matching in new GUI scripts:
- Subclass `ttk.Frame` as `MyApp`, take `root` in `__init__`, call `super().__init__(root)` then `self.grid(...)`.
- Lay widgets out with `.grid()` (not `.pack()`).
- Canvas drawing clears with `self.canvas.delete("all")` before redrawing; interactive shapes are given `tags` and wired with `self.canvas.tag_bind(...)`.
- Standard entry point: `app_root = tk.Tk(); app = MyApp(app_root); app_root.mainloop()` under `if __name__ == "__main__":`.

## Notes

- Under git version control. Tracked so far: `Code-Template/saccades.py` and `Code-Template/README.md` (initial commit). The `.venv/`, sample data, and generated output are untracked.
- `Code-Template/` holds the working exercises plus sample data (`iris_dataset.csv`, `data.csv`, both the standard Iris schema) and `scatter.png` (generated matplotlib output).
- `Code-Template/saccades.py` is the worked saccades exercise: a Tkinter target that jumps to random positions on an `after()` timer with a single start/stop toggle button, run in a maximized window. `Code-Template/README.md` documents it.
