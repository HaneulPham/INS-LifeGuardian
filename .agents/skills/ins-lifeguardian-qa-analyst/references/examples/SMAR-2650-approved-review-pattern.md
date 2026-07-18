# SMAR-2650 — Approved Requirement-Review Pattern

This file teaches the expected depth and structure for an INS LifeGuardian API/security ticket review. It is an analysis pattern, not a replacement for inspecting the current ticket and implementation.

## Evidence Pattern

A strong review should inspect more than the Jira summary. For SMAR-2650, the useful evidence types were:

- Current Jira description and expected behaviour
- Ticket history clarifying the exact affected methods and routes
- Parent HMAC security-remediation epic
- Existing ActivityMonitoringCriteria API documentation
- HMAC authentication usage documentation identifying endpoint consumers
- Relevant `serverless.yml`, function handlers, packaging output, and deployed API Gateway resources when available

## Weak vs Approved Reasoning

### Weak

`Risk: The API might not work correctly after merging the functions.`

### Approved

`Deployment Risk — High: Consolidating duplicate Serverless declarations may remove the /file/{Uuid} event, generate duplicate API Gateway methods, leave one method without Lambda invocation permission, or reference an unresolved authorizer import. Validate the source YAML, packaged CloudFormation, deployment events, deployed API Gateway methods, Lambda integration, and invocation permissions before runtime regression.`

### Weak

`Test invalid authentication.`

### Approved

`Verify both supported GET routes reject an API key without HMAC authentication, reject tampered or wrong-route signatures, and do not invoke the business Lambda or return criteria data. Confirm rejected requests are traceable without exposing API keys, HMAC secrets, valid signatures, or stack traces.`

## Required Review Shape

1. Requirement Summary
2. Scope
3. Missing Requirements and Gaps
4. Risk Analysis
5. Backend and Integration Impact
6. Required Validations
7. Questions
8. Proposed Test Coverage
9. Evidence Reviewed / Could Not Verify / QA Assumptions

## Quality Standard

A strong review:

- distinguishes configuration cleanup from functional implementation;
- identifies what must remain unchanged;
- finds conflicts between the ticket and older documentation;
- identifies active-consumer and backward-compatibility risk;
- analyses API Gateway, Lambda, authorizer, CloudFormation, data, and logs;
- states exact observable validation rather than `works correctly`;
- labels assumptions and unavailable evidence;
- does not generate detailed test cases before approval of the analysis and groups.
