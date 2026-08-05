# INS LifeGuardian Playwright API Automation

API-only TypeScript automation for approved INS LifeGuardian manual API cases. Web/browser automation will be a separate future project.

## Safety boundary

- Approved non-production environments only.
- No browser, page, locator, screenshot, or visual-test code.
- No hard-coded credentials, tokens, personal data, health data, production identifiers, or production URLs.
- No endpoint, payload, status, schema, auth, or business behavior may be invented.
- Every test maps to an approved manual case ID.

## Setup

```bash
cd automation/api
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install
cp .env.example .env   # keep .env local and ignored
```

Set `API_ENVIRONMENT`, `API_BASE_URL`, and only the credential variables required by the approved auth contract.

## Validate without live API access

```bash
npm run validate
```

This performs TypeScript compilation, secret scanning, mapping/traceability checks, API-only architecture checks, and Playwright test discovery. It does not claim live API execution.

## Run

```bash
npm test
npm run test:smoke
npm run test:regression
npm run test:case -- SMAR-2651-G2-01
npm run test:ticket -- SMAR-2651
```

## Structure

- `config/` — environment and path safety
- `fixtures/` — isolated request contexts and cleanup
- `clients/` — transport wrappers; no invented module routes
- `builders/` — unique safe test data
- `helpers/` — assertions, polling, redaction, traceability
- `schemas/` — shared JSON types and approved schemas
- `tests/` — executable `.api.spec.ts` files
- `templates/` — non-executable starting patterns
- `mappings/automation-map.json` — executable automation mapping
- `reports/` — generated and ignored

## Test metadata

Use `<CASE-ID> Verify ...` titles and `apiCaseDetails()` annotations/tags. Store manual-case automation status separately from manual case approval.

## Mapping statuses

`Candidate`, `Automated`, `Partially Automated`, `Blocked`, `Not Suitable`, `Maintenance Required`.

Use `update API automation mapping` only after review or execution evidence.
