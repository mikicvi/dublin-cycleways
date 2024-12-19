const MAP_CENTER = [53.3498, -6.2603];
const MAP_ZOOM = 14;
const API_BASE = '/api/';

let userLocation = null;
let routeControl = null;

// Initialize map
const map = L.map('map').setView(MAP_CENTER, MAP_ZOOM);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Layer groups for managing map layers
const cyclewaysLayerGroup = L.layerGroup().addTo(map);
const redInfrastructureLayerGroup = L.layerGroup().addTo(map);
const yellowInfrastructureLayerGroup = L.layerGroup().addTo(map);
const categoryLayerGroup = L.markerClusterGroup().addTo(map);

// Styles for infrastructure
const cyclewayStyle = { color: '#3388ff', weight: 4, opacity: 0.8 };
const redInfrastructureStyle = { color: 'red', weight: 3, opacity: 0.8 };
const yellowInfrastructureStyle = { color: '#ffd003', weight: 3, opacity: 0.9 };


/**
 * Generates HTML content for a popup based on the provided feature and marker coordinates.
 *
 * @param {Object} feature - The GeoJSON feature object containing properties and geometry.
 * @param {Object} feature.properties - The properties of the feature.
 * @param {Object} feature.geometry - The geometry of the feature.
 * @param {string} feature.geometry.type - The type of geometry (e.g., 'Point').
 * @param {Array<number>} markerCoords - The coordinates of the marker [longitude, latitude].
 * @returns {string} The HTML content for the popup.
 */
function createPopupContent(feature, markerCoords) {
    const props = feature.properties || {};
    const fields = [
        { key: 'featureID', label: 'Feature ID' },
        { key: 'name', label: 'Name', formatter: (v) => (v !== 'undefined' ? v : 'No Name') },
        { key: 'layer', label: 'Layer' },
        { key: 'colour', label: 'Colour' },
        { key: 'linetype', label: 'Line Type' },
        { key: 'refname', label: 'Reference Name' },
        { key: 'description', label: 'Description' },
        { key: 'twoway', label: 'Two Way', formatter: (v) => (v === '1' ? 'Yes' : 'No') },
        { key: 'bollard_protected', label: 'Bollard Protected', formatter: (v) => (v === '1' ? 'Yes' : 'No') },
        { key: 'shape_length', label: 'Lane Length', formatter: (v) => `${(parseFloat(v) / 1000).toFixed(2)} km` },
        { key: 'location', label: 'Location' },
        { key: 'date_added', label: 'Date Added' },
        { key: 'area', label: 'Area' },
        { key: 'stand_type', label: 'Stand Type' },
        { key: 'bicycle_parking', label: 'Bicycle Parking Type' },
        { key: 'covered', label: 'Is Sheltered?' },
        { key: 'capacity', label: 'Bicycle Capacity' },
    ];

    // Add structured fields
    let popupContent = fields
        .filter(({ key }) => props[key])
        .map(
            ({ key, label, formatter }) =>
                `<strong>${label}:</strong> ${formatter ? formatter(props[key]) : props[key]}<br>`
        )
        .join('');

    // Add any other dynamic fields
    const excludedKeys = fields
        .map((f) => f.key)
        .concat(['featureID_internal', 'x', 'y', 'public_stands', 'private_stands', 'osm_id']);
    Object.entries(props).forEach(([key, value]) => {
        if (!excludedKeys.includes(key) && value && value.toString().trim()) {
            popupContent += `<strong>${key}:</strong> ${value}<br>`;
        }
    });

    // Add a button for routing only if the feature is a point
    if (feature.geometry.type === 'Point') {
        popupContent += `
				<div class="text-center mt-2">
					<button 
						class="btn btn-sm btn-outline-primary bi bi-arrow-up-circle"
						onclick="startRoutingFromPopup([${markerCoords.join(',')}])">
						Route Here
					</button>
				</div>`;
    }

    return popupContent;
}

/**
 * Asynchronously loads GeoJSON data from a specified endpoint and adds it to a given Leaflet layer group.
 *
 * @param {string} endpoint - The API endpoint to fetch the GeoJSON data from.
 * @param {L.LayerGroup} layerGroup - The Leaflet layer group to which the GeoJSON data will be added.
 * @param {Object} [style=null] - Optional styling options for the GeoJSON layer and markers.
 * @returns {Promise<void>} A promise that resolves when the GeoJSON data has been successfully loaded and added to the layer group.
 *
 * @throws {Error} Throws an error if the fetch request fails or if there is an issue processing the GeoJSON data.
 */
