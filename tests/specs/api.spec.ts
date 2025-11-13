import { test, expect } from '@playwright/test';

test.describe('API Tests', () => {
  test('health check returns healthy', async ({ request }) => {
    const response = await request.get('/health');
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.status).toBe('healthy');
  });

  test('create and retrieve item', async ({ request }) => {
    // Create item
    const createResponse = await request.post('/api/v1/items', {
      data: {
        name: 'Test Item',
        description: 'Created by test'
      }
    });
    expect(createResponse.status()).toBe(201);
    const created = await createResponse.json();
    expect(created.id).toBeDefined();
    expect(created.name).toBe('Test Item');

    // Retrieve item
    const getResponse = await request.get(`/api/v1/items/${created.id}`);
    expect(getResponse.ok()).toBeTruthy();
    const retrieved = await getResponse.json();
    expect(retrieved.id).toBe(created.id);
  });

  test('list items returns array', async ({ request }) => {
    const response = await request.get('/api/v1/items');
    expect(response.ok()).toBeTruthy();
    const items = await response.json();
    expect(Array.isArray(items)).toBeTruthy();
  });

  test('404 for non-existent item', async ({ request }) => {
    const response = await request.get('/api/v1/items/nonexistent');
    expect(response.status()).toBe(404);
  });

  test('slow endpoint completes', async ({ request }) => {
    const response = await request.get('/api/v1/slow');
    expect(response.ok()).toBeTruthy();
    const data = await response.json();
    expect(data.message).toBe('completed');
  });
});
