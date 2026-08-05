const ALLOWED_ENVIRONMENTS = new Set(['local', 'dev', 'test', 'qa', 'stag', 'staging', 'uat']);
const PRODUCTION_HINT = /(^|[.\-_/])(prod|production)([.\-_/]|$)/i;

export type ApiEnvironment = {
  name: string;
  baseURL: string;
  defaultTimeoutMs: number;
  pollIntervalMs: number;
};

function required(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`${name} is required.`);
  return value;
}

function positiveInteger(name: string, fallback: number): number {
  const raw = process.env[name]?.trim();
  if (!raw) return fallback;
  const value = Number(raw);
  if (!Number.isInteger(value) || value <= 0) {
    throw new Error(`${name} must be a positive integer.`);
  }
  return value;
}

export function loadApiEnvironment(): ApiEnvironment {
  const name = required('API_ENVIRONMENT').toLowerCase();
  const baseURL = required('API_BASE_URL');

  if (!ALLOWED_ENVIRONMENTS.has(name)) {
    throw new Error(`API_ENVIRONMENT must be one of: ${[...ALLOWED_ENVIRONMENTS].join(', ')}.`);
  }

  const url = new URL(baseURL);
  if (PRODUCTION_HINT.test(`${name}/${url.hostname}/${url.pathname}`)) {
    throw new Error('Production API automation is prohibited. Use an approved non-production environment.');
  }
  if (name !== 'local' && url.protocol !== 'https:') {
    throw new Error('Non-local API_BASE_URL must use HTTPS.');
  }

  return {
    name,
    baseURL: url.toString().replace(/\/$/, ''),
    defaultTimeoutMs: positiveInteger('API_DEFAULT_TIMEOUT_MS', 30_000),
    pollIntervalMs: positiveInteger('API_POLL_INTERVAL_MS', 500),
  };
}

export function buildAuthHeaders(): Record<string, string> {
  const token = required('API_TOKEN');
  const header = process.env.API_AUTH_HEADER?.trim() || 'Authorization';
  const scheme = process.env.API_AUTH_SCHEME?.trim() ?? 'Bearer';
  return { [header]: scheme ? `${scheme} ${token}` : token };
}
