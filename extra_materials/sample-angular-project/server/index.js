const express = require('express');
const { productsRouter } = require('./products.controller');

const app = express();
app.use(express.json());
app.use('/api/products', productsRouter);

app.get('/health', (_req, res) => res.json({ ok: true }));

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  app.listen(PORT, () => console.log(`API listening on http://localhost:${PORT}`));
}

module.exports = { app };
