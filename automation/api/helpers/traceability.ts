const CASE_ID = /^(?:SMAR|MA)-\d+-G\d+-\d{2}$/;
const REQUIREMENT_ID = /^R\d+$/;

export type ApiCaseMetadata = {
  caseId: string;
  requirements?: string[];
  endpoint?: string;
  method?: string;
  tags?: string[];
};

export function apiTestTitle(caseId: string, behavior: string): string {
  if (!CASE_ID.test(caseId)) throw new Error(`Invalid QA test-case ID: ${caseId}`);
  if (!behavior.startsWith('Verify ')) throw new Error('API automation behavior must begin with "Verify ".');
  return `${caseId} ${behavior}`;
}

export function apiCaseDetails(metadata: ApiCaseMetadata) {
  if (!CASE_ID.test(metadata.caseId)) throw new Error(`Invalid QA test-case ID: ${metadata.caseId}`);
  const requirements = metadata.requirements ?? [];
  for (const requirement of requirements) {
    if (!REQUIREMENT_ID.test(requirement)) throw new Error(`Invalid Requirement ID: ${requirement}`);
  }
  const ticket = metadata.caseId.match(/^(?:SMAR|MA)-\d+/)?.[0];
  const group = metadata.caseId.match(/-G\d+-/)?.[0].replaceAll('-', '');
  const tags = new Set([`@${metadata.caseId}`, `@${ticket}`, group ? `@${group}` : '', '@api', ...(metadata.tags ?? [])].filter(Boolean));
  return {
    tag: [...tags],
    annotation: [
      { type: 'qa-test-case', description: metadata.caseId },
      ...(requirements.length ? [{ type: 'requirement', description: requirements.join(', ') }] : []),
      ...(metadata.endpoint ? [{ type: 'endpoint', description: metadata.endpoint }] : []),
      ...(metadata.method ? [{ type: 'method', description: metadata.method.toUpperCase() }] : []),
    ],
  };
}
