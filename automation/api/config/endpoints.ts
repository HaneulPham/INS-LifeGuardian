export function apiPath(path: string): string {
  const normalized = path.trim();
  if (!normalized.startsWith('/')) {
    throw new Error(`API path must start with '/': ${path}`);
  }
  if (normalized.includes('://')) {
    throw new Error('Use relative API paths; base URL belongs in API_BASE_URL.');
  }
  return normalized;
}
