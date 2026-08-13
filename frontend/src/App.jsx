import { useEffect, useState } from "react";

import {
  ShieldCheck,
  ShieldAlert,
  Activity,
  Ban,
  Clock3,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Database,
  Mail,
  FileText,
  LayoutDashboard,
  ScrollText,
  Settings,
  ChevronRight,
} from "lucide-react";

import "./App.css";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("dashboard");

  const [health, setHealth] = useState(false);
  const [logs, setLogs] = useState([]);
  const [approvals, setApprovals] = useState([]);
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);

    try {
      const healthResponse = await fetch(`${API}/health`);
      setHealth(healthResponse.ok);

      const auditResponse = await fetch(`${API}/audit`);
      const auditData = await auditResponse.json();
      setLogs(auditData.logs || []);

      const approvalResponse = await fetch(`${API}/approvals`);
      const approvalData = await approvalResponse.json();
      setApprovals(approvalData.approvals || []);

      const policyResponse = await fetch(`${API}/policies`);
      const policyData = await policyResponse.json();
      setPolicies(policyData.policies || []);

    } catch (error) {
      console.error("Backend connection failed:", error);
      setHealth(false);
    }

    setLoading(false);
  };

  useEffect(() => {
    fetchData();

    const interval = setInterval(fetchData, 3000);

    return () => clearInterval(interval);
  }, []);

  const approve = async (id) => {
    try {
      await fetch(`${API}/approvals/${id}/approve`, {
        method: "POST",
      });

      await fetchData();

    } catch (error) {
      console.error(error);
    }
  };

  const reject = async (id) => {
    try {
      await fetch(`${API}/approvals/${id}/reject`, {
        method: "POST",
      });

      await fetchData();

    } catch (error) {
      console.error(error);
    }
  };

  const blockedCount = logs.filter(
    (log) => log.outcome === "block"
  ).length;

  const allowedCount = logs.filter(
    (log) =>
      log.outcome === "allow" ||
      log.outcome === "log_and_allow" ||
      log.outcome === "approved_and_executed"
  ).length;

  return (
    <div className="app">

      {/* SIDEBAR */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            <ShieldCheck size={25} />
          </div>

          <div>
            <h2>Guardrail</h2>
            <span>AI Governance</span>
          </div>

        </div>


        <nav>

          <NavItem
            icon={<LayoutDashboard size={18} />}
            label="Dashboard"
            active={page === "dashboard"}
            onClick={() => setPage("dashboard")}
          />

          <NavItem
            icon={<ShieldAlert size={18} />}
            label="Policies"
            active={page === "policies"}
            onClick={() => setPage("policies")}
          />

          <NavItem
            icon={<Clock3 size={18} />}
            label="Approvals"
            active={page === "approvals"}
            badge={approvals.length}
            onClick={() => setPage("approvals")}
          />

          <NavItem
            icon={<ScrollText size={18} />}
            label="Audit Logs"
            active={page === "audit"}
            onClick={() => setPage("audit")}
          />

        </nav>


        <div className="sidebar-bottom">

          <div className="system-status">

            <span
              className={`status-dot ${
                health ? "online" : "offline"
              }`}
            />

            <div>
              <strong>
                {health ? "System Online" : "Offline"}
              </strong>

              <small>
                {health
                  ? "FastAPI connected"
                  : "Backend unavailable"}
              </small>
            </div>

          </div>

        </div>

      </aside>


      {/* MAIN */}

      <main className="main">

        <header className="header">

          <div>

            <h1>
              {page === "dashboard" && "Action Guardrail"}

              {page === "policies" && "Policy Management"}

              {page === "approvals" && "Human Approvals"}

              {page === "audit" && "Audit Logs"}
            </h1>

            <p>
              {page === "dashboard" &&
                "Runtime policy enforcement for AI agents"}

              {page === "policies" &&
                "Policies currently enforced by the guardrail"}

              {page === "approvals" &&
                "Review high-risk agent actions"}

              {page === "audit" &&
                "Complete history of evaluated agent actions"}
            </p>

          </div>


          <button
            className="refresh-button"
            onClick={fetchData}
          >

            <RefreshCw
              size={17}
              className={loading ? "spin" : ""}
            />

            Refresh

          </button>

        </header>


        {/* PAGE CONTENT */}

        {page === "dashboard" && (
          <Dashboard
            logs={logs}
            approvals={approvals}
            blockedCount={blockedCount}
            allowedCount={allowedCount}
          />
        )}


        {page === "policies" && (
          <Policies policies={policies} />
        )}


        {page === "approvals" && (
          <Approvals
            approvals={approvals}
            approve={approve}
            reject={reject}
          />
        )}


        {page === "audit" && (
          <AuditLogs logs={logs} />
        )}

      </main>

    </div>
  );
}


/* =========================================
   NAVIGATION ITEM
========================================= */

