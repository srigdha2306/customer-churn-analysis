
from pathlib import Path
import sqlite3

project_dir = Path(__file__).resolve().parents[1]
db_path = project_dir / "data" / "processed" / "churn.db"
sql_path = project_dir / "sql" / "analysis.sql"

sql_text = sql_path.read_text(encoding="utf-8")


def split_sql_statements(sql_text):
    statements = []
    buffer = ""

    for line in sql_text.splitlines():
        buffer += line + "\n"

        if sqlite3.complete_statement(buffer):
            statement = buffer.strip()
            if statement:
                statements.append(statement)
            buffer = ""

    if buffer.strip():
        statements.append(buffer.strip())

    return statements


with sqlite3.connect(db_path) as connection:
    query_number = 0

    for statement in split_sql_statements(sql_text):
        cursor = connection.execute(statement)

        if cursor.description:
            query_number += 1
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            print(f"\n--- Query {query_number} ---")
            print(" | ".join(columns))
            print("-" * 50)

            for row in rows:
                print(" | ".join(str(value) for value in row))
