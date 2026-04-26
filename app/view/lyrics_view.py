import shutil
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser
from tkinter import font as tkfont


class LyricsView:
	def __init__(self, root: tk.Tk):
		self.root = root
		self.root.title("Lyr - Presiona Enter para avanzar")

		self.bg_color = "#2ecc71"
		self.base_text_color = "#ffffff"
		self.border_color = "#103f1f"
		self.status_fg = "#103f1f"
		self.border_width = 0

		self._animation_job: str | None = None
		self._active_animation_id = 0
		self._font_options: list[str] = []
		self._current_text = ""
		self._stroke_items: list[int] = []
		self._main_item: int | None = None

		self.main_font_family = "Segoe UI"
		self.main_font_size = 28
		self.main_font_weight = "bold"

		self.animation_options = ["none", "fade", "zoom", "tiktok"]
		self.out_animation_var = tk.StringVar(value="fade")
		self.in_animation_var = tk.StringVar(value="fade")
		self.out_duration_var = tk.IntVar(value=180)
		self.in_duration_var = tk.IntVar(value=180)

		self.text_color_var = tk.StringVar(value=self.base_text_color)
		self.border_color_var = tk.StringVar(value=self.border_color)
		self.bg_color_var = tk.StringVar(value=self.bg_color)
		self.border_width_var = tk.IntVar(value=self.border_width)

		self.root.configure(bg=self.bg_color)
		self.container = tk.Frame(self.root, bg=self.bg_color)
		self.container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

		self.controls = tk.Frame(self.container, bg=self.bg_color)
		self.controls.pack(fill=tk.X, pady=(0, 10))

		self._build_font_controls()
		self._build_animation_controls()
		self._build_style_controls()

		self.display_area = tk.Frame(self.container, bg=self.bg_color)
		self.display_area.pack(fill=tk.BOTH, expand=True)

		self.canvas = tk.Canvas(
			self.display_area,
			bg=self.bg_color,
			highlightthickness=0,
			bd=0,
		)
		self.canvas.pack(fill=tk.BOTH, expand=True)

		self.status_var = tk.StringVar(value="Sin archivo cargado")
		self.status = tk.Label(
			self.container,
			textvariable=self.status_var,
			bg=self.bg_color,
			fg=self.status_fg,
			font=("Segoe UI", 12),
			anchor="w",
		)
		self.status.pack(fill=tk.X, pady=(10, 0))

		self._build_menus()
		self._load_font_options()
		self._render_text()

		self.root.bind("<Configure>", self.on_resize)
		self.canvas.bind("<Configure>", self.on_resize)

	def _build_font_controls(self) -> None:
		self.font_label = tk.Label(self.controls, text="Fuente:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.font_label.pack(side=tk.LEFT)

		self.font_var = tk.StringVar(value=self.main_font_family)
		self.font_menu = tk.OptionMenu(self.controls, self.font_var, self.main_font_family)
		self.font_menu.configure(bg=self.bg_color, fg=self.status_fg, highlightthickness=0)
		self.font_menu["menu"].configure(bg="white")
		self.font_menu.pack(side=tk.LEFT, padx=(6, 8))

		self.size_label = tk.Label(self.controls, text="Tamaño:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.size_label.pack(side=tk.LEFT)

		self.size_var = tk.IntVar(value=self.main_font_size)
		self.size_spin = tk.Spinbox(self.controls, from_=14, to=96, width=5, textvariable=self.size_var)
		self.size_spin.pack(side=tk.LEFT, padx=(6, 10))

		self.import_font_button = tk.Button(self.controls, text="Importar fuente")
		self.import_font_button.pack(side=tk.LEFT, padx=(0, 8))

		self.apply_font_button = tk.Button(self.controls, text="Aplicar fuente")
		self.apply_font_button.pack(side=tk.LEFT, padx=(0, 16))

	def _build_animation_controls(self) -> None:
		self.out_anim_label = tk.Label(self.controls, text="Salida:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.out_anim_label.pack(side=tk.LEFT)

		self.out_anim_menu = tk.OptionMenu(self.controls, self.out_animation_var, *self.animation_options)
		self.out_anim_menu.configure(bg=self.bg_color, fg=self.status_fg, highlightthickness=0)
		self.out_anim_menu["menu"].configure(bg="white")
		self.out_anim_menu.pack(side=tk.LEFT, padx=(6, 6))

		self.out_dur_label = tk.Label(self.controls, text="ms:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.out_dur_label.pack(side=tk.LEFT)

		self.out_dur_spin = tk.Spinbox(self.controls, from_=0, to=2000, increment=10, width=6, textvariable=self.out_duration_var)
		self.out_dur_spin.pack(side=tk.LEFT, padx=(4, 12))

		self.in_anim_label = tk.Label(self.controls, text="Entrada:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.in_anim_label.pack(side=tk.LEFT)

		self.in_anim_menu = tk.OptionMenu(self.controls, self.in_animation_var, *self.animation_options)
		self.in_anim_menu.configure(bg=self.bg_color, fg=self.status_fg, highlightthickness=0)
		self.in_anim_menu["menu"].configure(bg="white")
		self.in_anim_menu.pack(side=tk.LEFT, padx=(6, 6))

		self.in_dur_label = tk.Label(self.controls, text="ms:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.in_dur_label.pack(side=tk.LEFT)

		self.in_dur_spin = tk.Spinbox(self.controls, from_=0, to=2000, increment=10, width=6, textvariable=self.in_duration_var)
		self.in_dur_spin.pack(side=tk.LEFT, padx=(4, 8))

		self.apply_anim_button = tk.Button(self.controls, text="Aplicar animación")
		self.apply_anim_button.pack(side=tk.LEFT)

	def _build_style_controls(self) -> None:
		self.style_controls = tk.Frame(self.container, bg=self.bg_color)
		self.style_controls.pack(fill=tk.X, pady=(0, 10))

		self.text_color_button = tk.Button(self.style_controls, text="Color texto")
		self.text_color_button.pack(side=tk.LEFT, padx=(0, 6))

		self.border_color_button = tk.Button(self.style_controls, text="Color borde")
		self.border_color_button.pack(side=tk.LEFT, padx=(0, 6))

		self.bg_color_button = tk.Button(self.style_controls, text="Color fondo")
		self.bg_color_button.pack(side=tk.LEFT, padx=(0, 12))

		self.border_width_label = tk.Label(self.style_controls, text="Borde:", bg=self.bg_color, fg=self.status_fg, font=("Segoe UI", 10, "bold"))
		self.border_width_label.pack(side=tk.LEFT)

		self.border_width_spin = tk.Spinbox(self.style_controls, from_=0, to=8, width=4, textvariable=self.border_width_var)
		self.border_width_spin.pack(side=tk.LEFT, padx=(6, 10))

		self.apply_style_button = tk.Button(self.style_controls, text="Aplicar estilo")
		self.apply_style_button.pack(side=tk.LEFT)

	def _build_menus(self) -> None:
		self.menubar = tk.Menu(self.root)
		self.file_menu = tk.Menu(self.menubar, tearoff=0)
		self.file_menu.add_command(label="Abrir...", accelerator="Ctrl+O")
		self.file_menu.add_separator()
		self.file_menu.add_command(label="Salir", command=self.root.quit)
		self.menubar.add_cascade(label="Archivo", menu=self.file_menu)

		self.help_menu = tk.Menu(self.menubar, tearoff=0)
		self.help_menu.add_command(label="Acerca de")
		self.menubar.add_cascade(label="Ayuda", menu=self.help_menu)
		self.root.config(menu=self.menubar)

	def _load_font_options(self) -> None:
		families = sorted(set(tkfont.families()))
		preferred = ["Segoe UI", "Arial", "Calibri", "Verdana", "Tahoma", "Times New Roman", "Courier New"]
		filtered = [name for name in preferred if name in families]
		extras = [name for name in families if name not in filtered][:30]
		options = filtered + extras
		if not options:
			options = [self.main_font_family]
		if self.main_font_family not in options:
			options.insert(0, self.main_font_family)
		self._font_options = options
		self._refresh_font_menu()

	def _refresh_font_menu(self) -> None:
		menu = self.font_menu["menu"]
		menu.delete(0, "end")
		for option in self._font_options:
			menu.add_command(label=option, command=tk._setit(self.font_var, option))

	def register_custom_font(self, font_path: str) -> str | None:
		font_dir = Path.cwd() / "app" / "assets" / "fonts"
		font_dir.mkdir(parents=True, exist_ok=True)
		source = Path(font_path)
		target = font_dir / source.name
		if source.resolve() != target.resolve():
			shutil.copy2(source, target)

		self._load_font_options()
		candidates = [name for name in tkfont.families() if source.stem.lower() in name.lower()]
		family = candidates[0] if candidates else None
		if family and family not in self._font_options:
			self._font_options.insert(0, family)
			self._refresh_font_menu()
		if family:
			self.font_var.set(family)
		return family

	def set_callbacks(self, on_open, on_next, on_font_change, on_animation_change, on_style_change, on_import_font, on_about) -> None:
		self.root.bind("<Return>", on_next)
		self.root.bind("<KP_Enter>", on_next)
		self.root.bind("<Control-o>", on_open)

		self.file_menu.entryconfigure("Abrir...", command=on_open)
		self.help_menu.entryconfigure("Acerca de", command=on_about)
		self.apply_font_button.configure(command=lambda: on_font_change(self.font_var.get(), self.size_var.get()))
		self.import_font_button.configure(command=on_import_font)

		self.apply_anim_button.configure(
			command=lambda: on_animation_change(
				self.out_animation_var.get(),
				self.out_duration_var.get(),
				self.in_animation_var.get(),
				self.in_duration_var.get(),
			)
		)

		self.text_color_button.configure(command=lambda: self._pick_color("text"))
		self.border_color_button.configure(command=lambda: self._pick_color("border"))
		self.bg_color_button.configure(command=lambda: self._pick_color("bg"))
		self.apply_style_button.configure(
			command=lambda: on_style_change(
				self.text_color_var.get(),
				self.border_color_var.get(),
				self.border_width_var.get(),
				self.bg_color_var.get(),
			)
		)

	def _pick_color(self, target: str) -> None:
		initial = {"text": self.text_color_var.get(), "border": self.border_color_var.get(), "bg": self.bg_color_var.get()}[target]
		result = colorchooser.askcolor(color=initial, title="Selecciona color")
		if not result or not result[1]:
			return
		chosen = result[1]
		if target == "text":
			self.text_color_var.set(chosen)
		elif target == "border":
			self.border_color_var.set(chosen)
		else:
			self.bg_color_var.set(chosen)

	def on_resize(self, event) -> None:
		self._render_text()

	def set_text(self, text: str, animated: bool) -> None:
		self._active_animation_id += 1
		animation_id = self._active_animation_id
		if self._animation_job:
			self.root.after_cancel(self._animation_job)
			self._animation_job = None

		if not animated:
			self._current_text = text
			self._render_text()
			return

		self._animate_text(text, animation_id)

	def _animate_text(self, new_text: str, animation_id: int) -> None:
		out_sequence = self._build_animation_sequence(self.out_animation_var.get(), self._safe_duration(self.out_duration_var.get()), is_in=False)
		in_sequence = self._build_animation_sequence(self.in_animation_var.get(), self._safe_duration(self.in_duration_var.get()), is_in=True)
		self._run_out_sequence(out_sequence, 0, new_text, in_sequence, animation_id)

	def _run_out_sequence(self, sequence: list[dict], index: int, new_text: str, in_sequence: list[dict], animation_id: int) -> None:
		if animation_id != self._active_animation_id:
			return
		if index >= len(sequence):
			self._current_text = new_text
			self._render_text()
			self._run_in_sequence(in_sequence, 0, animation_id)
			return

		frame = sequence[index]
		self._apply_frame(frame)
		self._animation_job = self.root.after(frame["delay"], lambda: self._run_out_sequence(sequence, index + 1, new_text, in_sequence, animation_id))

	def _run_in_sequence(self, sequence: list[dict], index: int, animation_id: int) -> None:
		if animation_id != self._active_animation_id:
			return
		if index >= len(sequence):
			self._animation_job = None
			self._render_text()
			return

		frame = sequence[index]
		self._apply_frame(frame)
		self._animation_job = self.root.after(frame["delay"], lambda: self._run_in_sequence(sequence, index + 1, animation_id))

	def _apply_frame(self, frame: dict) -> None:
		color = frame.get("fg", self.base_text_color)
		stroke_color = frame.get("stroke_fg", self.border_color)
		size = frame.get("font_size", self.main_font_size)
		self._render_text(text_color=color, stroke_color=stroke_color, font_size=size)

	def _build_animation_sequence(self, mode: str, duration_ms: int, is_in: bool) -> list[dict]:
		steps = 10
		if mode == "none":
			return [{"delay": 0}]
		if mode == "fade":
			return self._fade_frames(steps, duration_ms, is_in)
		if mode == "zoom":
			return self._zoom_frames(steps, duration_ms, is_in)
		if mode == "tiktok":
			return self._tiktok_frames(duration_ms, is_in)
		return self._fade_frames(steps, duration_ms, is_in)

	def _fade_frames(self, steps: int, duration_ms: int, is_in: bool) -> list[dict]:
		start = self.bg_color if is_in else self.base_text_color
		end = self.base_text_color if is_in else self.bg_color
		stroke_start = self.bg_color if is_in else self.border_color
		stroke_end = self.border_color if is_in else self.bg_color
		colors = self._gradient(start, end, steps)
		stroke_colors = self._gradient(stroke_start, stroke_end, steps)
		delay = self._frame_delay(duration_ms, steps)
		return [{"fg": colors[i], "stroke_fg": stroke_colors[i], "delay": delay} for i in range(len(colors))]

	def _zoom_frames(self, steps: int, duration_ms: int, is_in: bool) -> list[dict]:
		min_size = max(12, int(self.main_font_size * 0.55))
		max_size = max(min_size + 1, int(self.main_font_size * 1.35))
		start = min_size if is_in else self.main_font_size
		end = self.main_font_size if is_in else max_size
		delay = self._frame_delay(duration_ms, steps)
		frames = []
		for step in range(steps):
			ratio = step / max(steps - 1, 1)
			font_size = int(start + (end - start) * ratio)
			frames.append({"font_size": font_size, "delay": delay, "fg": self.base_text_color, "stroke_fg": self.border_color})
		return frames

	def _tiktok_frames(self, duration_ms: int, is_in: bool) -> list[dict]:
		base = self.main_font_size
		pulse_big = int(base * 1.22)
		pulse_small = int(base * 0.86)
		hidden = self.bg_color
		if is_in:
			pattern = [
				{"font_size": pulse_small, "fg": hidden, "stroke_fg": hidden},
				{"font_size": pulse_big, "fg": self.base_text_color, "stroke_fg": self.border_color},
				{"font_size": int(base * 1.08), "fg": self.base_text_color, "stroke_fg": self.border_color},
				{"font_size": base, "fg": self.base_text_color, "stroke_fg": self.border_color},
			]
		else:
			pattern = [
				{"font_size": base, "fg": self.base_text_color, "stroke_fg": self.border_color},
				{"font_size": pulse_big, "fg": self.base_text_color, "stroke_fg": self.border_color},
				{"font_size": pulse_small, "fg": self.base_text_color, "stroke_fg": self.border_color},
				{"font_size": int(base * 0.75), "fg": hidden, "stroke_fg": hidden},
			]
		delay = self._frame_delay(duration_ms, len(pattern))
		for frame in pattern:
			frame["delay"] = delay
		return pattern

	def _frame_delay(self, duration_ms: int, steps: int) -> int:
		duration = self._safe_duration(duration_ms)
		if duration == 0:
			return 0
		return max(1, duration // max(steps, 1))

	def set_status(self, text: str) -> None:
		self.status_var.set(text)

	def update_main_font(self, family: str, size: int) -> None:
		self.main_font_family = family
		self.main_font_size = max(14, min(96, int(size)))
		if family not in self._font_options:
			self._font_options.insert(0, family)
			self._refresh_font_menu()
		self._render_text()

	def update_animation_settings(self, out_animation: str, out_duration_ms: int, in_animation: str, in_duration_ms: int) -> None:
		self.out_animation_var.set(out_animation if out_animation in self.animation_options else "fade")
		self.in_animation_var.set(in_animation if in_animation in self.animation_options else "fade")
		self.out_duration_var.set(self._safe_duration(out_duration_ms))
		self.in_duration_var.set(self._safe_duration(in_duration_ms))

	def update_style_settings(self, text_color: str, border_color: str, border_width: int, background_color: str) -> None:
		self.base_text_color = text_color
		self.border_color = border_color
		self.bg_color = background_color
		self.border_width = max(0, min(8, int(border_width)))

		self.text_color_var.set(self.base_text_color)
		self.border_color_var.set(self.border_color)
		self.bg_color_var.set(self.bg_color)
		self.border_width_var.set(self.border_width)

		self._apply_background_color()
		self._render_text()

	def _apply_background_color(self) -> None:
		self.root.configure(bg=self.bg_color)
		self.container.configure(bg=self.bg_color)
		self.controls.configure(bg=self.bg_color)
		self.style_controls.configure(bg=self.bg_color)
		self.display_area.configure(bg=self.bg_color)
		self.canvas.configure(bg=self.bg_color)
		self.status.configure(bg=self.bg_color)
		for widget in [self.font_label, self.size_label, self.out_anim_label, self.out_dur_label, self.in_anim_label, self.in_dur_label, self.border_width_label]:
			widget.configure(bg=self.bg_color)
		self.font_menu.configure(bg=self.bg_color)
		self.out_anim_menu.configure(bg=self.bg_color)
		self.in_anim_menu.configure(bg=self.bg_color)

	def _render_text(self, text_color: str | None = None, stroke_color: str | None = None, font_size: int | None = None) -> None:
		text_color = text_color or self.base_text_color
		stroke_color = stroke_color or self.border_color
		font_size = font_size or self.main_font_size
		font_tuple = (self.main_font_family, font_size, self.main_font_weight)

		width = max(300, self.canvas.winfo_width() - 40)
		x = max(self.canvas.winfo_width() // 2, 1)
		y = max(self.canvas.winfo_height() // 2, 1)

		self.canvas.delete("lyrics")
		self._stroke_items = []
		if self.border_width > 0:
			offsets = [
				(-self.border_width, 0), (self.border_width, 0), (0, -self.border_width), (0, self.border_width),
				(-self.border_width, -self.border_width), (-self.border_width, self.border_width),
				(self.border_width, -self.border_width), (self.border_width, self.border_width),
			]
			for ox, oy in offsets:
				item = self.canvas.create_text(
					x + ox, y + oy, text=self._current_text, fill=stroke_color, font=font_tuple,
					width=width, justify=tk.CENTER, tags="lyrics"
				)
				self._stroke_items.append(item)

		self._main_item = self.canvas.create_text(
			x, y, text=self._current_text, fill=text_color, font=font_tuple,
			width=width, justify=tk.CENTER, tags="lyrics"
		)

	def _safe_duration(self, value: int) -> int:
		return max(0, min(2000, int(value)))

	def _gradient(self, start_hex: str, end_hex: str, steps: int) -> list[str]:
		start = self._hex_to_rgb(start_hex)
		end = self._hex_to_rgb(end_hex)
		if steps <= 1:
			return [end_hex]
		result = []
		for step in range(steps):
			ratio = step / (steps - 1)
			channel = tuple(int(start[idx] + (end[idx] - start[idx]) * ratio) for idx in range(3))
			result.append(self._rgb_to_hex(channel))
		return result

	def _hex_to_rgb(self, color: str) -> tuple[int, int, int]:
		value = color.lstrip("#")
		return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

	def _rgb_to_hex(self, rgb: tuple[int, int, int]) -> str:
		return "#{:02x}{:02x}{:02x}".format(*rgb)
