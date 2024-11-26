from .Export import Export
import sqlite3

class PythonSQL(Export):
    def export_to_database(report_name: str, report_table: list):
        try:
            # Konstanten definieren
            DATABASE_NAME = "test_result.db"
            PROTOCOL_TABLE_NAME = "test_protocol"
            RESULT_TABLE_NAME = "test_results"

            # Datenbank erstellen/verbindung herstellen
            connection = sqlite3.connect(DATABASE_NAME)
            cursor = connection.cursor()
            

            # SQL-Abfrage für test_name
            test_device, employee_number, test_id  = report_name.split('_', 2)
            sql = f'''
            INSERT INTO {PROTOCOL_TABLE_NAME} (
                test_id,
                test_device,
                employee_number
            )
            VALUES (?, ?, ?)
            '''
            cursor.execute(sql, (test_id, test_device, employee_number))


            # SQL-Abfrage für test_results
            sql = f'''
            INSERT INTO {RESULT_TABLE_NAME} (
                test_id,
                test_name,
                timestamp,
                duration,
                status,
                additional_info
            )
            VALUES (?, ?, ?, ?, ?, ?)
            '''
            for row in report_table:
                cursor.execute(sql, row)


            # Änderungen speichern
            connection.commit()

            # Erfolgreiche Rückmeldung
            return "Daten erfolgreich in die Datenbank exportiert."

        except Exception as e:
            # Fehlerbehandlung: Rückgabe einer Fehlermeldung
            connection.rollback()
            return f"Fehler beim Exportieren der Daten: {str(e)}"

        finally:
            connection.close()
        
