import { test as base, expect, type APIRequestContext } from '@playwright/test';
import { buildAuthHeaders, loadApiEnvironment, type ApiEnvironment } from '../config/environment.js';
import { CleanupRegistry } from '../helpers/cleanup.js';

export type ApiFixtures = {
  apiEnvironment: ApiEnvironment;
  api: APIRequestContext;
  authenticatedApi: APIRequestContext;
  cleanup: CleanupRegistry;
};

export const test = base.extend<ApiFixtures>({
  apiEnvironment: async ({}, use) => {
    await use(loadApiEnvironment());
  },

  api: async ({ playwright, apiEnvironment }, use) => {
    const context = await playwright.request.newContext({
      baseURL: apiEnvironment.baseURL,
      extraHTTPHeaders: { Accept: 'application/json' },
      timeout: apiEnvironment.defaultTimeoutMs,
    });
    await use(context);
    await context.dispose();
  },

  authenticatedApi: async ({ playwright, apiEnvironment }, use) => {
    const context = await playwright.request.newContext({
      baseURL: apiEnvironment.baseURL,
      extraHTTPHeaders: { Accept: 'application/json', ...buildAuthHeaders() },
      timeout: apiEnvironment.defaultTimeoutMs,
    });
    await use(context);
    await context.dispose();
  },

  cleanup: async ({}, use) => {
    const registry = new CleanupRegistry();
    await use(registry);
    await registry.run();
  },
});

export { expect };
