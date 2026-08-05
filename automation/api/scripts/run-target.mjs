import { spawnSync } from 'node:child_process';

const [mode, target] = process.argv.slice(2);
if (!['case', 'ticket'].includes(mode) || !target) {
  console.error('Usage: node scripts/run-target.mjs <case|ticket> <ID>');
  process.exit(2);
}
const pattern = mode === 'case'
  ? /^(?:SMAR|MA)-\d+-G\d+-\d{2}$/
  : /^(?:SMAR|MA)-\d+$/;
if (!pattern.test(target)) {
  console.error(`Invalid ${mode} ID: ${target}`);
  process.exit(2);
}
const envCheck = spawnSync(process.execPath, ['scripts/validate-environment.mjs'], { stdio: 'inherit' });
if (envCheck.status !== 0) process.exit(envCheck.status ?? 1);
const result = spawnSync(process.platform === 'win32' ? 'npx.cmd' : 'npx', ['playwright', 'test', '--grep', `@${target}`], { stdio: 'inherit' });
process.exit(result.status ?? 1);
