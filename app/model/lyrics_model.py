import os
from dataclasses import dataclass, field


@dataclass
class LyricsModel:
	lines: list[str] = field(default_factory=list)
	index: int = 0
	file_path: str | None = None

	def load_from_path(self, path: str) -> None:
		if not os.path.isfile(path):
			raise FileNotFoundError(f"No se encontró el archivo:\n{path}")

		with open(path, "r", encoding="utf-8", errors="replace") as file:
			raw_lines = file.readlines()

		self.lines = [line.rstrip("\r\n") for line in raw_lines]
		self.index = 0
		self.file_path = path

	def has_lines(self) -> bool:
		return bool(self.lines)

	def current_line(self) -> str:
		if not self.lines:
			return "Archivo vacío"
		return self.lines[self.index]

	def current_position(self) -> tuple[int, int]:
		if not self.lines:
			return (0, 0)
		return (self.index + 1, len(self.lines))

	def current_filename(self) -> str:
		if not self.file_path:
			return "(sin archivo)"
		return os.path.basename(self.file_path)

	def advance(self) -> bool:
		if not self.lines:
			return False

		if self.index < len(self.lines) - 1:
			self.index += 1
			return False

		self.index = 0
		return True
