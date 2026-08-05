import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const source = process.argv[2] ? path.resolve(process.argv[2]) : path.join(root, 'reports', 'results.json');
if (!fs.existsSync(source)) {
  console.error(`Result file does not exist: ${source}`);
  process.exit(1);
}
const report = JSON.parse(fs.readFileSync(source, 'utf8'));
const counts = { passed: 0, failed: 0, flaky: 0, skipped: 0 };
function visitSuite(suite) {
  for (const spec of suite.specs || []) {
    for (const test of spec.tests || []) {
      const results = test.results || [];
      const last = results.at(-1);
      if (!last) { counts.skipped += 1; continue; }
      if (last.status === 'passed' && results.length > 1) counts.flaky += 1;
      else if (last.status === 'passed') counts.passed += 1;
      else if (last.status === 'skipped') counts.skipped += 1;
      else counts.failed += 1;
    }
  }
  for (const child of suite.suites || []) visitSuite(child);
}
for (const suite of report.suites || []) visitSuite(suite);
const output = [
  '# API Automation Execution Summary', '',
  `- Passed: ${counts.passed}`,
  `- Failed: ${counts.failed}`,
  `- Flaky: ${counts.flaky}`,
  `- Skipped: ${counts.skipped}`,
  `- Source: ${path.relative(root, source)}`, '',
].join('\n');
const target = path.join(root, 'reports', 'summary.md');
fs.mkdirSync(path.dirname(target), { recursive: true });
fs.writeFileSync(target, output);
console.log(output);
