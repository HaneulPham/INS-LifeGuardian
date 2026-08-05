import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const mapPath = path.join(root, 'mappings', 'automation-map.json');
const allowedStatuses = new Set(['Candidate', 'Automated', 'Partially Automated', 'Blocked', 'Not Suitable', 'Maintenance Required']);
const casePattern = /^(?:SMAR|MA)-\d+-G\d+-\d{2}$/;
const mapping = JSON.parse(fs.readFileSync(mapPath, 'utf8'));
const failures = [];
if (mapping.schemaVersion !== 1) failures.push('schemaVersion must be 1');
if (!Array.isArray(mapping.entries)) failures.push('entries must be an array');
const seen = new Set();
for (const [index, entry] of (mapping.entries || []).entries()) {
  const label = `entries[${index}]`;
  if (!casePattern.test(entry.caseId || '')) failures.push(`${label}.caseId is invalid`);
  if (seen.has(entry.caseId)) failures.push(`${label}.caseId is duplicated`);
  seen.add(entry.caseId);
  if (!allowedStatuses.has(entry.status)) failures.push(`${label}.status is invalid`);
  if (entry.status === 'Automated') {
    for (const key of ['specFile', 'testTitle', 'endpoint', 'method']) if (!entry[key]) failures.push(`${label}.${key} is required for Automated`);
    if (entry.specFile && !fs.existsSync(path.join(root, entry.specFile))) failures.push(`${label}.specFile does not exist`);
  }
}
if (failures.length) {
  failures.forEach(item => console.error(`FAIL ${item}`));
  process.exit(1);
}
console.log(`PASS automation mapping entries=${seen.size}`);
