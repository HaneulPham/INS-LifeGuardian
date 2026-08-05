# Authentication and authorization

- Use environment variables for tokens, client credentials, API keys, and custom auth headers.
- Never commit `.env`, storage state, tokens, cookies, credentials, private keys, or production identifiers.
- Keep unauthenticated and authenticated request contexts separate.
- Use distinct approved accounts for roles/tenants where authorization is tested.
- Verify both response denial and no persistence/downstream side effect when evidence supports it.
- Test cross-client and cross-tenant boundaries only with approved isolated data.
- Redact authorization headers and sensitive fields from reports and debug output.
- Reject `API_ENVIRONMENT=production` and production-like URLs. Do not bypass this gate silently.
- When token creation or refresh is not documented, report the missing contract instead of inventing an auth flow.
