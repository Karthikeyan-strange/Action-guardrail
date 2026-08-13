import yaml

POLICY_FILE = "app/policy.yaml"


def load_policies():
    with open(POLICY_FILE, "r") as file:
        data = yaml.safe_load(file)

    return data.get("rules", [])


def save_policies(rules):
    with open(POLICY_FILE, "w") as file:
        yaml.safe_dump(
            {"rules": rules},
            file,
            sort_keys=False
        )