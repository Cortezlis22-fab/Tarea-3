
import re
from datetime import date

from models import LogEvent, Severity


class LogParser:
    """Interpreta y valida cada línea de un archivo de logs."""

    SEVERITY_PATTERN = re.compile(
        r"^\s*\[(INFO|WARNING|ERROR)\]\s*",
        re.IGNORECASE
    )

    UNKNOWN_PATTERN = re.compile(
        r"^\s*\[([A-Z]+)\]\s*",
        re.IGNORECASE
    )

    DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def parse_line(self, line: str, line_number: int) -> LogEvent:
        """
        Analiza una línea y devuelve un objeto LogEvent
        con la información identificada y sus posibles errores.
        """

        original_text = line.rstrip("\r\n")
        remaining = original_text.strip()

        issues = []

        if not remaining:
            raise ValueError("No se pueden analizar líneas vacías.")


        severity_match = self.SEVERITY_PATTERN.match(remaining)

        if severity_match:
            severity = Severity(severity_match.group(1).upper())
            remaining = remaining[severity_match.end():].strip()

        else:
            severity = Severity.UNKNOWN
            issues.append("Nivel de severidad ausente o desconocido")

    
            unknown_match = self.UNKNOWN_PATTERN.match(remaining)

            if unknown_match:
                remaining = remaining[unknown_match.end():].strip()
        event_date = None

        if remaining:
            first_token = remaining.split(maxsplit=1)[0]


            if re.fullmatch(
             r"\d{1,4}[-/]\d{1,2}[-/]\d{1,4}",
                     first_token
                 ):
                if self.DATE_PATTERN.fullmatch(first_token):
                    try:
                        event_date = date.fromisoformat(first_token)

                    except ValueError:
                        issues.append(
                            f"Fecha inválida: {first_token}"
                        )
                else:
                    issues.append(
                        f"Formato de fecha incorrecto: {first_token}"
                    )

                
                remaining = remaining[len(first_token):].strip()

            else:
                issues.append("Fecha ausente")

        else:
            issues.append("Fecha ausente")

        
        message = remaining

        if not message:
            issues.append("Mensaje ausente")

        return LogEvent(
            line_number=line_number,
            original_text=original_text,
            severity=severity,
            event_date=event_date,
            message=message,
            issues=tuple(issues)
        )
