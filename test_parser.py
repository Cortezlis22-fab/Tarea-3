from log_parser import LogParser

# Crear una instancia del analizador de líneas.
parser = LogParser()

# Definir diferentes casos para comprobar el funcionamiento del parser.
test_cases = [
    "[INFO] 2025-01-10 User logged in",
    "[ERROR] 2025-02-30 Database failure",
    "[WARNING] Invalid password attempt",
    "[DEBUG] 2025-01-10 Unknown severity",
    "[ERROR] 2025-01-10"
]

# Recorrer los casos de prueba y asignar un número a cada línea.
for number, line in enumerate(test_cases, start=1):

    # Analizar la línea y obtener el evento con sus datos y posibles errores.
    event = parser.parse_line(line, number)

    # Mostrar la información que el parser identificó.
    print(f"\nLínea: {event.original_text}")
    print(f"Severidad: {event.severity.value}")
    print(f"Fecha: {event.event_date}")
    print(f"Mensaje: {event.message}")
    print(f"Válido: {event.is_valid}")
    print(f"Problemas: {event.issues}")