async function loadGeoJSON(endpoint, layerGroup, style = null) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}/`);
        if (!response.ok) throw new Error(`Failed to fetch ${endpoint}: ${response.statusText}`);
        const data = await response.json();
        layerGroup.clearLayers();

        L.geoJSON(data, {
            style: style || undefined,
            pointToLayer: (feature, latlng) => {
                // Apply custom marker styling
                const iconStyle = createMarkerIcon(style || 'default');
                return L.marker(latlng, { icon: iconStyle });
            },
            onEachFeature: (feature, layer) => {
                const { coordinates } = feature.geometry;
                const markerCoords = [coordinates[1], coordinates[0]]; // [lat, lng]
                const popupContent = createPopupContent(feature, markerCoords); // Create popup content
                layer.bindPopup(popupContent); // Bind popup with route button
            },
        }).addTo(layerGroup);
    } catch (error) {
        console.error(`Error loading ${endpoint}:`, error);
    }
}

///---Infrastructure Layers---///
/**
 * Asynchronously loads cycleways GeoJSON data and adds it to the specified layer group with the given style.
 * 
 * @async
 * @function loadCycleways
 * @returns {Promise<void>} A promise that resolves when the GeoJSON data has been loaded and added to the map.
 */
async function loadCycleways() {
    await loadGeoJSON('cycleways', cyclewaysLayerGroup, cyclewayStyle);
}

/**
 * Asynchronously loads the red cycling infrastructure GeoJSON data and applies it to the specified layer group with the given style.
 *
 * @async
 * @function loadRedInfrastructure
 * @returns {Promise<void>} A promise that resolves when the GeoJSON data has been loaded and applied.
 */
async function loadRedInfrastructure() {
    await loadGeoJSON('red-cycling-infrastructure', redInfrastructureLayerGroup, redInfrastructureStyle);
}

/**
 * Asynchronously loads the yellow cycling infrastructure GeoJSON data and applies it to the specified layer group with the given style.
 *
 * @async
 * @function loadYellowInfrastructure
 * @returns {Promise<void>} A promise that resolves when the GeoJSON data has been successfully loaded and applied.
 */
async function loadYellowInfrastructure() {
    await loadGeoJSON('yellow-cycling-infrastructure', yellowInfrastructureLayerGroup, yellowInfrastructureStyle);
}

/**
 * Asynchronously loads and displays the selected category of amenities on the map.
 * Clears existing layers and clusters before loading new data.
 * 
 * The function retrieves the selected category from a dropdown menu with the ID 'amenities-dropdown'.
 * Depending on the selected category, it maps to a specific endpoint and loads the corresponding GeoJSON data.
 * The markers are styled based on the category: 'orange' for Live API bike-related categories and 'green' for others.
 * 
 * @async
 * @function loadSelectedCategory
 * @returns {Promise<void>} A promise that resolves when the selected category data is loaded and displayed on the map.
 */
async function loadSelectedCategory() {
    const selectedCategory = document.getElementById('amenities-dropdown').value;
    const endpoints = {
        parking_stands: 'parking-stands',
        maintenance_stands: 'maintenance-stands',
        dublin_bikes: 'dublin-bikes',
        bleeper_bikes: 'bleeper-bikes',
        moby_bikes: 'moby-bikes',
    };

    const endpoint = endpoints[selectedCategory];
    categoryLayerGroup.clearLayers();
    // Clear clusters if no selection
    if (!endpoint) {
        categoryLayerGroup.clearLayers();
        return;
    }

    // Define marker color
    const categoryStyle = ['dublin-bikes', 'bleeper-bikes', 'moby-bikes'].includes(endpoint) ? 'orange' : 'green';

    // Load the selected category with clustering
    await loadGeoJSON(endpoint, categoryLayerGroup, categoryStyle);
}

/**
 * Fetches the user's current location using the Geolocation API and updates the map with the user's location.
 * If the user's location is successfully fetched, it updates the map with a marker at the user's location,
 * sets the map view to the user's location, and optionally sends the location to the server.
 *
 * @returns {Promise<Array<number>>} A promise that resolves to an array containing the latitude and longitude of the user's location.
 * @throws {string} An error message if geolocation is not supported or if there is an error fetching the location.
 */
async function fetchAndUpdateLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            console.error('Geolocation is not supported by this browser.');
            return reject('Geolocation is not supported.');
        }

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude, accuracy } = position.coords;
                userLocation = [latitude, longitude];

                // Update map with the user's location
                if (window.userLocationMarker) {
                    map.removeLayer(window.userLocationMarker);
                }
                window.userLocationMarker = L.marker(userLocation).addTo(map);
                window.userLocationMarker
                    .bindPopup(`You are within ${accuracy.toFixed(2)} meters from this point`)
                    .openPopup();
                map.setView(userLocation, 14);

                // Optionally, send location to the server
                try {
                    const csrfToken = document.querySelector('input#csrf-token').value || '{{ csrf_token }}';
                    const response = await fetch(`${API_BASE}location/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                        },
                        body: JSON.stringify({ latitude, longitude }),
                    });
                    if (!response.ok) {
                        const data = await response.json();
                        throw new Error(data.error || 'Failed to update location');
                    }
                    console.log('Location updated successfully on the server.');
                } catch (error) {
                    console.error('Error updating location on the server:', error);
                }

                resolve(userLocation);
            },
            (error) => {
                console.error('Error fetching location:', error.message);
                reject(error.message);
            }
        );
    });
}

