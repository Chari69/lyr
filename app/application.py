import tkinter as tk

from app.controller.lyrics_controller import LyricsController
from app.model.lyrics_model import LyricsModel
from app.view.lyrics_view import LyricsView


def run_application(initial_path: str | None = None) -> None:
	root = tk.Tk()
	root.geometry("1024x600")

	model = LyricsModel()
	view = LyricsView(root)
	controller = LyricsController(model, view)
	controller.start(initial_path)

	root.mainloop()
