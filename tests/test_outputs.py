import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")

# Trusted ground truth: a copy of the access log baked into tests/, which is only
# overlaid at verify time and is never present (or readable) during the agent run.
# This means the agent cannot influence the expected values by editing /app/access.log.
FIXTURE_LOG = Path(__file__).parent / "fixtures" / "access.log"

# Expected values, computed and hand-verified independently of solution/solve.py
# (not derived by re-running the oracle), from the 6-line fixture log:
#   3x GET /index.html, 2x GET /about.html, 1x POST /api/login
#   3 distinct client IPs: 192.168.0.1, 192.168.0.2, 10.0.0.5
EXPECTED = {
    "total_requests": 6,
    "unique_ips": 3,
    "top_path": "/index.html",
}


def _load_report():
    assert REPORT_PATH.exists(), "no /app/report.json found"
    assert REPORT_PATH.stat().st_size > 0, "/app/report.json is empty"
    with open(REPORT_PATH) as f:
        return json.load(f)


def test_criterion_1_schema_exact():
    """instruction.md criterion 1: report.json exists, is valid JSON, and has
    exactly the keys total_requests, unique_ips, top_path -- no more, no less."""
    data = _load_report()
    assert isinstance(data, dict)
    assert set(data.keys()) == {"total_requests", "unique_ips", "top_path"}


def test_criterion_2_total_requests():
    """instruction.md criterion 2: total_requests equals the true non-empty
    line count of /app/access.log."""
    data = _load_report()
    assert isinstance(data["total_requests"], int)
    assert data["total_requests"] == EXPECTED["total_requests"]


def test_criterion_3_unique_ips():
    """instruction.md criterion 3: unique_ips equals the true count of
    distinct client IPs in /app/access.log."""
    data = _load_report()
    assert isinstance(data["unique_ips"], int)
    assert data["unique_ips"] == EXPECTED["unique_ips"]


def test_criterion_4_top_path():
    """instruction.md criterion 4: top_path equals the most-requested path
    in /app/access.log."""
    data = _load_report()
    assert isinstance(data["top_path"], str)
    assert data["top_path"] == EXPECTED["top_path"]


def test_criterion_5_access_log_unmodified():
    """instruction.md criterion 5: /app/access.log must be left unmodified.
    Compared against a trusted fixture copy baked into tests/ (verify-time
    only), so the agent cannot pass this by tampering with its own copy."""
    agent_log = Path("/app/access.log")
    assert agent_log.exists(), "agent's /app/access.log is missing"
    assert agent_log.read_text() == FIXTURE_LOG.read_text(), (
        "agent's access.log differs from the trusted fixture -- log was modified"
    )