/**
 * Initializes the routing control on the map with the specified start and end coordinates and mode of transportation.
 * 
 * @param {number[]} startCoords - The starting coordinates as an array [latitude, longitude].
 * @param {number[]} endCoords - The ending coordinates as an array [latitude, longitude].
 * @param {string} [mode='cycling'] - The mode of transportation, either 'cycling' or 'walking'. Defaults to 'cycling'.
 */
function initializeRoutingControl(startCoords, endCoords, mode = 'cycling') {
    if (routeControl) map.removeControl(routeControl);

    const profile = mode === 'walking' ? 'mapbox/walking' : 'mapbox/cycling';

    routeControl = L.Routing.control({
        waypoints: [L.latLng(...startCoords), L.latLng(...endCoords)],
        router: L.Routing.mapbox(MAPBOX_API_KEY, { profile }), // Specify mode of transportation
        lineOptions: { styles: [{ color: 'red', opacity: 0.5, weight: 3 }] },
    }).addTo(map);
}

/**
 * Geocodes a location query using the Mapbox Geocoding API.
 *
 * @param {string} query - The location query to geocode.
 * @returns {Promise<[number, number] | null>} A promise that resolves to an array containing the latitude and longitude of the location, or null if the location could not be geocoded.
 * @throws {Error} If the fetch request fails or no results are found.
 */
