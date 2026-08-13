import requests
import time


BASE_URL = "http://127.0.0.1:8000"


def send_action(title, action):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)

    print("\nAgent Action:")
    print(action)

    response = requests.post(
        f"{BASE_URL}/evaluate",
        json=action
    )

    result = response.json()

    print("\nGuardrail Decision:")
    print(result)

    return result


def main():

    print("\n")
    print("=" * 60)
    print("       AI ACTION GUARDRAIL SIMULATION")
    print("=" * 60)


    # ---------------------------------------
    # SCENARIO 1
    # ---------------------------------------

    send_action(
        "SCENARIO 1 — LARGE DATABASE DELETE",

        {
            "agent_id": "agent-demo",
            "tool_name": "database",
            "operation": "delete",
            "parameters": {
                "record_count": 500
            },
            "session_id": "demo-session-1"
        }
    )


    time.sleep(1)


    # ---------------------------------------
    # SCENARIO 2
    # ---------------------------------------

    send_action(
        "SCENARIO 2 — SMALL DATABASE DELETE",

        {
            "agent_id": "agent-demo",
            "tool_name": "database",
            "operation": "delete",
            "parameters": {
                "record_count": 5
            },
            "session_id": "demo-session-2"
        }
    )


    time.sleep(1)


    # ---------------------------------------
    # SCENARIO 3
    # ---------------------------------------

    result = send_action(
        "SCENARIO 3 — EXTERNAL EMAIL",

        {
            "agent_id": "agent-demo",
            "tool_name": "email",
            "operation": "send",
            "parameters": {
                "recipient": "customer@gmail.com",
                "domain_type": "external"
            },
            "session_id": "demo-session-3"
        }
    )


    approval_id = result.get("approval_id")


    if approval_id:

        print("\n")
        print("Human approval required.")
        print(f"Approval ID: {approval_id}")

        print("\nApproving request...")

        approval_response = requests.post(
            f"{BASE_URL}/approvals/{approval_id}/approve"
        )

        print("\nApproval Result:")
        print(approval_response.json())


    time.sleep(1)


    # ---------------------------------------
    # SCENARIO 4
    # ---------------------------------------

    send_action(
        "SCENARIO 4 — CONFIDENTIAL FILE READ",

        {
            "agent_id": "agent-demo",
            "tool_name": "file",
            "operation": "read",
            "parameters": {
                "path": "/documents/confidential/report.pdf"
            },
            "session_id": "demo-session-4"
        }
    )


    print("\n")
    print("=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()