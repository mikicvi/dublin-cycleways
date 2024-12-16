const CACHE_NAME = 'cycleways-v3';
const urlsToCache = [
    // do not cache root URL, since it's a plain redirect to either map or login
    '/map/',
    '/offline/',
    '/api/cycleways/',
    '/api/parking-stands/',
    '/api/maintenance-stands/',
    '/staticfiles/img/apple-touch-icon.png',
    '/staticfiles/img/favicon.ico',
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css',
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js',
];

// Install Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(urlsToCache).catch((error) => {
                console.error('Failed to cache during install:', error);
            });
        })
    );
});

// Fetch Cached Content
self.addEventListener('fetch', (event) => {
    if (event.request.method === 'GET') {
        // Handle navigation requests
        if (event.request.mode === 'navigate') {
            event.respondWith(
                caches.match(event.request).then((response) => {
                    return (
                        response ||
                        fetch(event.request)
                            .then((fetchResponse) => {
                                if (!fetchResponse.ok || fetchResponse.redirected) {
                                    // Clone the response and return it, but do not cache
                                    return fetchResponse;
                                }
                                if (fetchResponse.type === 'opaqueredirect') {
                                    return caches.match('/offline/');
                                }
                                return caches.open(CACHE_NAME).then((cache) => {
                                    cache.put(event.request, fetchResponse.clone());
                                    return fetchResponse;
                                });
                            })
                            .catch(() => caches.match('/offline/').then((offlineResponse) => offlineResponse || new Response('Offline page not available', { status: 503 }))) // Fallback to offline page
                    );
                })
            );
            return;
        }

        // Handle API requests
        if (event.request.url.includes('/api/')) {
            event.respondWith(
                caches.match(event.request).then((response) => {
                    return (
                        response ||
                        fetch(event.request)
                            .then((fetchResponse) => {
                                if (fetchResponse.type === 'opaqueredirect') {
                                    return caches.match('/offline/');
                                }
                                return caches.open(CACHE_NAME).then((cache) => {
                                    cache.put(event.request, fetchResponse.clone());
                                    return fetchResponse;
                                });
                            })
                            .catch(() => {
                                console.warn('Serving cached API response due to fetch failure:', event.request.url);
                                return caches.match(event.request).then((cachedResponse) => cachedResponse || new Response('API response not available', { status: 503 })); // Serve cached response if available
                            })
                    );
                })
            );
            return;
        }

        // Handle static assets
        event.respondWith(
            caches.match(event.request).then((response) => {
                return (
                    response ||
                    fetch(event.request)
                        .then((fetchResponse) => {
                            if (fetchResponse.type === 'opaqueredirect') {
                                return caches.match('/offline/');
                            }
                            return caches.open(CACHE_NAME).then((cache) => {
                                cache.put(event.request, fetchResponse.clone());
                                return fetchResponse;
                            });
                        })
                        .catch(() => {
                            // Fallback to offline page for HTML requests
                            if (event.request.headers.get('accept').includes('text/html')) {
                                return caches.match('/offline/').then((offlineResponse) => offlineResponse || new Response('Offline page not available', { status: 503 }));
                            }
                        })
                );
            })
        );
    }

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
