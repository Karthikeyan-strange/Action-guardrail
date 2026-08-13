import sqlite3
import json
from datetime import datetime


DB_NAME = "audit.db"


def create_approval(
    agent_id,
    tool_name,
    operation,
    parameters,
    session_id
):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO pending_approvals
        (
            created_at,
            agent_id,
            tool_name,
            operation,
            parameters,
            session_id,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        agent_id,
        tool_name,
        operation,
        json.dumps(parameters),
        session_id,
        "pending"
    ))

    approval_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return approval_id


def get_pending_approvals():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            created_at,
            agent_id,
            tool_name,
            operation,
            parameters,
            session_id,
            status
        FROM pending_approvals
        WHERE status = 'pending'
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    approvals = []

    for row in rows:

        approvals.append({
            "id": row[0],
            "created_at": row[1],
            "agent_id": row[2],
            "tool_name": row[3],
            "operation": row[4],
            "parameters": json.loads(row[5]),
            "session_id": row[6],
            "status": row[7]
        })

    return approvals


def get_approval(approval_id):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            created_at,
            agent_id,
            tool_name,
            operation,
            parameters,
            session_id,
            status
        FROM pending_approvals
        WHERE id = ?
    """, (approval_id,))

    row = cursor.fetchone()

    connection.close()

    if not row:
        return None

    return {
        "id": row[0],
        "created_at": row[1],
        "agent_id": row[2],
        "tool_name": row[3],
        "operation": row[4],
        "parameters": json.loads(row[5]),
        "session_id": row[6],
        "status": row[7]
    }


def update_approval(
    approval_id,
    status
):

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE pending_approvals
        SET status = ?
        WHERE id = ?
    """, (
        status,
        approval_id
    ))

    connection.commit()
    connection.close()