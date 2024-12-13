const CACHE_NAME = 'cycleways-v1';
const urlsToCache = [
    '/',
    '/map/',
    '/offline/',
    '/staticfiles/img/apple-touch-icon.png', // Add other static assets
    '/staticfiles/img/favicon.ico',
];

// Install Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache).catch((error) => {
                console.error('Failed to cache:', error);
            });
        })
    );
});

// Fetch Cached Content
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches
            .match(event.request)
            .then((response) => {
                return (
                    response ||
                    fetch(event.request).then((fetchResponse) => {
                        return caches.open(CACHE_NAME).then((cache) => {
                            cache.put(event.request, fetchResponse.clone());
                            return fetchResponse;
                        });
                    })
                );
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    );
});

// Activate Service Worker and Clear Old Caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
