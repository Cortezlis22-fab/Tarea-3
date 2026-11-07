
from pathlib import Path

from models import AnalysisReport
from log_parser import LogParser


class LogAnalyzer:
    """Coordina la lectura y el análisis de archivos de logs."""

    def __init__(self, parser: LogParser | None = None):
        self.parser = parser or LogParser()

    def analyze(self, file_path: Path) -> AnalysisReport:
        """
        Lee un archivo de logs, analiza sus registros
        y devuelve un informe con los resultados.
        """

        if not file_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo: {file_path}"
            )

        report = AnalysisReport(source=file_path)

        with file_path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:

            for line_number, line in enumerate(file, start=1):

                # Ignorar las líneas vacías.
                if not line.strip():
                    report.ignored_blank_lines += 1
                    continue

                event = self.parser.parse_line(
                    line,
                    line_number
                )

                report.events.append(event)

        return report
