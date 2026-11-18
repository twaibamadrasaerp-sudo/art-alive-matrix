const CACHE_NAME = 'matrix-guide-v26';
const APP_SHELL = [
  './',
  './index.html',
  './styles.css?v=26',
  './app.js?v=26',
  './manifest.webmanifest',
  './icon.svg',
  './art%20png.png',
  './qalamxlabs_icon.png'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)).catch(err => console.warn('Cache addAll warning:', err))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isDocOrScript = event.request.mode === 'navigate' ||
                        event.request.destination === 'document' ||
                        event.request.destination === 'script' ||
                        event.request.destination === 'style' ||
                        url.pathname.endsWith('.html') ||
                        url.pathname.endsWith('.js') ||
                        url.pathname.endsWith('.css');

  if (isDocOrScript) {
    // Network-First for core logic and markup so updates reflect instantly
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response && response.status === 200) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => caches.match(event.request).then(cached => cached || caches.match('./index.html')))
    );
    return;
  }

  // Cache-First for static images & assets with network fallback
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
      if (response && response.status === 200) {
        const copy = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy));
      }
      return response;
    }))
  );
});
