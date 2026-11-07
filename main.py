
import sys
from models import Severity
from models import AnalysisReport, Severity
from collections import Counter
from pathlib import Path
from tkinter import Tk, filedialog

from analyzer import LogAnalyzer
from models import Severity



def select_file() -> Path | None:
    """Permite al usuario seleccionar un archivo de texto."""

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    try:
        selected_file = filedialog.askopenfilename(
            title="Seleccionar archivo de logs",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        return Path(selected_file) if selected_file else None

    finally:
        root.destroy()


def print_report(report: AnalysisReport) -> None:
    """Muestra las estadísticas del análisis en consola."""

    severity_counts = Counter(
        event.severity for event in report.events
    )

    print("\n" + "=" * 55)
    print("             REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 55)

    print(f"\nArchivo analizado: {report.source}")
    print(f"Total de eventos: {report.total_events}")

    print("\nEVENTOS POR SEVERIDAD")
    print("-" * 35)

    for severity in Severity:
        count = severity_counts.get(severity, 0)
        print(f"{severity.value:<12}: {count}")

    print("\nESTADO DE LOS REGISTROS")
    print("-" * 35)

    print(
        f"Registros válidos: "
        f"{report.total_events - len(report.malformed_events)}"
    )

    print(
        f"Registros malformados: "
        f"{len(report.malformed_events)}"
    )

    print(
        f"Líneas vacías ignoradas: "
        f"{report.ignored_blank_lines}"
    )

    if report.malformed_events:
        print("\nDETALLE DE REGISTROS INCORRECTOS")
        print("-" * 35)

        for event in report.malformed_events:
            print(
                f"\nLínea {event.line_number}: "
                f"{event.original_text}"
            )

            for issue in event.issues:
                print(f"  - {issue}")

    print("\n" + "=" * 55)
    print("          ANÁLISIS FINALIZADO")
    print("=" * 55)


def main() -> int:
    """Coordina la ejecución principal del programa."""

    print("\nANALIZADOR DE ARCHIVOS DE LOGS")
    print("Selecciona un archivo TXT para comenzar.\n")

    try:
        file_path = select_file()

        if file_path is None:
            print("Operación cancelada: no se seleccionó un archivo.")
            return 0

        analyzer = LogAnalyzer()
        report = analyzer.analyze(file_path)

        print_report(report)

        return 0

    except PermissionError:
        print("Error: no tienes permisos para leer el archivo.")
        return 1

    except UnicodeError:
        print("Error: no fue posible interpretar el archivo.")
        return 1

    except OSError as error:
        print(f"Error de lectura: {error}")
        return 1

    except Exception as error:
        print(f"Error inesperado: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
