from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "agent.yaml", "SOUL.md", "README.md", "RULES.md", "DUTIES.md", "AGENTS.md",
    "EXPLAINABILITY.md", "requirements.txt", ".env.example", ".gitignore", "adapter.py",
    "core/__init__.py", "core/analysis.py", "example-input.json", "tools/inventory-dependencies.yaml",
    "tools/assess-dependency-risk.yaml", "tools/plan-risk-remediation.yaml",
    "skills/dependency-inventory/SKILL.md", "skills/risk-analysis/SKILL.md",
    "skills/remediation-planning/SKILL.md", "tests/test_analysis.py", "pytest.ini"
]
missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
print(f"Required files: {len(REQUIRED)-len(missing)}/{len(REQUIRED)} present")
if missing:
    print("Missing:", ", ".join(missing))
    sys.exit(1)
print("Readiness audit: PASS")
