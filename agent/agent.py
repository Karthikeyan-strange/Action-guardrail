import requests


GUARDRAIL_URL = "http://127.0.0.1:8000/evaluate"


class Agent:

    def __init__(self, agent_id):

        self.agent_id = agent_id

    def perform_action(
        self,
        tool_name,
        operation,
        parameters,
        session_id
    ):

        action = {
            "agent_id": self.agent_id,
            "tool_name": tool_name,
            "operation": operation,
            "parameters": parameters,
            "session_id": session_id
        }

        response = requests.post(
            GUARDRAIL_URL,
            json=action
        )

        return response.json()


if __name__ == "__main__":

    agent = Agent("agent-001")

    result = agent.perform_action(
    tool_name="email",
    operation="send",
    parameters={
        "recipient": "customer@gmail.com",
        "domain_type": "external"
    },
    session_id="session-002"
)

    print("\nAgent Action Result")
    print("===================")
    print(result)