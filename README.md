# 🛡️ AI Action Guardrail

### Runtime Policy Enforcement for Agentic AI

> **An enforcement layer that governs what AI agents *do*, not just what they *say*.**

AI agents are increasingly capable of taking real-world actions through tools — deleting database records, sending emails, modifying files, calling APIs, and more.

Traditional LLM guardrails mainly inspect **prompts and generated text**. But a perfectly harmless-looking response can still cause an agent to perform a dangerous operation.

**AI Action Guardrail** solves this problem by placing a policy enforcement layer **between an AI agent and its tools**.

```text
                 AI AGENT
                    │
                    │ Tool Call
                    ▼
          ┌─────────────────────┐
          │   ACTION GUARDRAIL  │
          │                     │
          │    Policy Engine    │
          └──────────┬──────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       ALLOW       BLOCK       HITL
          │          │          │
          ▼          ▼          ▼
      Execute      Reject    Human Review
       Tool                     │
          │              ┌──────┴──────┐
          │              ▼             ▼
          │           APPROVE       REJECT
          │              │
          └──────────────┘
                     │
                     ▼
               AUDIT LOG
```

---

## 🚀 Why This Project?

An AI agent may receive a request such as:

> "Delete the unnecessary customer records."

The LLM might generate a completely normal response, but the actual tool call could be:

```text
DELETE 500 customer records
```

A text-only safety system may never see this as a dangerous action.

This project evaluates the **actual action before execution**.

```text
Agent wants to delete 500 records
              ↓
        Action Guardrail
              ↓
     record_count > 100
              ↓
          ❌ BLOCKED
              ↓
        Audit Recorded
```

---

## 🎯 Problem Statement

This project implements **PS-3.1 — The Action Guardrail** from the Agentic AI Governance problem set.

The goal is to build a guardrail that operates on **agent actions rather than only LLM text**, evaluating every tool call before execution.

The policy engine supports three enforcement outcomes:

| Outcome            | Behaviour                          |
| ------------------ | ---------------------------------- |
| 🟢 `log_and_allow` | Execute the action and record it   |
| 🔴 `block`         | Reject the action                  |
| 🟠 `require_hitl`  | Pause execution for human approval |

---

# ✨ Key Features

### 🛡️ Runtime Action Enforcement

Every agent tool call passes through the policy engine before execution.

```text
Agent
  ↓
Tool Request
  ↓
Policy Evaluation
  ↓
Decision
  ↓
Tool Execution / Rejection / HITL
```

### 📜 Declarative YAML Policies

Policies are defined independently from application logic.

Example:

```yaml
- name: block_large_delete
  tool: database
  operation: delete

  condition:
    parameter: record_count
    operator: greater_than
    value: 100

  action: block

  reason: "Database delete exceeds 100 records"
```

This makes policies easy to understand, modify, and extend.

---

### 👤 Human-in-the-Loop

High-risk actions can be paused for human review.

```text
AI Agent
   ↓
External Email
   ↓
Policy Engine
   ↓
REQUIRE HITL
   ↓
Approval Queue
   ↓
Human Reviewer
   ├── APPROVE → Execute
   └── REJECT  → Block
```

---

### 📋 Audit Logging

Every evaluated action is recorded with:

* Agent ID
* Tool
* Operation
* Outcome
* Reason
* Timestamp

Example:

```json
{
  "agent_id": "agent-001",
  "tool": "database",
  "operation": "delete",
  "outcome": "block",
  "reason": "Database delete exceeds 100 records"
}
```

---

### 📊 React Dashboard

The project includes a modern **React + Vite** dashboard providing:

* Total actions
* Allowed actions
* Blocked actions
* Pending HITL requests
* Active policies
* Recent audit activity
* Human approval/rejection controls
* System health status

---

### 🧪 Simulation Harness

The project includes automated scenarios demonstrating:

```text
Scenario 1
500-record delete
        ↓
     BLOCK ❌


Scenario 2
5-record delete
        ↓
    EXECUTE ✅


Scenario 3
External email
        ↓
   REQUIRE HITL ⚠️
        ↓
     APPROVE
        ↓
    EXECUTE ✅


Scenario 4
Confidential file read
        ↓
 LOG + ALLOW 📝
```