async function geocodeLocation(query) {
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
        query
    )}.json?access_token=${MAPBOX_API_KEY}`;
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch location.');
        const data = await response.json();
        if (data.features && data.features.length) {
            const [lng, lat] = data.features[0].geometry.coordinates;
            return [lat, lng];
        }
        throw new Error('No results found.');
    } catch (error) {
        console.error(error.message);
        return null;
    }
}

/**
 * Handles the search and routing functionality.
 * 
 * This function retrieves the end location query from the input field,
 * fetches the user's current location if not already available, geocodes
 * the end location query to get coordinates, and initializes the routing
 * control to plan the route from the user's location to the destination.
 * 
 * @async
 * @function handleSearchAndRoute
 * @returns {void}
 * @throws Will alert the user if the destination is not entered or cannot be found.
 * @throws Will alert the user if an error occurs during the routing process.
 */
async function handleSearchAndRoute() {
    const endLocationQuery = document.getElementById('search-location').value;
    if (!endLocationQuery) return alert('Please enter a destination.');

    try {
        if (!userLocation) userLocation = await fetchAndUpdateLocation();
        const endCoords = await geocodeLocation(endLocationQuery);
        if (!endCoords) return alert('Unable to find the destination.');

        initializeRoutingControl(userLocation, endCoords);
    } catch (error) {
        console.error(error);
        alert('An error occurred while planning the route.');
    }
}

/**
 * Initiates routing from the user's location to the specified marker coordinates.
 * If the user's location is not available, an alert is shown to the user.
 *
 * @param {Array<number>} markerCoords - The coordinates of the marker to route to, in the format [latitude, longitude].
 */
function startRoutingFromPopup(markerCoords) {
    if (!userLocation) {
        alert('User location is not available. Please enable location services.');
        return;
    }
    initializeRoutingControl(userLocation, markerCoords);
}

/**
 * Clears the current route from the map by removing the route control.
 * If a route control exists, it will be removed from the map and set to null.
 */
function clearRoute() {
    if (routeControl) {
        map.removeControl(routeControl);
        routeControl = null;
    }
}

/**
 * Creates a Leaflet marker icon with the specified colour.
 *
 * @param {string} colour - The colour of the marker icon. Can be 'green' or 'orange'.
 * @returns {L.Icon} A Leaflet Icon object configured with the specified colour.
 */
function createMarkerIcon(colour) {
    const iconUrl = `${STATIC_URL}img/marker-icon-2x-${colour}.png`;
    return new L.Icon({
        iconUrl: iconUrl,
        shadowUrl: `${STATIC_URL}img/marker-shadow.png`,
        iconSize: [19, 31],
        iconAnchor: [9, 31],
        popupAnchor: [0.75, -25.5],
        shadowSize: [31, 31],
    });
}

/**
 * Registers a service worker and requests persistent storage.
 * 
 * This function checks if the browser supports service workers and attempts to register
 * a service worker with the specified scope. If the registration is successful, it logs
 * the scope of the registered service worker. If the registration fails, it logs the error.
 * 
 * Additionally, the function checks if the browser supports the Storage API and requests
 * persistent storage. If granted, it logs a confirmation message. If not granted, it logs
 * a warning message indicating that the cache may be cleared by the browser.
 * 
 * @async
 * @function registerServiceWorker
 * @returns {Promise<void>} A promise that resolves when the service worker registration and
 *                          storage persistence request are complete.
 */
async function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker
            .register(`${STATIC_URL}serviceworker.js`, { scope: '/' })
            .then((registration) => {
                console.log('Service Worker registered with scope:', registration.scope);
            })
            .catch((error) => {
                console.error('Service Worker registration failed:', error);
            });
    }
    if ('storage' in navigator && 'persist' in navigator.storage) {
        navigator.storage.persist().then((granted) => {
            if (granted) {
                console.log('Persistent storage granted.');
            } else {
                console.warn('Persistent storage not granted. Cache may be cleared by the browser.');
            }
        });
    }
}

// On document load event listener - load cycleways, fetch user location, and register service worker
document.addEventListener('DOMContentLoaded', async () => {
    // Initialize Segregated Cycleways (always loaded)
    await loadCycleways();
    userLocation = await fetchAndUpdateLocation();
    await registerServiceWorker();
    // Layer visibility control
    const cyclewaysCheckbox = document.getElementById('cyclewaysLayer');
    const redCheckbox = document.getElementById('redInfrastructureLayer');
    const yellowCheckbox = document.getElementById('yellowInfrastructureLayer');

    // Flags to track if data is already loaded
    let redInfrastructureLoaded = false;
    let yellowInfrastructureLoaded = false;

    // Event listeners for toggling layers
    cyclewaysCheckbox.addEventListener('change', () => {
        if (cyclewaysCheckbox.checked) {
            map.addLayer(cyclewaysLayerGroup);
        } else {
            map.removeLayer(cyclewaysLayerGroup);
        }
    });

    redCheckbox.addEventListener('change', async () => {
        if (redCheckbox.checked) {
            if (!redInfrastructureLoaded) {
                await loadRedInfrastructure();
                redInfrastructureLoaded = true;
            }
            map.addLayer(redInfrastructureLayerGroup);
        } else {
            map.removeLayer(redInfrastructureLayerGroup);
        }
    });

    yellowCheckbox.addEventListener('change', async () => {
        if (yellowCheckbox.checked) {
            if (!yellowInfrastructureLoaded) {
                await loadYellowInfrastructure();
                yellowInfrastructureLoaded = true;
            }
            map.addLayer(yellowInfrastructureLayerGroup);
        } else {
            map.removeLayer(yellowInfrastructureLayerGroup);
        }
    });
});