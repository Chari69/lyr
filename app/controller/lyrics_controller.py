from tkinter import filedialog, messagebox

from app.model.lyrics_model import LyricsModel
from app.view.lyrics_view import LyricsView


class LyricsController:
	def __init__(self, model: LyricsModel, view: LyricsView):
		self.model = model
		self.view = view
		self.view.set_callbacks(
			on_open=self.open_file_dialog,
			on_next=self.next_line,
			on_font_change=self.apply_font_settings,
			on_animation_change=self.apply_animation_settings,
			on_style_change=self.apply_style_settings,
			on_import_font=self.open_font_dialog,
			on_about=self.open_about_dialog,
		)

	def start(self, initial_path: str | None = None) -> None:
		if initial_path:
			self.load_file(initial_path)
		else:
			self.view.set_text("Selecciona un archivo .txt o pasa uno por argumento", animated=False)
			self.view.set_status("Sin archivo cargado")

	def open_file_dialog(self, event=None) -> None:
		path = filedialog.askopenfilename(
			title="Selecciona archivo de líricas (.txt)",
			filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
		)
		if path:
			self.load_file(path)

	def load_file(self, path: str) -> None:
		try:
			self.model.load_from_path(path)
		except (FileNotFoundError, OSError) as error:
			messagebox.showerror("Error", str(error))
			return

		self.refresh_view(animated=False)

	def next_line(self, event=None) -> None:
		if not self.model.has_lines():
			self.open_file_dialog()
			return

		restarted = self.model.advance()
		if restarted:
			messagebox.showinfo("Fin", "Fin de la letra. Reiniciando al inicio.")

		self.refresh_view(animated=True)

	def refresh_view(self, animated: bool) -> None:
		self.view.set_text(self.model.current_line(), animated=animated)
		position, total = self.model.current_position()
		self.view.set_status(
			f"{self.model.current_filename()} — Línea {position}/{total} — Enter: siguiente"
		)

	def apply_font_settings(self, family: str, size: int) -> None:
		self.view.update_main_font(family, size)

	def apply_animation_settings(
		self,
		out_animation: str,
		out_duration_ms: int,
		in_animation: str,
		in_duration_ms: int,
	) -> None:
		self.view.update_animation_settings(
			out_animation=out_animation,
			out_duration_ms=out_duration_ms,
			in_animation=in_animation,
			in_duration_ms=in_duration_ms,
		)

	def apply_style_settings(
		self,
		text_color: str,
		border_color: str,
		border_width: int,
		background_color: str,
	) -> None:
		self.view.update_style_settings(
			text_color=text_color,
			border_color=border_color,
			border_width=border_width,
			background_color=background_color,
		)

	def open_font_dialog(self) -> None:
		path = filedialog.askopenfilename(
			title="Selecciona una fuente (.ttf/.otf)",
			filetypes=[("Font files", "*.ttf *.otf"), ("All files", "*.*")],
		)
		if not path:
			return

		try:
			family_name = self.view.register_custom_font(path)
		except OSError as error:
			messagebox.showerror("Error", f"No se pudo cargar la fuente:\n{error}")
			return

		if not family_name:
			messagebox.showwarning(
				"Fuente cargada",
				"La fuente se copió, pero no se detectó familia automáticamente. "
				"Si no aparece ahora, reinicia la app.",
			)
			return

		self.view.update_main_font(family_name, self.view.main_font_size)
		messagebox.showinfo("Fuente cargada", f"Fuente disponible: {family_name}")

	def open_about_dialog(self) -> None:
		messagebox.showinfo(
			"Acerca de",
			"Lyr\n\nCreado por @jdchari\nVersión 1.0.0",
		)
