import requests


BASE_URL = "http://127.0.0.1:8000"


def test_large_delete_blocked():

    action = {
        "agent_id": "test-agent",
        "tool_name": "database",
        "operation": "delete",
        "parameters": {
            "record_count": 500
        },
        "session_id": "test-session"
    }

    response = requests.post(
        f"{BASE_URL}/evaluate",
        json=action
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "blocked"
    assert data["tool_executed"] is False

    print("PASS: Large delete blocked")


def test_small_delete_allowed():

    action = {
        "agent_id": "test-agent",
        "tool_name": "database",
        "operation": "delete",
        "parameters": {
            "record_count": 5
        },
        "session_id": "test-session"
    }

    response = requests.post(
        f"{BASE_URL}/evaluate",
        json=action
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "executed"
    assert data["tool_executed"] is True

    print("PASS: Small delete executed")


def test_external_email_hitl():

    action = {
        "agent_id": "test-agent",
        "tool_name": "email",
        "operation": "send",
        "parameters": {
            "recipient": "customer@gmail.com",
            "domain_type": "external"
        },
        "session_id": "test-session"
    }

    response = requests.post(
        f"{BASE_URL}/evaluate",
        json=action
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "waiting_for_human_approval"
    assert data["tool_executed"] is False
    assert "approval_id" in data

    print("PASS: External email requires HITL")


def test_confidential_file_log_and_allow():

    action = {
        "agent_id": "test-agent",
        "tool_name": "file",
        "operation": "read",
        "parameters": {
            "path": "/documents/confidential/report.pdf"
        },
        "session_id": "test-session"
    }

    response = requests.post(
        f"{BASE_URL}/evaluate",
        json=action
    )

    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "executed"
    assert data["decision"]["outcome"] == "log_and_allow"

    print("PASS: Confidential read logged and allowed")