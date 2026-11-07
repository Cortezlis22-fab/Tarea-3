
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from pathlib import Path


class Severity(Enum):
    """Define los niveles de severidad de los eventos."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class LogEvent:
    """Representa un evento individual del archivo de logs."""

    line_number: int
    original_text: str
    severity: Severity
    event_date: date | None
    message: str
    issues: tuple[str, ...] = field(default_factory=tuple)

    @property
    def is_valid(self) -> bool:
        """Indica si el evento no presenta problemas."""
        return len(self.issues) == 0


@dataclass
class AnalysisReport:
    """Almacena los resultados del análisis del archivo."""

    source: Path
    events: list[LogEvent] = field(default_factory=list)
    ignored_blank_lines: int = 0

    @property
    def total_events(self) -> int:
        return len(self.events)

    @property
    def malformed_events(self) -> list[LogEvent]:
        return [
            event for event in self.events
            if not event.is_valid
        ]
