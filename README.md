# Software Dependency Risk Agent

A local, evidence-conscious assistant for reviewing package/dependency inventories and prioritizing software supply-chain follow-up. It uses supplied metadata and transparent heuristics; it does not replace a software composition analysis scanner or current vulnerability/advisory feeds.

## Features
- Normalize dependency inventory records.
- Flag review signals such as unknown version, unpinned version, end-of-life metadata supplied by user, or advisory matches explicitly included in input.
- Produce prioritized follow-up recommendations with reasons and uncertainty.
- No network access or package installation is performed by the core logic.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pytest -q
python3 adapter.py example-input.json
```

## OpenGAP checks
```bash
python3 verification/readiness_audit.py
opengap validate
```

## Important limitations
The heuristic output is not a CVE scan, legal/security certification, or guarantee that a dependency is safe. Validate advisory identifiers and affected-version ranges against authoritative databases and your own lockfiles/build environment. Human reviewers must approve changes and test updates before deployment.
