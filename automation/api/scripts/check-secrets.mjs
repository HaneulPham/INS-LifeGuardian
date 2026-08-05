import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const skip = new Set(['node_modules', 'reports', '.git']);
const allowedFiles = new Set(['.env.example', 'package-lock.json']);
const forbiddenNames = [/^\.env(?:\..+)?$/, /\.pem$/i, /\.key$/i, /\.p12$/i, /\.pfx$/i];
const patterns = [
  ['private key', /-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/],
  ['AWS access key', /\bAKIA[0-9A-Z]{16}\b/],
  ['hard-coded bearer token', /Authorization\s*[:=]\s*['"]Bearer\s+[A-Za-z0-9._~+\/-]{20,}['"]/i],
  ['hard-coded secret', /\b(?:password|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['"][^'"\n]{8,}['"]/i],
];
const failures = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (skip.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    const relative = path.relative(root, full);
    if (entry.isDirectory()) { walk(full); continue; }
    if (!allowedFiles.has(entry.name) && forbiddenNames.some(pattern => pattern.test(entry.name))) {
      failures.push(`${relative}: forbidden credential file`);
      continue;
    }
    if (allowedFiles.has(entry.name) || entry.name.endsWith('.json')) continue;
    const text = fs.readFileSync(full, 'utf8');
    for (const [label, pattern] of patterns) if (pattern.test(text)) failures.push(`${relative}: ${label}`);
  }
}
walk(root);
if (failures.length) {
  failures.forEach(item => console.error(`FAIL ${item}`));
  process.exit(1);
}
console.log('PASS no committed secrets detected');
