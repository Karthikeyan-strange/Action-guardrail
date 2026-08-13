def database_tool(operation, parameters):
    """
    Mock database tool.
    """

    if operation == "delete":

        record_count = parameters.get("record_count", 0)

        return {
            "tool": "database",
            "status": "executed",
            "message": f"{record_count} records deleted"
        }

    if operation == "read":

        return {
            "tool": "database",
            "status": "executed",
            "message": "Customer records retrieved"
        }

    return {
        "tool": "database",
        "status": "error",
        "message": "Unsupported database operation"
    }


def email_tool(operation, parameters):
    """
    Mock email tool.
    """

    if operation == "send":

        recipient = parameters.get(
            "recipient",
            "unknown"
        )

        return {
            "tool": "email",
            "status": "executed",
            "message": f"Email sent to {recipient}"
        }

    return {
        "tool": "email",
        "status": "error",
        "message": "Unsupported email operation"
    }


def file_tool(operation, parameters):
    """
    Mock file tool.
    """

    if operation == "read":

        path = parameters.get(
            "path",
            "unknown"
        )

        return {
            "tool": "file",
            "status": "executed",
            "message": f"File read: {path}"
        }

    return {
        "tool": "file",
        "status": "error",
        "message": "Unsupported file operation"
    }


def execute_tool(
    tool_name,
    operation,
    parameters
):

    if tool_name == "database":

        return database_tool(
            operation,
            parameters
        )

    if tool_name == "email":

        return email_tool(
            operation,
            parameters
        )

    if tool_name == "file":

        return file_tool(
            operation,
            parameters
        )

    return {
        "status": "error",
        "message": f"Unknown tool: {tool_name}"
    }