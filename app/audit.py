import sqlite3
from datetime import datetime


DB_NAME = "audit.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            agent_id TEXT,
            tool_name TEXT,
            operation TEXT,
            outcome TEXT,
            reason TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pending_approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            agent_id TEXT,
            tool_name TEXT,
            operation TEXT,
            parameters TEXT,
            session_id TEXT,
            status TEXT
        )
    """)

    connection.commit()
    connection.close()


def log_action(
    agent_id,
    tool_name,
    operation,
    outcome,
    reason
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO audit_logs
        (
            timestamp,
            agent_id,
            tool_name,
            operation,
            outcome,
            reason
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        agent_id,
        tool_name,
        operation,
        outcome,
        reason
    ))

    connection.commit()
    connection.close()


def get_logs():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            timestamp,
            agent_id,
            tool_name,
            operation,
            outcome,
            reason
        FROM audit_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows