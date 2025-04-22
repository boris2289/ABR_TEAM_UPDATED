
export default {
  bootstrap: () => import('./main.server.mjs').then(m => m.default),
  inlineCriticalCss: true,
  baseHref: '/static/angular/',
  locale: undefined,
  routes: [
  {
    "renderMode": 2,
    "route": "/static/angular"
  }
],
  entryPointToBrowserMapping: undefined,
  assets: {
    'index.csr.html': {size: 511, hash: '904c0d405f3610cadf73d1f0191d79fed96fe2c25dac63387d14ee6555087c58', text: () => import('./assets-chunks/index_csr_html.mjs').then(m => m.default)},
    'index.server.html': {size: 1024, hash: '6b1010ace45adaa2418ed870f8ae27546a615e3474785a739a55532b2851d549', text: () => import('./assets-chunks/index_server_html.mjs').then(m => m.default)},
    'index.html': {size: 3161, hash: 'c12e8561fdee297815026fdc742f5371a9d99839b3075002eae8885c31067ef9', text: () => import('./assets-chunks/index_html.mjs').then(m => m.default)},
    'styles-5INURTSO.css': {size: 0, hash: 'menYUTfbRu8', text: () => import('./assets-chunks/styles-5INURTSO_css.mjs').then(m => m.default)}
  },
};
