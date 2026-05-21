const express = require('express');
const request = require('supertest');
const { buildRouter } = require('./products.controller');

function makeApp(seed) {
  const app = express();
  app.use('/api/products', buildRouter(seed));
  return app;
}

const SEED = [
  { id: 'a', name: 'Alpha', priceEur: 100, stock: 1, category: 'consulting' },
  { id: 'b', name: 'Beta',  priceEur: 200, stock: 0, category: 'training'   },
];

describe('GET /api/products', () => {
  it('returns all seeded products with a total', async () => {
    const res = await request(makeApp(SEED)).get('/api/products');
    expect(res.status).toBe(200);
    expect(res.body.total).toBe(2);
    expect(res.body.items).toHaveLength(2);
  });
});

describe('GET /api/products/:id', () => {
  it('returns the single product when it exists', async () => {
    const res = await request(makeApp(SEED)).get('/api/products/a');
    expect(res.status).toBe(200);
    expect(res.body.name).toBe('Alpha');
  });

  it('responds 404 when the product is missing', async () => {
    const res = await request(makeApp(SEED)).get('/api/products/zzz');
    expect(res.status).toBe(404);
    expect(res.body.error).toBe('not found');
  });
});