---

# 🏗️ Architecture

```text
                         ┌───────────────────┐
                         │     AI AGENT      │
                         └─────────┬─────────┘
                                   │
                              Tool Call
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │    ACTION GUARDRAIL      │
                    │                          │
                    │    FastAPI API Layer     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      POLICY ENGINE       │
                    │                          │
                    │       policy.yaml        │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
                 ALLOW        BLOCK         HITL
                    │            │            │
                    ▼            ▼            ▼
               Mock Tool      Reject     Approval Queue
                    │                         │
                    │                   Human Review
                    │                         │
                    │                    ┌────┴────┐
                    │                    ▼         ▼
                    │                 APPROVE   REJECT
                    │                    │
                    └────────────────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │  AUDIT LOG    │
                         │    SQLite     │
                         └───────────────┘
                                 │
                                 ▼
                         React Dashboard
```

---

# 🧰 Technology Stack

### Backend

* **Python 3.10**
* **FastAPI**
* **Pydantic**
* **PyYAML**
* **SQLite**
* **Uvicorn**

### Frontend

* **React**
* **Vite**
* **JavaScript**
* **Lucide React**
* **CSS**

### Testing

* **Pytest**
* Automated API scenarios
* Guardrail simulation harness

### Deployment

* **Docker**
* Docker Compose
* AWS deployment ready

---

# 📁 Project Structure

```text
action-guardrail/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── guardrail.py
│   ├── models.py
│   ├── policy.yaml
│   ├── policy_manager.py
│   ├── audit.py
│   ├── hitl.py
│   └── tools.py
│
├── agent/
│   └── agent.py
│
├── tests/
│   └── test_guardrail.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   └── package-lock.json
│
├── simulation.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>

cd action-guardrail
```

---

## 2. Create Python environment

Python **3.10** is used for the backend.

```bash
py -3.10 -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Install backend dependencies

```bash
py -3.10 -m pip install -r requirements.txt
```

---

## 4. Start FastAPI

```bash
py -3.10 -m uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🎨 Start React Frontend

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start Vite:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# 🧪 Running Tests

Start the backend first:

```bash
py -3.10 -m uvicorn app.main:app --reload
```

Then in another terminal:

```bash
pytest -s
```

Expected:

```text
PASS: Large delete blocked
PASS: Small delete executed
PASS: External email requires HITL
PASS: Confidential read logged and allowed

4 passed
```

---

# ▶️ Running the Simulation

With the backend running:

```bash
py -3.10 simulation.py
```

The simulation demonstrates the complete governance workflow:

```text
┌─────────────────────────────────────┐
│       AI ACTION GUARDRAIL           │
├─────────────────────────────────────┤
│                                     │
│  DELETE 500       → BLOCK ❌        │
│                                     │
│  DELETE 5         → ALLOW ✅        │
│                                     │
│  EXTERNAL EMAIL   → HITL ⚠️         │
│                    → APPROVE        │
│                    → EXECUTE ✅      │
│                                     │
│  CONFIDENTIAL     → LOG + ALLOW 📝  │
│  FILE READ                           │
│                                     │
└─────────────────────────────────────┘
```

---

# 📡 API Endpoints

| Method | Endpoint                  | Purpose                    |
| ------ | ------------------------- | -------------------------- |
| `GET`  | `/`                       | System information         |
| `GET`  | `/health`                 | Health check               |
| `POST` | `/evaluate`               | Evaluate an agent action   |
| `GET`  | `/audit`                  | Retrieve audit logs        |
| `GET`  | `/approvals`              | View pending HITL requests |
| `POST` | `/approvals/{id}/approve` | Approve an action          |
| `POST` | `/approvals/{id}/reject`  | Reject an action           |
| `GET`  | `/policies`               | View active policies       |
| `PUT`  | `/policies`               | Update policies            |

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Example Policy Scenarios

## 1. Block Large Delete

```text
Action:
DELETE 500 records

Policy:
record_count > 100

Result:
❌ BLOCK
```

The tool is **never executed**.

---

## 2. Allow Small Delete

```text
Action:
DELETE 5 records

Policy:
record_count > 100

Result:
✅ ALLOW
```

The mock database tool executes.

---

## 3. Require Human Approval

