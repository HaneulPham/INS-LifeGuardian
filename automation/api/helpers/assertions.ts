import { expect, type APIResponse } from '@playwright/test';
import type { JsonObject } from '../schemas/common.js';
import { safeExcerpt } from './redaction.js';

export async function readJsonObject(response: APIResponse): Promise<JsonObject> {
  const contentType = response.headers()['content-type'] ?? '';
  expect(contentType, 'Response must be JSON.').toContain('application/json');
  const body: unknown = await response.json();
  expect(body, `Expected a JSON object, received: ${safeExcerpt(body)}`).toBeTruthy();
  expect(Array.isArray(body), `Expected an object, received: ${safeExcerpt(body)}`).toBe(false);
  expect(typeof body, `Expected an object, received: ${safeExcerpt(body)}`).toBe('object');
  return body as JsonObject;
}

export async function expectStatus(response: APIResponse, expected: number): Promise<void> {
  let body: unknown = '<unavailable>';
  try {
    body = await response.json();
  } catch {
    try { body = await response.text(); } catch { /* response body unavailable */ }
  }
  expect(response.status(), `Unexpected response body: ${safeExcerpt(body)}`).toBe(expected);
}
