from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

from app.models import ToolAction
from app.guardrail import ActionGuardrail
from app.audit import init_db, get_logs, log_action
from app.tools import execute_tool
from app.policy_manager import load_policies, save_policies
from app.hitl import (
    create_approval,
    get_pending_approvals,
    get_approval,
    update_approval
)


app = FastAPI(
    title="AI Action Guardrail",
    description="Policy enforcement layer for AI agent tool calls",
    version="1.0.0"
)

# Parse CORS origins from environment variable
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_db()

guardrail = ActionGuardrail(
    "app/policy.yaml"
)


@app.get("/")
def home():

    return {
        "system": "AI Action Guardrail",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/evaluate")
def evaluate_action(action: ToolAction):

    # --------------------------------
    # STEP 1: Evaluate Guardrail
    # --------------------------------

    decision = guardrail.evaluate(action)

    outcome = decision["outcome"]


    # --------------------------------
    # BLOCK
    # --------------------------------

    if outcome == "block":

        return {
            "agent_id": action.agent_id,
            "tool": action.tool_name,
            "operation": action.operation,
            "status": "blocked",
            "decision": decision,
            "tool_executed": False
        }


    # --------------------------------
    # HITL
    # --------------------------------

    if outcome == "require_hitl":

        approval_id = create_approval(
            agent_id=action.agent_id,
            tool_name=action.tool_name,
            operation=action.operation,
            parameters=action.parameters,
            session_id=action.session_id
        )

        return {
            "agent_id": action.agent_id,
            "tool": action.tool_name,
            "operation": action.operation,
            "status": "waiting_for_human_approval",
            "approval_id": approval_id,
            "decision": decision,
            "tool_executed": False
        }


    # --------------------------------
    # ALLOW
    # --------------------------------

    tool_result = execute_tool(
        action.tool_name,
        action.operation,
        action.parameters
    )

    return {
        "agent_id": action.agent_id,
        "tool": action.tool_name,
        "operation": action.operation,
        "status": "executed",
        "decision": decision,
        "tool_executed": True,
        "tool_result": tool_result
    }


# ==================================
# HITL ENDPOINTS
# ==================================


@app.get("/approvals")
def pending_approvals():

    return {
        "count": len(get_pending_approvals()),
        "approvals": get_pending_approvals()
    }


@app.post("/approvals/{approval_id}/approve")
def approve_action(approval_id: int):

    approval = get_approval(approval_id)

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found"
        )

    if approval["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="Approval request already processed"
        )


    # Execute tool ONLY after human approval

    tool_result = execute_tool(
        approval["tool_name"],
        approval["operation"],
        approval["parameters"]
    )


    update_approval(
        approval_id,
        "approved"
    )


    log_action(
        approval["agent_id"],
        approval["tool_name"],
        approval["operation"],
        "approved_and_executed",
        "Human approval granted"
    )


    return {
        "approval_id": approval_id,
        "status": "approved",
        "tool_executed": True,
        "tool_result": tool_result
    }


@app.post("/approvals/{approval_id}/reject")
def reject_action(approval_id: int):

    approval = get_approval(approval_id)

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Approval request not found"
        )

    if approval["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="Approval request already processed"
        )


    update_approval(
        approval_id,
        "rejected"
    )


    log_action(
        approval["agent_id"],
        approval["tool_name"],
        approval["operation"],
        "rejected",
        "Human approval denied"
    )


    return {
        "approval_id": approval_id,
        "status": "rejected",
        "tool_executed": False
    }


# ==================================
# AUDIT
# ==================================


@app.get("/audit")
def audit_logs():

    rows = get_logs()

    logs = []

    for row in rows:

        logs.append({
            "id": row[0],
            "timestamp": row[1],
            "agent_id": row[2],
            "tool": row[3],
            "operation": row[4],
            "outcome": row[5],
            "reason": row[6]
        })

    return {
        "count": len(logs),
        "logs": logs
    }
@app.get("/policies")
def get_policies():

    rules = load_policies()

    return {
        "count": len(rules),
        "policies": rules
    }


@app.put("/policies")
def update_policies(data: dict):

    rules = data.get("rules", [])

    save_policies(rules)

    return {
        "status": "success",
        "message": "Policies updated",
        "count": len(rules)
    }
    