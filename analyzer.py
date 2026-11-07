from pathlib import Path

from models import AnalysisReport
from log_parser import LogParser


class LogAnalyzer:
    """Coordina la lectura y el análisis de archivos de logs."""

    def __init__(self, parser: LogParser | None = None):
        # Permite utilizar un parser personalizado o crear uno por defecto.
        self.parser = parser or LogParser()

    def analyze(self, file_path: Path) -> AnalysisReport:
        """
        Lee un archivo de logs, analiza sus registros
        y devuelve un informe con los resultados.
        """

        # Verificar que la ruta seleccionada corresponda a un archivo existente.
        # Si no existe, se genera una excepción para evitar continuar el análisis.
        if not file_path.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo: {file_path}"
            )

        # Crear el informe donde se almacenarán los eventos analizados
        # y la cantidad de líneas vacías encontradas.
        report = AnalysisReport(source=file_path)

        # utf-8-sig permite leer archivos UTF-8 con o sin marca BOM.
        # La lectura estricta permite detectar errores de codificación
        # en lugar de reemplazar caracteres inválidos silenciosamente.
        with file_path.open(
            "r",
            encoding="utf-8-sig",
        ) as file:

            # Enumerar las líneas desde 1 para conservar su numeración original.
            for line_number, line in enumerate(file, start=1):

                # Las líneas vacías no se consideran eventos,
                # pero se contabilizan por separado en el informe.
                if not line.strip():
                    report.ignored_blank_lines += 1
                    continue

                # Enviar cada línea no vacía al parser para identificar
                # su severidad, fecha, mensaje y posibles errores.
                event = self.parser.parse_line(
                    line,
                    line_number
                )

                # Guardar el evento analizado en el informe general.
                report.events.append(event)

        # Devolver el informe con todos los eventos y estadísticas recopiladas.
        return report