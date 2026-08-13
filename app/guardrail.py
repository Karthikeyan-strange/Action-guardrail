import yaml

from app.audit import log_action


class ActionGuardrail:

    def __init__(self, policy_file):

        with open(policy_file, "r") as file:

            policy_data = yaml.safe_load(file)

        self.rules = policy_data["rules"]


    def evaluate(self, action):

        for rule in self.rules:

            if rule["tool"] != action.tool_name:
                continue

            if rule["operation"] != action.operation:
                continue

            condition = rule.get("condition")

            if self.check_condition(
                condition,
                action.parameters
            ):

                outcome = rule["action"]

                reason = rule["reason"]

                log_action(
                    action.agent_id,
                    action.tool_name,
                    action.operation,
                    outcome,
                    reason
                )

                return {
                    "allowed": outcome == "log_and_allow",
                    "outcome": outcome,
                    "reason": reason,
                    "rule": rule["name"]
                }

        # No matching rule
        log_action(
            action.agent_id,
            action.tool_name,
            action.operation,
            "allow",
            "No matching blocking rule"
        )

        return {
            "allowed": True,
            "outcome": "allow",
            "reason": "No matching policy rule",
            "rule": None
        }


    def check_condition(
        self,
        condition,
        parameters
    ):

        if not condition:
            return False

        parameter = condition["parameter"]

        operator = condition["operator"]

        expected_value = condition["value"]

        actual_value = parameters.get(parameter)

        if actual_value is None:
            return False

        if operator == "greater_than":

            return actual_value > expected_value

        if operator == "equals":

            return actual_value == expected_value

        if operator == "contains":

            return expected_value in actual_value

        return False