```text
Action:
Send email to external domain

Policy:
external email → require_hitl

Result:
⚠️ HUMAN APPROVAL REQUIRED
```

The tool remains paused until a reviewer approves it.

---

## 4. Log and Allow

```text
Action:
Read confidential file

Policy:
path contains "confidential"

Result:
📝 LOG + ALLOW
```

The operation executes and the event is recorded.

---

# 🛡️ Security Model

The core principle is:

> **No tool action should execute before policy evaluation.**

The guardrail therefore acts as a policy enforcement point between the agent and its tools.

```text
                 UNTRUSTED
                    │
                    ▼
              AI AGENT ACTION
                    │
                    ▼
          ┌──────────────────┐
          │    GUARDRAIL     │
          └────────┬─────────┘
                   │
             Policy Check
                   │
          ┌────────┼────────┐
          ▼        ▼        ▼
        ALLOW    BLOCK     HITL
          │        │        │
          ▼        ▼        ▼
        TOOL     STOP     REVIEW
```

---

# 🐳 Docker

The backend includes Docker support.

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

The container uses:

```text
Python 3.10
```

---

# ☁️ AWS Deployment

The project is designed to be deployable beyond localhost.

Current deployment path:

```text
Local Development
       ↓
Docker
       ↓
AWS
       ↓
Production AI Governance Service
```

Potential AWS deployment architecture:

```text
                 Internet
                    │
                    ▼
              React Frontend
                    │
                    ▼
              AWS Service
                    │
                    ▼
              FastAPI API
                    │
                    ▼
            Action Guardrail
                    │
            ┌───────┼───────┐
            ▼       ▼       ▼
          Allow   Block    HITL
                    │
                    ▼
              Audit Storage
```

> AWS deployment is planned as the production deployment stage of this project.

---

# 📈 Future Enhancements

The current implementation focuses on the core Action Guardrail capability.

Planned improvements include:

* [ ] AWS deployment
* [ ] Production database
* [ ] Authentication and role-based access
* [ ] Real LLM integration
* [ ] Real agent framework integration
* [ ] More advanced policy operators
* [ ] Policy versioning
* [ ] Policy simulation mode
* [ ] Real-time WebSocket events
* [ ] Advanced risk scoring
* [ ] Alerting for repeated violations
* [ ] Container orchestration
* [ ] CI/CD with GitHub Actions
* [ ] Production observability

---

# 🧪 Validation Matrix

| Scenario               | Expected Result | Status |
| ---------------------- | --------------- | ------ |
| Delete 500 records     | Block           | ✅      |
| Delete 5 records       | Execute         | ✅      |
| External email         | HITL            | ✅      |
| Approve HITL request   | Execute         | ✅      |
| Reject HITL request    | Block           | ✅      |
| Confidential file read | Log + Allow     | ✅      |
| Audit event creation   | Recorded        | ✅      |
| Health endpoint        | Healthy         | ✅      |
| React dashboard        | Operational     | ✅      |

---

# 🎓 Learning Outcomes

This project demonstrates practical experience with:

* Agentic AI governance
* Runtime AI security
* Policy enforcement
* Human-in-the-loop systems
* REST API development
* FastAPI
* React
* YAML-based policy management
* Audit logging
* SQLite
* Automated testing
* Docker
* Cloud deployment architecture

---

# 👨‍💻 Author

**Karthikeyan M A**

B.Tech — Artificial Intelligence & Data Science

Interested in:

```text
AI/ML • Agentic AI • Software Development
Backend Engineering • Cloud • AI Security
```

---

# ⭐ Project Goal

The goal of this project is simple:

> **Let AI agents be autonomous — without letting them become uncontrolled.**

```text
        AUTONOMY
           +
        GOVERNANCE
           =
    TRUSTWORTHY AI AGENTS
```

---

## 📌 Project Status

**Current Stage:** 🟢 Local Development Complete

**Backend:** ✅ FastAPI

**Frontend:** ✅ React + Vite

**Policy Engine:** ✅

**HITL:** ✅

**Audit Logging:** ✅

**Testing:** ✅

**Docker:** 🔄

**AWS Deployment:** 🔜

---

### ⭐ If you find this project useful, consider giving the repository a star.
