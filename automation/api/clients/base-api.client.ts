import type { APIRequestContext, APIResponse } from '@playwright/test';
import type { JsonValue } from '../schemas/common.js';
import { apiPath } from '../config/endpoints.js';

export type ApiRequestOptions = {
  data?: JsonValue;
  params?: Record<string, string | number | boolean>;
  headers?: Record<string, string>;
  timeout?: number;
  failOnStatusCode?: boolean;
};

export class BaseApiClient {
  constructor(protected readonly request: APIRequestContext) {}

  get(path: string, options: ApiRequestOptions = {}): Promise<APIResponse> {
    return this.request.get(apiPath(path), options);
  }

  post(path: string, options: ApiRequestOptions = {}): Promise<APIResponse> {
    return this.request.post(apiPath(path), options);
  }

  put(path: string, options: ApiRequestOptions = {}): Promise<APIResponse> {
    return this.request.put(apiPath(path), options);
  }

  patch(path: string, options: ApiRequestOptions = {}): Promise<APIResponse> {
    return this.request.patch(apiPath(path), options);
  }

  delete(path: string, options: ApiRequestOptions = {}): Promise<APIResponse> {
    return this.request.delete(apiPath(path), options);
  }
}