function NavItem({
  icon,
  label,
  active,
  badge,
  onClick,
}) {
  return (
    <button
      className={`nav-item ${active ? "active" : ""}`}
      onClick={onClick}
    >

      {icon}

      <span>{label}</span>

      {badge > 0 && (
        <span className="nav-badge">
          {badge}
        </span>
      )}

    </button>
  );
}


/* =========================================
   DASHBOARD
========================================= */

function Dashboard({
  logs,
  approvals,
  blockedCount,
  allowedCount,
}) {
  return (
    <>

      <section className="stats">

        <StatCard
          title="Total Actions"
          value={logs.length}
          icon={<Activity size={21} />}
        />

        <StatCard
          title="Allowed"
          value={allowedCount}
          icon={<CheckCircle2 size={21} />}
        />

        <StatCard
          title="Blocked"
          value={blockedCount}
          icon={<Ban size={21} />}
        />

        <StatCard
          title="Pending HITL"
          value={approvals.length}
          icon={<Clock3 size={21} />}
        />

      </section>


      <section className="content-grid">

        <div className="panel">

          <div className="panel-header">

            <div>
              <h2>Pending Approvals</h2>

              <p>
                Human-in-the-loop actions
              </p>
            </div>

            <span className="count-badge">
              {approvals.length}
            </span>

          </div>


          <ApprovalList
            approvals={approvals}
          />

        </div>


        <div className="panel">

          <div className="panel-header">

            <div>
              <h2>Guardrail Flow</h2>

              <p>
                Action evaluation pipeline
              </p>
            </div>

          </div>


          <div className="flow">

            <FlowStep
              icon={<Activity />}
              title="AI Agent"
              text="Tool request"
            />

            <div className="arrow">↓</div>

            <FlowStep
              icon={<ShieldCheck />}
              title="Policy Engine"
              text="Evaluate action"
            />

            <div className="arrow">↓</div>

            <div className="decision-row">

              <Decision
                label="ALLOW"
                type="allow"
              />

              <Decision
                label="BLOCK"
                type="block"
              />

              <Decision
                label="HITL"
                type="hitl"
              />

            </div>

          </div>

        </div>

      </section>


      <AuditTable
        logs={logs.slice(0, 10)}
      />

    </>
  );
}


/* =========================================
   POLICIES
========================================= */

function Policies({ policies }) {
  return (
    <section className="panel">

      <div className="panel-header">

        <div>
          <h2>Active Policies</h2>

          <p>
            Rules loaded from policy.yaml
          </p>
        </div>

        <span className="count-badge">
          {policies.length}
        </span>

      </div>


      {policies.length === 0 ? (

        <div className="empty">

          <ShieldAlert size={35} />

          <p>No policies found</p>

        </div>

      ) : (

        <div className="policy-list">

          {policies.map((policy) => (

            <div
              className="policy-card"
              key={policy.name}
            >

              <div className="policy-icon">
                <ShieldAlert size={19} />
              </div>


              <div className="policy-info">

                <strong>
                  {policy.name}
                </strong>

                <span>
                  Tool: {policy.tool}
                </span>

                <span>
                  Operation: {policy.operation}
                </span>

                <small>
                  {policy.reason}
                </small>

              </div>


              <div
                className={`policy-action ${policy.action}`}
              >
                {policy.action.replaceAll("_", " ")}
              </div>

            </div>

          ))}

        </div>

      )}

    </section>
  );
}


/* =========================================
   APPROVALS
========================================= */

function Approvals({
  approvals,
  approve,
  reject,
}) {
  return (
    <section className="panel">

      <div className="panel-header">

        <div>
          <h2>Pending Human Review</h2>

          <p>
            High-risk actions waiting for approval
          </p>
        </div>

        <span className="count-badge">
          {approvals.length}
        </span>

      </div>


      {approvals.length === 0 ? (

        <div className="empty">

          <CheckCircle2 size={38} />

          <p>No pending approvals</p>

          <span>
            There are no actions waiting for human review.
          </span>

        </div>

      ) : (

        <div className="approval-page-list">

          {approvals.map((approval) => (

            <div
              className="approval-full-card"
              key={approval.id}
            >

              <div className="approval-main">

                <div className="approval-icon">
                  <Mail size={21} />
                </div>

                <div>

                  <h3>
                    {approval.operation}
                  </h3>

                  <p>
                    Approval ID: #{approval.id}
                  </p>

                </div>

              </div>


              <div className="approval-details">

                <Detail
                  label="Agent"
                  value={approval.agent_id}
                />

                <Detail
                  label="Tool"
                  value={approval.tool_name}
                />

                <Detail
                  label="Operation"
                  value={approval.operation}
                />

                <Detail
                  label="Session"
                  value={approval.session_id}
                />

              </div>


              <div className="parameters">

                <strong>Parameters</strong>

                <pre>
                  {JSON.stringify(
                    approval.parameters,
                    null,
                    2
                  )}
                </pre>

              </div>


              <div className="approval-actions-large">

                <button
                  className="approve"
                  onClick={() =>
                    approve(approval.id)
                  }
                >
                  <CheckCircle2 size={16} />
                  Approve & Execute
                </button>

                <button
                  className="reject"
                  onClick={() =>
                    reject(approval.id)
                  }
                >
                  <XCircle size={16} />
                  Reject Action
                </button>

              </div>

            </div>

          ))}

        </div>

      )}

    </section>
  );
}


