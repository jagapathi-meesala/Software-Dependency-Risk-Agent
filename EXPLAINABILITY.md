# Explainability

This document describes the inputs, reasoning, outputs, limitations, failure handling, and human review expected for the agent and each tool.

## Inputs
The agent accepts dependency records supplied by the user. A record may contain package name, version, ecosystem, direct/transitive status, source, support status, and advisory identifiers or advisory matches provided by the user. Missing fields remain unknown; the agent does not silently complete them from outside sources.

## Decision
The core normalizes names and versions for display, then applies deterministic review rules. Missing versions and explicitly unpinned versions produce inventory-quality signals. Advisory matches are treated as supplied evidence only and are not independently verified. Signals are accompanied by reasons and recommended validation steps rather than presented as proof of exploitability.

## Limits
The agent does not query live vulnerability databases, inspect source code, resolve transitive dependency graphs, evaluate exploitability, or certify a system as secure. Heuristic risk labels are preliminary. An absent advisory in the input does not mean a package is vulnerability-free, and a supplied advisory ID does not prove that the recorded version is affected.

## Tool: inventory-dependencies

### Inputs and Data Sources
Accepts a list of dependency records explicitly supplied by the user.

### Decision and Reasoning
Checks required identifiers, preserves supplied version strings, and marks missing or ambiguous metadata. It does not install, resolve, or execute dependencies.

### Outputs and Evidence
Returns normalized records and inventory-quality issues tied to the original record index.

### Limits and Constraints
It cannot establish whether the inventory is complete unless the user provides a trusted source such as a lockfile and confirms its scope.

### Failure Handling
Malformed records are reported with their index; invalid input should be corrected and resubmitted. The tool must not guess missing versions.

### Human Review
A maintainer should compare the inventory with the project's manifest, lockfile, build targets, and deployed artifacts.

## Tool: assess-dependency-risk

### Inputs and Data Sources
Uses normalized dependency records and optional advisory/support metadata supplied by the user.

### Decision and Reasoning
Raises transparent signals for missing or unpinned versions and for explicitly supplied advisory matches. It does not assign unsupported CVSS scores or claim a live vulnerability lookup occurred.

### Outputs and Evidence
Returns signal labels, reasons, source fields when provided, and suggested verification steps.

### Limits and Constraints
Signals are triage hints, not a definitive risk score or proof of vulnerability. No external database is queried.

### Failure Handling
If evidence fields conflict or are incomplete, the result marks the uncertainty and asks for verification rather than resolving the conflict by assumption.

### Human Review
Verify package identity, ecosystem, affected version range, advisory date, reachability, and applicable mitigations against authoritative advisories and project context.

## Tool: plan-risk-remediation

### Inputs and Data Sources
Uses risk signals, dependency records, and constraints supplied by the user.

### Decision and Reasoning
Maps each signal to a cautious follow-up action such as pinning a tested version, checking an advisory range, reviewing maintainer support status, or adding a regression test. It does not select a fabricated replacement version.

### Outputs and Evidence
Returns an ordered checklist linked to the input records and explains why each task is suggested.

### Limits and Constraints
The plan cannot know compatibility, business impact, or release constraints unless these are supplied. It does not change files or deploy updates.

### Failure Handling
If a recommendation lacks sufficient context, the plan lists the missing information and a verification task rather than prescribing a specific version.

### Human Review
Maintainers must review changes in a staging environment, run tests and scanners, assess transitive impact, and prepare a rollback path before production rollout.

## Uncertainty and Responsible Use
All findings are bounded by input completeness and currentness. Do not interpret absence of a signal as proof of safety. Keep the manifest, lockfile, advisory evidence, tool version, outputs, and human decisions together for reproducibility. Treat any generated plan as advisory.
