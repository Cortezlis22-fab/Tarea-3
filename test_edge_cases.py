
import tempfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from analyzer import LogAnalyzer
from log_parser import LogParser
from models import Severity


class TestLogParser(unittest.TestCase):
    """Prueba los diferentes escenarios del analizador."""

    def setUp(self):
        self.parser = LogParser()

    def test_valid_date(self):
        event = self.parser.parse_line(
            "[INFO] 2025-01-10 User logged in", 1
        )

        self.assertEqual(event.severity, Severity.INFO)
        self.assertIsNotNone(event.event_date)
        self.assertTrue(event.is_valid)

    def test_impossible_date(self):
        event = self.parser.parse_line(
            "[ERROR] 2025-02-30 Database failure", 2
        )

        self.assertIsNone(event.event_date)
        self.assertFalse(event.is_valid)

    def test_different_date_format(self):
        event = self.parser.parse_line(
            "[INFO] 10/01/2025 User logged in", 3
        )

        self.assertIsNone(event.event_date)
        self.assertFalse(event.is_valid)
        self.assertIn("Formato de fecha incorrecto: 10/01/2025",
                      event.issues)

    def test_incomplete_date(self):
        event = self.parser.parse_line(
            "[INFO] 2025-1-10 User logged in", 4
        )

        self.assertIsNone(event.event_date)
        self.assertFalse(event.is_valid)

    def test_missing_date(self):
        event = self.parser.parse_line(
            "[WARNING] Invalid password attempt", 5
        )

        self.assertIsNone(event.event_date)
        self.assertIn("Fecha ausente", event.issues)

    def test_missing_message(self):
        event = self.parser.parse_line(
            "[ERROR] 2025-01-10", 6
        )

        self.assertIn("Mensaje ausente", event.issues)

    def test_unknown_severity(self):
        event = self.parser.parse_line(
            "[DEBUG] 2025-01-10 Debug message", 7
        )

        self.assertEqual(event.severity, Severity.UNKNOWN)
        self.assertFalse(event.is_valid)

    def test_empty_line(self):
        with self.assertRaises(ValueError):
            self.parser.parse_line("", 8)


class TestLogAnalyzer(unittest.TestCase):
    """Prueba la lectura de archivos completos."""
    def test_invalid_utf8_file(self):
         with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "invalid.txt"
            file_path.write_bytes(b"\xff")

            analyzer = LogAnalyzer()

            with self.assertRaises(UnicodeDecodeError):
                analyzer.analyze(file_path)
    
    def test_nonexistent_file(self):
        analyzer = LogAnalyzer()
        file_path = Path("archivo_inexistente.txt")

        with self.assertRaises(FileNotFoundError):
         analyzer.analyze(file_path)
    def setUp(self):
        self.analyzer = LogAnalyzer()

    def test_empty_file(self):
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "empty.txt"
            file_path.write_text("", encoding="utf-8")

            report = self.analyzer.analyze(file_path)

            self.assertEqual(report.total_events, 0)
            self.assertEqual(len(report.malformed_events), 0)
            self.assertEqual(report.ignored_blank_lines, 0)

    def test_file_with_blank_lines(self):
        with TemporaryDirectory() as directory:
            file_path = Path(directory) / "blank.txt"
            file_path.write_text("\n   \n", encoding="utf-8")

            report = self.analyzer.analyze(file_path)

            self.assertEqual(report.total_events, 0)
            self.assertEqual(report.ignored_blank_lines, 2)
    

if __name__ == "__main__":
    unittest.main(verbosity=2)
