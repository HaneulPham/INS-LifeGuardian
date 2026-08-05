# Assertions and observability

Assert the strongest accessible approved evidence:

1. exact status code and response contract;
2. material response fields and identifiers;
3. headers/correlation ID where required;
4. persistence-visible GET or supported API readback;
5. approved audit, notification, queue, job, report, or integration evidence.

Rules:

- Parse JSON only when the content type supports it.
- Include a redacted response excerpt in failure messages, never raw secrets or client/health data.
- For negative cases, verify the approved error schema and no partial persistence or unintended trigger.
- For asynchronous behavior, poll a supported observable endpoint with a bounded timeout and interval defined by confirmed timing behavior.
- Do not use arbitrary delays or assert inaccessible internal implementation.
- Mark unavailable essential evidence `Requires Test Instrumentation` and name the exact log, endpoint, event, or field needed.
