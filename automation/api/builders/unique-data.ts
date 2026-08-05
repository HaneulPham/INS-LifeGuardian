import { randomUUID } from 'node:crypto';

export function uniqueTestValue(caseId: string, label: string): string {
  const safeCase = caseId.replace(/[^A-Za-z0-9-]/g, '-');
  const safeLabel = label.replace(/[^A-Za-z0-9-]/g, '-');
  return `AUT-${safeCase}-${safeLabel}-${Date.now()}-${randomUUID().slice(0, 8)}`;
}
