"""Deterministic, local-only software dependency risk triage helpers."""
from __future__ import annotations

from typing import Any


def inventory_dependencies(dependencies: Any) -> dict[str, Any]:
    if not isinstance(dependencies, list):
        raise ValueError("dependencies must be a list")
    records: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    seen: dict[tuple[str, str], int] = {}
    for index, item in enumerate(dependencies):
        if not isinstance(item, dict):
            issues.append({"record_index": index, "issue": "record_not_object"})
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name.strip():
            issues.append({"record_index": index, "issue": "missing_package_name"})
            continue
        version = item.get("version")
        version_text = version.strip() if isinstance(version, str) else ""
        ecosystem = item.get("ecosystem", "unknown")
        ecosystem = ecosystem.strip().lower() if isinstance(ecosystem, str) and ecosystem.strip() else "unknown"
        normalized = {
            "record_index": index,
            "name": name.strip(),
            "normalized_name": name.strip().lower(),
            "version": version_text or None,
            "ecosystem": ecosystem,
            "directness": item.get("directness", "unknown"),
            "source": item.get("source"),
            "version_pinned": bool(version_text) and not any(ch in version_text for ch in ("*", ">", "<", "^", "~", "x", "X")),
            "support_status": item.get("support_status", "unknown"),
            "advisories": item.get("advisories", []),
        }
        if not version_text:
            issues.append({"record_index": index, "issue": "missing_version", "name": name.strip()})
        if not normalized["version_pinned"]:
            issues.append({"record_index": index, "issue": "version_not_pinned_or_unknown", "name": name.strip()})
        key = (normalized["normalized_name"], ecosystem)
        if key in seen:
            issues.append({"record_index": index, "issue": "possible_duplicate", "name": name.strip(), "first_record_index": seen[key]})
        else:
            seen[key] = index
        if not isinstance(normalized["advisories"], list):
            normalized["advisories"] = []
            issues.append({"record_index": index, "issue": "advisories_not_list", "name": name.strip()})
        records.append(normalized)
    return {"dependencies": records, "inventory_issues": issues, "record_count": len(records)}


def assess_dependency_risk(dependencies: Any) -> dict[str, Any]:
    inventory = inventory_dependencies(dependencies)
    findings: list[dict[str, Any]] = []
    for dep in inventory["dependencies"]:
        signals: list[dict[str, str]] = []
        if not dep["version"]:
            signals.append({"signal": "version_unknown", "reason": "No version was supplied.", "recommended_check": "Inspect the project's resolved lockfile or artifact inventory."})
        elif not dep["version_pinned"]:
            signals.append({"signal": "version_not_pinned", "reason": "The version string appears ranged or wildcard-based under a simple heuristic.", "recommended_check": "Confirm resolved versions from the lockfile and assess reproducible-build requirements."})
        support = str(dep.get("support_status", "unknown")).strip().lower()
        if support in {"eol", "unsupported", "end-of-life", "deprecated"}:
            signals.append({"signal": "support_status_review", "reason": f"Input marks support status as '{support}'. This was not independently verified.", "recommended_check": "Verify lifecycle status from the upstream maintainer's official policy."})
        for advisory in dep.get("advisories", []):
            if isinstance(advisory, str) and advisory.strip():
                signals.append({"signal": "supplied_advisory_reference", "reason": f"Input includes advisory reference '{advisory.strip()}'; its validity and affected range are not independently verified.", "recommended_check": "Check the advisory from an authoritative source and compare its affected-version range with the resolved version."})
            elif isinstance(advisory, dict):
                ref = advisory.get("id") or advisory.get("url") or "unidentified advisory record"
                signals.append({"signal": "supplied_advisory_reference", "reason": f"Input includes {ref}; affected status is not independently verified.", "recommended_check": "Verify package identity, affected range, severity, and mitigation using the advisory publisher."})
        if signals:
            findings.append({"record_index": dep["record_index"], "name": dep["name"], "version": dep["version"], "ecosystem": dep["ecosystem"], "signals": signals})
    return {
        "findings": findings,
        "inventory_issues": inventory["inventory_issues"],
        "summary": {"dependencies_reviewed": inventory["record_count"], "dependencies_with_signals": len(findings)},
        "interpretation": "Heuristic triage only. No external vulnerability database was queried and no dependency is declared safe or vulnerable by this result."
    }


def plan_risk_remediation(assessment: Any) -> dict[str, Any]:
    if not isinstance(assessment, dict) or not isinstance(assessment.get("findings", []), list):
        raise ValueError("assessment must be an object with a findings list")
    tasks: list[dict[str, Any]] = []
    for finding in assessment.get("findings", []):
        if not isinstance(finding, dict):
            continue
        name = finding.get("name", "unknown dependency")
        for signal in finding.get("signals", []):
            if not isinstance(signal, dict):
                continue
            kind = signal.get("signal", "review_signal")
            action = {
                "version_unknown": "Resolve the dependency version from a trusted lockfile or build artifact.",
                "version_not_pinned": "Check the resolved dependency and decide whether a reproducible pin is required.",
                "support_status_review": "Verify lifecycle status from the official upstream maintainer source and evaluate a supported alternative if needed.",
                "supplied_advisory_reference": "Verify the advisory identity and affected-version range using an authoritative source before classifying impact.",
            }.get(kind, "Review the evidence and determine the next verification step.")
            tasks.append({"dependency": name, "record_index": finding.get("record_index"), "signal": kind, "action": action, "evidence_note": signal.get("reason", "")})
    tasks.append({"dependency": "project-wide", "record_index": None, "signal": "validation_and_rollback", "action": "After any dependency change, run tests, rebuild in a clean environment, scan the resolved dependency graph, and prepare a rollback plan before deployment.", "evidence_note": "Standard release safeguard; no dependency changes are performed by this agent."})
    return {"tasks": tasks, "requires_human_approval": True}
