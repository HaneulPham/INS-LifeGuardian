import { test, expect } from '../fixtures/api-test.js';
import { BaseApiClient } from '../clients/base-api.client.js';
import { expectStatus, readJsonObject } from '../helpers/assertions.js';
import { apiCaseDetails, apiTestTitle } from '../helpers/traceability.js';

const caseId = 'SMAR-0000-G1-01';

// Template only: replace every placeholder with approved contract evidence.
test(
  apiTestTitle(caseId, 'Verify <specific observable API behavior>'),
  apiCaseDetails({
    caseId,
    requirements: ['R1'],
    endpoint: '/<approved-path>',
    method: 'POST',
    tags: ['@module', '@high'],
  }),
  async ({ authenticatedApi, cleanup }) => {
    const client = new BaseApiClient(authenticatedApi);
    const response = await client.post('/<approved-path>', {
      data: { /* approved request body */ },
    });

    await expectStatus(response, 201);
    const body = await readJsonObject(response);
    expect(body['id']).toEqual(expect.any(String));

    cleanup.register(`${caseId} created resource`, async () => {
      // Delete only the resource created by this test using an approved endpoint.
    });
  },
);
