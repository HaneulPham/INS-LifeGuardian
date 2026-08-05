import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const tests = path.join(root, 'tests');
const failures = [];
const forbidden = [
  ['browser fixture', /\b(?:page|browser|context)\s*[,}:]/],
  ['locator API', /\b(?:locator|getByRole|getByLabel|getByText|getByTestId)\s*\(/],
  ['arbitrary wait', /waitForTimeout\s*\(/],
  ['focused test', /\btest\.only\s*\(/],
  ['serial mode', /mode\s*:\s*['"]serial['"]/],
];
function walk(dir) {
  if (!fs.existsSync(dir)) return;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) { walk(full); continue; }
    if (!entry.name.endsWith('.ts')) continue;
    const relative = path.relative(root, full);
    if (entry.name.includes('.spec.') && !entry.name.endsWith('.api.spec.ts')) failures.push(`${relative}: spec file must end with .api.spec.ts`);
    const text = fs.readFileSync(full, 'utf8');
    for (const [label, pattern] of forbidden) if (pattern.test(text)) failures.push(`${relative}: ${label} is forbidden in API automation`);
    if (entry.name.endsWith('.api.spec.ts')) {
      if (!/apiTestTitle\s*\(/.test(text)) failures.push(`${relative}: use apiTestTitle()`);
      if (!/apiCaseDetails\s*\(/.test(text)) failures.push(`${relative}: use apiCaseDetails()`);
      if (!/cleanup/.test(text)) failures.push(`${relative}: declare or explicitly document cleanup`);
    }
  }
}
walk(tests);
if (failures.length) {
  failures.forEach(item => console.error(`FAIL ${item}`));
  process.exit(1);
}
console.log('PASS API-only automation architecture');
