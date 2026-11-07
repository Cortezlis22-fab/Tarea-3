
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path


class Severity(Enum):
    """Define los niveles de severidad de los eventos."""

    # Utilizar valores definidos evita clasificaciones inconsistentes.
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class LogEvent:
    """Representa un evento individual del archivo de logs."""

    # frozen=True impide modificar los datos del evento después de crearlo.
    line_number: int
    original_text: str
    severity: Severity
    event_date: date | None
    message: str
    issues: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_valid(self) -> bool:
        """Indica si el evento no presenta problemas."""

        # Un evento se considera válido únicamente cuando no tiene errores.
        return len(self.issues) == 0


@dataclass
class AnalysisReport:
    """Almacena los resultados del análisis del archivo."""

    source: Path

    # Cada informe inicia con una lista independiente de eventos.
    events: list[LogEvent] = field(default_factory=list)

    # Contabilizar las líneas vacías sin incluirlas en el total de eventos.
    ignored_blank_lines: int = 0

    @property
    def total_events(self) -> int:
        """Devuelve la cantidad total de eventos analizados."""
        return len(self.events)

    @property
    def malformed_events(self) -> list[LogEvent]:
        """Obtiene únicamente los eventos que presentan problemas."""

        # Filtrar los eventos según su propiedad de validación.
        return [
            event for event in self.events
            if not event.is_valid
        ]
