const express = require('express');

const SEED = [
  { id: 'p1', name: 'Architect day',     priceEur: 1200, stock: 5, category: 'consulting' },
  { id: 'p2', name: 'Claude bootcamp',   priceEur: 800,  stock: 0, category: 'training'   },
  { id: 'p3', name: 'Enterprise licence',priceEur: 4500, stock: 12,category: 'license'    },
];

function buildRouter(seed = SEED) {
  const router = express.Router();

  router.get('/', (_req, res) => {
    res.json({ items: seed, total: seed.length });
  });

  router.get('/:id', (req, res) => {
    const found = seed.find((p) => p.id === req.params.id);
    if (!found) return res.status(404).json({ error: 'not found' });
    res.json(found);
  });

  return router;
}

module.exports = {
  productsRouter: buildRouter(),
  buildRouter,
  SEED,
};
