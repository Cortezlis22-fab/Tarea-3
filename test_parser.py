from log_parser import LogParser

parser = LogParser()

test_cases = [
    "[INFO] 2025-01-10 User logged in",
    "[ERROR] 2025-02-30 Database failure",
    "[WARNING] Invalid password attempt",
    "[DEBUG] 2025-01-10 Unknown severity",
    "[ERROR] 2025-01-10"
]

for number, line in enumerate(test_cases, start=1):
    event = parser.parse_line(line, number)

    print(f"\nLínea: {event.original_text}")
    print(f"Severidad: {event.severity.value}")
    print(f"Fecha: {event.event_date}")
    print(f"Mensaje: {event.message}")
    print(f"Válido: {event.is_valid}")
    print(f"Problemas: {event.issues}")