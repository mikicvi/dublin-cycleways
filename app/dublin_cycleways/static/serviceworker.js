const CACHE_NAME = 'cycleways-v16';
const CACHE_LIFETIME = 8 * 60 * 60 * 1000; // Cache lifetime in milliseconds (24 hours)
const CACHE_LIFETIME_LIVE = 5 * 60 * 1000; // Cache lifetime for live data in milliseconds (5 minutes)
const urlsToCache = [
    '/map/',
    '/offline/',
    '/api/cycleways/',
    '/api/parking-stands/',
    '/api/maintenance-stands/',
    '/api/red-cycling-infrastructure/',
    '/api/yellow-cycling-infrastructure/',
    '/staticfiles/img/apple-touch-icon.png',
    '/staticfiles/img/favicon.ico',
    '/staticfiles/img/marker-icon-2x-green.png',
    '/staticfiles/img/marker-icon-2x-orange.png',
    '/staticfiles/img/marker-shadow.png',
    '/staticfiles/css/map_styles.css',
    '/staticfiles/js/map.js',
    '/staticfiles/js/theme-toggle.js',
    '/staticfiles/serviceworker.js',
    '/staticfiles/js/login.js',
    '/staticfiles/js/register.js',
    'https://unpkg.com/leaflet/dist/leaflet.js',
    'https://unpkg.com/leaflet/dist/leaflet.css',
    'https://unpkg.com/leaflet/dist/images/marker-icon.png',
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    'https://unpkg.com/leaflet/dist/images/marker-shadow.png',
    'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    'https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js',
    'https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css',
    'https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css',
];

// Install Service Worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            const cachePromises = urlsToCache.map((url) => {
                return fetch(url).then((response) => {
                    const responseClone = response.clone();
                    const headers = new Headers(responseClone.headers);
                    headers.append('sw-cache-timestamp', Date.now().toString());
                    const newResponse = new Response(responseClone.body, {
                        status: responseClone.status,
                        statusText: responseClone.statusText,
                        headers: headers,
                    });
                    return cache.put(url, newResponse);
                });
            });
            return Promise.all(cachePromises).catch((error) => {
                console.error('Failed to cache during install:', error);
            });
        })
    );
});

// Fetch Cached Content
self.addEventListener('fetch', (event) => {
    if (event.request.method === 'GET') {
        event.respondWith(
            caches.match(event.request).then((response) => {
                if (response) {
                    const cachedTimestamp = response.headers.get('sw-cache-timestamp');
                    const now = Date.now();
                    const isLiveData = ['/api/dublin-bikes/', '/api/bleeper-bikes/', '/api/moby-bikes/'].some((path) => event.request.url.includes(path));
                    const cacheLifetime = isLiveData ? CACHE_LIFETIME_LIVE : CACHE_LIFETIME;

                    if (cachedTimestamp && (now - parseInt(cachedTimestamp, 10)) > cacheLifetime) {
                        // Cache expired, fetch new data
                        return fetchAndCache(event.request);
                    }
                    return response;
                }
                return fetchAndCache(event.request);
            })
        );
    }
});

// Fetch and cache the request
function fetchAndCache(request) {
    return fetch(request).then((response) => {
        if (!response.ok) {
            return response;
        }
        const responseClone = response.clone();
        const headers = new Headers(responseClone.headers);
        headers.append('sw-cache-timestamp', Date.now().toString());
        const newResponse = new Response(responseClone.body, {
            status: responseClone.status,
            statusText: responseClone.statusText,
            headers: headers,
        });
        caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, newResponse);
        });
        return response;
    }).catch((error) => {
        console.error('Fetch failed; returning offline page instead.', error);
        return caches.match('/offline/');
    });
}

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