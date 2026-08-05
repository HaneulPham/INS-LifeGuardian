# API automation failure classification

Classify before fixing:

| Classification | Use when | Next action |
|---|---|---|
| Product Defect | Product contradicts approved behavior with valid data/environment | Preserve assertion; draft evidence-backed bug |
| Automation Defect | Code, fixture, assertion, cleanup, or mapping is wrong | Fix automation and rerun narrow scope |
| Test Data Failure | Data missing, invalid, stale, shared, or not cleaned | Repair data setup/cleanup; do not weaken behavior |
| Authentication Failure | Token/account/session creation or expiry failed | Verify auth contract and environment |
| Authorization Failure | Role/tenant access differs from approved rule | Distinguish product defect from wrong test identity |
| Environment Failure | Service, deployment, DNS, configuration, or dependency unavailable | Report environment evidence; do not claim product defect |
| Dependency Failure | Confirmed external/internal dependency failed | Verify expected degraded behavior and logs |
| Requirement Conflict | Sources define different outcomes | Stop affected assertion changes; record conflict/question |
| Could Not Verify | Required evidence is unavailable | Name missing evidence and affected cases |
| Requires Test Instrumentation | Behavior has no approved observable signal | Request exact instrumentation |
| Flaky Under Investigation | Failure is intermittent and classification is not proven | Capture repeats/evidence; do not hide with retries |

A retry pass is evidence of flakiness, not proof that the product is correct.
