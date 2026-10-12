"""Small CLI adapter for local JSON inputs; performs no network calls."""
import json
import sys
from pathlib import Path
from core.analysis import assess_dependency_risk, plan_risk_remediation


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python adapter.py <input.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        assessment = assess_dependency_risk(data.get("dependencies", []))
        result = {"assessment": assessment, "remediation_plan": plan_risk_remediation(assessment)}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
