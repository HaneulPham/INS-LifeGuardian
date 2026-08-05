import type { APIRequestContext } from '@playwright/test';
import { BaseApiClient } from '../clients/base-api.client.js';

export class ModuleApiClient extends BaseApiClient {
  constructor(request: APIRequestContext) {
    super(request);
  }

  // Add only evidence-backed module endpoints and typed payloads.
}
