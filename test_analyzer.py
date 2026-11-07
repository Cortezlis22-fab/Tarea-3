
from pathlib import Path

from analyzer import LogAnalyzer


def main():
    # Crear una instancia del analizador para procesar el archivo de prueba.
    analyzer = LogAnalyzer()

    # Definir la ruta del archivo TXT que contiene los registros de prueba.
    file_path = Path("logs_test.txt")

    # Ejecutar el análisis y obtener el informe con los resultados.
    report = analyzer.analyze(file_path)

    # Mostrar un resumen de los resultados obtenidos.
    print("\nREPORTE DE PRUEBA")
    print("-" * 35)

    print(f"Total de eventos: {report.total_events}")
    print(f"Eventos malformados: {len(report.malformed_events)}")
    print(f"Líneas vacías: {report.ignored_blank_lines}")

    # Mostrar los eventos identificados y su estado de validación.
    print("\nEventos detectados:")

    for event in report.events:
        print(
            f"Línea {event.line_number}: "
            f"{event.severity.value} | "
            f"Válido: {event.is_valid}"
        )


if __name__ == "__main__":
    # Ejecutar las pruebas manuales cuando se inicia este archivo directamente.
    main()
