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


def test_report_exists_and_is_valid_json():
    """The agent produced /app/report.json containing valid JSON."""
    data = _load_report()
    assert isinstance(data, dict)


def test_report_has_exact_schema():
    """report.json has exactly the three required keys, no more, no less."""
    data = _load_report()
    assert set(data.keys()) == {"total_requests", "unique_ips", "top_path"}


def test_total_requests_correct():
    """total_requests matches the true non-empty line count of the access log."""
    data = _load_report()
    assert isinstance(data["total_requests"], int)
    assert data["total_requests"] == EXPECTED["total_requests"]


def test_unique_ips_correct():
    """unique_ips matches the true count of distinct client IPs."""
    data = _load_report()
    assert isinstance(data["unique_ips"], int)
    assert data["unique_ips"] == EXPECTED["unique_ips"]


def test_top_path_correct():
    """top_path matches the most-requested path in the access log."""
    data = _load_report()
    assert isinstance(data["top_path"], str)
    assert data["top_path"] == EXPECTED["top_path"]


def test_fixture_matches_agent_input():
    """
    Sanity check on the verifier itself: the trusted fixture log used to compute
    EXPECTED must be byte-identical to the log the agent was given, otherwise this
    verifier would be grading against the wrong ground truth.
    """
    agent_log = Path("/app/access.log")
    assert agent_log.exists(), "agent's /app/access.log is missing"
    assert agent_log.read_text() == FIXTURE_LOG.read_text(), (
        "agent's access.log differs from the trusted fixture; "
        "verifier ground truth would be invalid"
    )
