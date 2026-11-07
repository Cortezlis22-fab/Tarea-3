
import re
from datetime import date

from models import LogEvent, Severity


class LogParser:
    """Interpreta y valida cada línea de un archivo de logs."""

    # Reconocer únicamente los niveles de severidad admitidos.
    # IGNORECASE permite aceptar etiquetas escritas en mayúsculas o minúsculas.
    SEVERITY_PATTERN = re.compile(
        r"^\s*\[(INFO|WARNING|ERROR)\]\s*",
        re.IGNORECASE
    )

    # Detectar otras etiquetas entre corchetes para clasificarlas como UNKNOWN.
    UNKNOWN_PATTERN = re.compile(
        r"^\s*\[([A-Z]+)\]\s*",
        re.IGNORECASE
    )

    # Establecer el único formato de fecha aceptado: año-mes-día.
    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def parse_line(self, line: str, line_number: int) -> LogEvent:
        """
        Analiza una línea y devuelve un objeto LogEvent
        con la información identificada y sus posibles errores.
        """

        # Conservar el texto original y eliminar únicamente los saltos de línea.
        original_text = line.rstrip("\r\n")
        remaining = original_text.strip()

        # Almacenar todos los problemas encontrados durante la validación.
        issues = []

        # Una línea vacía no puede considerarse un evento.
        if not remaining:
            raise ValueError("No se pueden analizar líneas vacías.")

        # Comprobar si la línea comienza con una severidad reconocida.
        severity_match = self.SEVERITY_PATTERN.match(remaining)

        if severity_match:
            # Convertir la etiqueta encontrada en un valor del enumerado Severity.
            severity = Severity(severity_match.group(1).upper())
            remaining = remaining[severity_match.end():].strip()

        else:
            # Si la severidad falta o no está admitida, clasificarla como UNKNOWN.
            severity = Severity.UNKNOWN
            issues.append("Nivel de severidad ausente o desconocido")

            # Si existe una etiqueta desconocida, retirarla para continuar
            # analizando correctamente el resto del registro.
            unknown_match = self.UNKNOWN_PATTERN.match(remaining)

            if unknown_match:
                remaining = remaining[unknown_match.end():].strip()

        event_date = None

        if remaining:
            # Obtener el primer elemento para comprobar si contiene una fecha.
            first_token = remaining.split(maxsplit=1)[0]

            # Detectar formatos que parecen fechas, aunque no necesariamente
            # cumplan el formato ISO requerido.
            if re.fullmatch(
                r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}",
                first_token
            ):
                # Verificar que la fecha tenga exactamente el formato YYYY-MM-DD.
                if self.DATE_PATTERN.fullmatch(first_token):
                    try:
                        # Comprobar también que la fecha exista en el calendario.
                        event_date = date.fromisoformat(first_token)

                    except ValueError:
                        issues.append(
                            f"Fecha inválida: {first_token}"
                        )
                else:
                    # Registrar los formatos de fecha diferentes al ISO admitido.
                    issues.append(
                        f"Formato de fecha incorrecto: {first_token}"
                    )

                # Retirar la fecha del texto para obtener posteriormente el mensaje.
                remaining = remaining[len(first_token):].strip()

            else:
                # Si el primer elemento no parece una fecha, marcarla como ausente.
                issues.append("Fecha ausente")

        else:
            # No existe contenido después de la severidad para identificar la fecha.
            issues.append("Fecha ausente")

        # El contenido restante corresponde al mensaje del evento.
        message = remaining

        # Comprobar que el registro contenga un mensaje.
        if not message:
            issues.append("Mensaje ausente")

        # Construir el evento con los datos identificados y todos sus problemas.
        return LogEvent(
            line_number=line_number,
            original_text=original_text,
            severity=severity,
            event_date=event_date,
            message=message,
            issues=tuple(issues)
        )

