import pytest
from core.analysis import inventory_dependencies, assess_dependency_risk, plan_risk_remediation


def test_inventory_flags_missing_version():
    result = inventory_dependencies([{"name": "demo", "ecosystem": "pypi"}])
    assert result["record_count"] == 1
    assert any(item["issue"] == "missing_version" for item in result["inventory_issues"])


def test_missing_name_record_is_reported():
    result = inventory_dependencies([{"version": "1.0"}])
    assert result["record_count"] == 0
    assert result["inventory_issues"][0]["issue"] == "missing_package_name"


def test_pinned_version_does_not_trigger_pin_signal():
    result = assess_dependency_risk([{"name": "demo", "version": "1.2.3", "ecosystem": "pypi"}])
    assert result["findings"] == []


def test_range_version_triggers_signal():
    result = assess_dependency_risk([{"name": "demo", "version": "^1.2.3", "ecosystem": "npm"}])
    assert result["findings"][0]["signals"][0]["signal"] == "version_not_pinned"


def test_supplied_advisory_is_not_claimed_verified():
    result = assess_dependency_risk([{"name": "demo", "version": "1.0", "advisories": ["GHSA-example"]}])
    reason = result["findings"][0]["signals"][0]["reason"]
    assert "not independently verified" in reason
    assert "was queried" in result["interpretation"]


def test_eol_input_is_review_signal():
    result = assess_dependency_risk([{"name": "demo", "version": "1.0", "support_status": "eol"}])
    assert any(s["signal"] == "support_status_review" for s in result["findings"][0]["signals"])


def test_plan_includes_human_approval_and_tests():
    assessment = assess_dependency_risk([{"name": "demo"}])
    plan = plan_risk_remediation(assessment)
    assert plan["requires_human_approval"] is True
    assert any(task["signal"] == "validation_and_rollback" for task in plan["tasks"])


def test_invalid_input_rejected():
    with pytest.raises(ValueError):
        inventory_dependencies({"name": "not-a-list"})
