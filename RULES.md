# Rules
- Work only from supplied dependency metadata and explicitly supplied advisory evidence.
- Never invent package versions, CVEs, severity scores, support dates, or upstream status.
- Label heuristic findings as review signals, not confirmed vulnerabilities.
- Keep the original package name and version alongside normalized values.
- Prefer minimal, reversible remediation and require tests before rollout.
- Do not execute dependency code or alter the user's environment.
