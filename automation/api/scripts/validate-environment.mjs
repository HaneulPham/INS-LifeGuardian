const allowed = new Set(['local', 'dev', 'test', 'qa', 'stag', 'staging', 'uat']);
const name = (process.env.API_ENVIRONMENT || '').trim().toLowerCase();
const base = (process.env.API_BASE_URL || '').trim();
const failures = [];
if (!allowed.has(name)) failures.push(`API_ENVIRONMENT must be one of: ${[...allowed].join(', ')}`);
let url;
try { url = new URL(base); } catch { failures.push('API_BASE_URL must be a valid URL'); }
if (url && /(^|[.\-_/])(prod|production)([.\-_/]|$)/i.test(`${name}/${url.hostname}/${url.pathname}`)) {
  failures.push('Production API automation is prohibited');
}
if (url && name !== 'local' && url.protocol !== 'https:') failures.push('Non-local API_BASE_URL must use HTTPS');
if (failures.length) {
  for (const failure of failures) console.error(`FAIL ${failure}`);
  process.exit(1);
}
console.log(`PASS environment=${name} baseURL=${url.origin}`);
