import type { JsonValue } from '../schemas/common.js';

const SENSITIVE_KEY = /(authorization|token|secret|password|api[-_]?key|cookie|email|phone|mobile|address|date[-_]?of[-_]?birth|dob|medical|health)/i;

export function redactJson(value: JsonValue): JsonValue {
  if (Array.isArray(value)) return value.map(redactJson);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([key, child]) => [key, SENSITIVE_KEY.test(key) ? '[REDACTED]' : redactJson(child)]),
    );
  }
  return value;
}

export function safeExcerpt(value: unknown, maxLength = 1_500): string {
  let rendered: string;
  try {
    rendered = JSON.stringify(redactJson(value as JsonValue));
  } catch {
    rendered = String(value);
  }
  return rendered.length > maxLength ? `${rendered.slice(0, maxLength)}…` : rendered;
}
