# Copilot Instructions for `lyr-pyvc`

## Build, test, and lint commands

This repository does not define a formal build, test, or lint pipeline (no `tests/`, no linter config, no npm scripts).

Use these verified project commands:

```powershell
# Run app with sample lyrics
python lyr.py sample_lyrics.txt

# Run app and choose a file from dialog
python lyr.py
```

For a quick single-file validation without launching the GUI:

```powershell
python -m py_compile lyr.py
```

## High-level architecture

The app is a single-file Tkinter desktop viewer:

- `main()` creates the Tk root, sets default window size, reads optional CLI path (`sys.argv[1]`), and instantiates `LyricViewer`.
- `LyricViewer` owns all UI widgets and playback state (`lines`, `index`, `file_path`).
- File ingestion happens in `load_file()`:
  - Validates file path.
  - Reads with UTF-8 and `errors="replace"`.
  - Preserves line content, stripping only line breaks via `rstrip("\r\n")`.
  - Resets index to `0` and updates text/status.
- Navigation happens in `next_line()`:
  - Enter / keypad Enter advances one line.
  - At end of file, shows a message and loops back to first line.
- `_update_status()` is the single formatter for the bottom status text.
- `_on_resize()` keeps long lyric lines readable by updating `wraplength`.

## Key conventions in this codebase

- UI text and labels are in Spanish; keep new user-facing strings consistent with this style.
- Keyboard-first flow is intentional:
  - `Enter` / `KP_Enter` for next line.
  - `Ctrl+O` for opening files.
- The display intentionally keeps spaces in lyric lines; only newline characters are removed.
- Status line format follows: `"<archivo> — Línea X/Y — Enter: siguiente"`.
- The script currently uses tab indentation; keep edits consistent within `lyr.py`.
- `README.md` is the source of truth for usage examples and should be updated when runtime behavior changes.
