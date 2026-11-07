
from pathlib import Path

from analyzer import LogAnalyzer


def main():
    analyzer = LogAnalyzer()

    file_path = Path("logs_test.txt")

    report = analyzer.analyze(file_path)

    print("\nREPORTE DE PRUEBA")
    print("-" * 35)

    print(f"Total de eventos: {report.total_events}")
    print(f"Eventos malformados: {len(report.malformed_events)}")
    print(f"Líneas vacías: {report.ignored_blank_lines}")

    print("\nEventos detectados:")

    for event in report.events:
        print(
            f"Línea {event.line_number}: "
            f"{event.severity.value} | "
            f"Válido: {event.is_valid}"
        )


if __name__ == "__main__":
    main()
