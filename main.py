
import sys
from collections import Counter
from pathlib import Path
from tkinter import Tk, filedialog

from analyzer import LogAnalyzer
from models import AnalysisReport, Severity


def select_file() -> Path | None:
    """Permite al usuario seleccionar un archivo de texto."""

    # Crear una ventana de Tkinter sin mostrar la ventana principal.
    root = Tk()
    root.withdraw()

    # Mantener el selector de archivos visible sobre otras ventanas.
    root.attributes("-topmost", True)

    try:
        # Mostrar el cuadro de diálogo para seleccionar un archivo TXT.
        selected_file = filedialog.askopenfilename(
            title="Seleccionar archivo de logs",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )

        # Convertir la ruta seleccionada en un objeto Path.
        # Si el usuario cancela, devolver None.
        return Path(selected_file) if selected_file else None

    finally:
        # Cerrar la ventana de Tkinter incluso si ocurre un error.
        root.destroy()


def print_report(report: AnalysisReport) -> None:
    """Muestra las estadísticas del análisis en consola."""

    # Contabilizar cuántos eventos pertenecen a cada nivel de severidad.
    severity_counts = Counter(
        event.severity for event in report.events
    )

    print("\n" + "=" * 55)
    print("             REPORTE DE ANÁLISIS DE LOGS")
    print("=" * 55)

    print(f"\nArchivo analizado: {report.source}")
    print(f"Total de eventos: {report.total_events}")

    # Mostrar la cantidad de eventos correspondientes a cada severidad.
    print("\nEVENTOS POR SEVERIDAD")
    print("-" * 35)

    for severity in Severity:
        count = severity_counts.get(severity, 0)
        print(f"{severity.value:<12}: {count}")

    # Presentar el estado general de los registros analizados.
    print("\nESTADO DE LOS REGISTROS")
    print("-" * 35)

    # Los registros válidos se obtienen restando los malformados del total.
    print(
        f"Registros válidos: "
        f"{report.total_events - len(report.malformed_events)}"
    )

    print(
        f"Registros malformados: "
        f"{len(report.malformed_events)}"
    )

    # Las líneas vacías se contabilizan aparte y no forman parte de los eventos.
    print(
        f"Líneas vacías ignoradas: "
        f"{report.ignored_blank_lines}"
    )

    # Mostrar los detalles de los registros que contienen problemas.
    if report.malformed_events:
        print("\nDETALLE DE REGISTROS INCORRECTOS")
        print("-" * 35)

        for event in report.malformed_events:
            print(
                f"\nLínea {event.line_number}: "
                f"{event.original_text}"
            )

            # Un registro puede presentar uno o varios problemas.
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
        # Solicitar al usuario que seleccione el archivo que desea analizar.
        file_path = select_file()

        # Si se cancela la selección, finalizar sin ejecutar el análisis.
        if file_path is None:
            print("Operación cancelada: no se seleccionó un archivo.")
            return 0

        # Crear el analizador y procesar el archivo seleccionado.
        analyzer = LogAnalyzer()
        report = analyzer.analyze(file_path)

        # Presentar el informe generado por el analizador.
        print_report(report)

        return 0

    # Gestionar errores específicos para mostrar mensajes comprensibles.
    except PermissionError:
        print("Error: no tienes permisos para leer el archivo.")
        return 1

    except UnicodeError:
        print("Error: no fue posible interpretar el archivo.")
        return 1

    except OSError as error:
        print(f"Error de lectura: {error}")
        return 1

    # Capturar otros errores inesperados para evitar una salida sin explicación.
    except Exception as error:
        print(f"Error inesperado: {error}")
        return 1


if __name__ == "__main__":
    # Ejecutar el programa y devolver su código de salida al sistema.
    sys.exit(main())