/* =========================================
   AUDIT LOGS
========================================= */

function AuditLogs({ logs }) {

  const [search, setSearch] = useState("");

  const filteredLogs = logs.filter((log) => {

    const text = `
      ${log.agent_id}
      ${log.tool}
      ${log.operation}
      ${log.outcome}
      ${log.reason}
    `.toLowerCase();

    return text.includes(search.toLowerCase());

  });


  return (
    <section className="panel">

      <div className="panel-header">

        <div>
          <h2>Audit Trail</h2>

          <p>
            Every evaluated action is recorded
          </p>
        </div>

        <span className="live-label">
          ● LIVE
        </span>

      </div>


      <div className="audit-toolbar">

        <input
          type="text"
          placeholder="Search agent, tool, operation..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
        />

      </div>


      <AuditTable logs={filteredLogs} />

    </section>
  );
}


/* =========================================
   AUDIT TABLE
========================================= */

function AuditTable({ logs }) {

  if (logs.length === 0) {

    return (
      <div className="empty">

        <Database size={32} />

        <p>No audit events yet</p>

      </div>
    );
  }


  return (
    <div className="table-wrapper">

      <table>

        <thead>

          <tr>
            <th>ID</th>
            <th>Agent</th>
            <th>Tool</th>
            <th>Operation</th>
            <th>Outcome</th>
            <th>Reason</th>
            <th>Time</th>
          </tr>

        </thead>


        <tbody>

          {logs.map((log) => (

            <tr key={log.id}>

              <td>
                #{log.id}
              </td>

              <td>
                <strong>
                  {log.agent_id}
                </strong>
              </td>

              <td>
                <span className="tool">
                  {log.tool}
                </span>
              </td>

              <td>
                {log.operation}
              </td>

              <td>
                <OutcomeBadge
                  outcome={log.outcome}
                />
              </td>

              <td className="reason">
                {log.reason}
              </td>

              <td className="time">
                {formatTime(log.timestamp)}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}


/* =========================================
   COMPONENTS
========================================= */

function StatCard({
  title,
  value,
  icon,
}) {
  return (
    <div className="stat-card">

      <div className="stat-icon">
        {icon}
      </div>

      <div>
        <span>{title}</span>
        <strong>{value}</strong>
      </div>

    </div>
  );
}


function ApprovalList({ approvals }) {

  if (approvals.length === 0) {

    return (
      <div className="empty">

        <CheckCircle2 size={35} />

        <p>No pending approvals</p>

        <span>
          All high-risk actions have been reviewed.
        </span>

      </div>
    );
  }


  return (
    <div className="approval-list">

      {approvals.slice(0, 5).map((approval) => (

        <div
          className="approval-card"
          key={approval.id}
        >

          <div className="approval-icon">
            <Mail size={20} />
          </div>

          <div className="approval-info">

            <strong>
              {approval.operation}
            </strong>

            <span>
              Agent: {approval.agent_id}
            </span>

            <span>
              Tool: {approval.tool_name}
            </span>

          </div>

        </div>

      ))}

    </div>
  );
}


function Detail({
  label,
  value,
}) {
  return (
    <div className="detail">

      <span>{label}</span>

      <strong>
        {value || "-"}
      </strong>

    </div>
  );
}


function FlowStep({
  icon,
  title,
  text,
}) {
  return (
    <div className="flow-step">

      <div className="flow-icon">
        {icon}
      </div>

      <div>
        <strong>{title}</strong>
        <span>{text}</span>
      </div>

    </div>
  );
}


function Decision({
  label,
  type,
}) {
  return (
    <div className={`decision ${type}`}>
      {label}
    </div>
  );
}


function OutcomeBadge({
  outcome,
}) {

  let type = "allow";

  if (
    outcome === "block" ||
    outcome === "rejected"
  ) {
    type = "block";
  }

  if (
    outcome === "require_hitl"
  ) {
    type = "hitl";
  }

  return (
    <span className={`outcome ${type}`}>
      {outcome.replaceAll("_", " ")}
    </span>
  );
}


function formatTime(timestamp) {

  if (!timestamp) {
    return "-";
  }

  return new Date(
    timestamp
  ).toLocaleString();
}


export default App;