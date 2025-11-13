import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './specs',
  timeout: 30000,
  use: {
    baseURL: process.env.API_URL || 'http://localhost:8000',
    extraHTTPHeaders: {
      'Accept': 'application/json',
    },
  },
  reporter: [['html'], ['list']],
});
