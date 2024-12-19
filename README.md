# Dublin Cycling Web App

This project is a django GIS web application designed to enhance the cycling experience in Dublin by providing information on bike stands, repair stations, bike lock locations, and cycling paths.  
The application integrates various datasets from the Irish government, ranging from 2020 to the present, and offers features such as querying datasets, calculating the longest safe journey by bike, and highlighting areas without cycling paths. It also provides a live API data feed for Dublin Bikes, Bleeper Bikes, and Moby Bikes, refreshed every 5 minutes in accordance to the API provider - https://data.smartdublin.ie.

## Environment Variables

The application requires the following environment variables to be set in a `.env` file:

| Variable                    | Description                         | Example Value                   |
| --------------------------- | ----------------------------------- | ------------------------------- |
| `DJANGO_SUPERUSER_USERNAME` | Superuser username for Django admin | `admin`                         |
| `DJANGO_SUPERUSER_EMAIL`    | Superuser email for Django admin    | `admin@example.com`             |
| `DJANGO_SUPERUSER_PASSWORD` | Superuser password for Django admin | `supersecretpassword`           |
| `DJANGO_SECRET_KEY`         | Secret key for Django application   | `django-insecure-yourtokenhere` |
| `DJANGO_DEBUG`              | Debug mode for Django               | `True`                          |
| `DEPLOY_SECURE`             | Settings flag for secure deployment | `False`                         |
| `POSTGRES_DB`               | PostgreSQL database name            | `gis`                           |
| `POSTGRES_USER`             | PostgreSQL username                 | `docker`                        |
| `POSTGRES_PASSWORD`         | PostgreSQL password                 | `docker`                        |
| `POSTGRES_HOST`             | PostgreSQL host                     | `postgis`                       |
| `POSTGRES_PORT`             | PostgreSQL port                     | `5432`                          |
| `PGADMIN_DEFAULT_EMAIL`     | Default email for pgAdmin           | `admin@example.com`             |
| `PGADMIN_DEFAULT_PASSWORD`  | Default password for pgAdmin        | `samplepassword`                |
| `MAPBOX_API_KEY`            | MapBox API key for routing & search | `pk.somerandomcharacters`       |

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/mikicvi/dublin-cycleways.git
    cd dublin-cycleways/app
    ```
2. Set up your env variables as shown above
3. Start the app in docker:
    ```sh
    docker compose up --build
    ```
## Deployment
- If deploying on low config VPS, building will fail. To combat this following steps can be taken:
  1. `docker build --platform={linux/amd64 or arm64} -t dublin_cycleways-{platform} .` - Platform specification has to be chosen based on the deployment system target architecture. 
  2. `docker tag dublin_cycleways{-platform} {dockerusername}/dublin_cycleways:latest ` - Replace curly braces {} with whatever your platform and username are
  3. `docker tag dublin_cycleways-{platform} {username}/dublin_cycleways:latest` - Replace curly braces {} with whatever your platform and username are
    - Tagname is kept as `latest` so it does not have to be specified for pulling on VPS side. On VPS(or home server) enter: `docker pull {username}/dublin_cycleways`
  - 
---

### Features List
| **Feature**                                    | **Status** | **Details**                                                                 |
|------------------------------------------------|------------|------------------------------------------------------------------------------|
| Comprehensive Cycling Data Integration         | ✅          | Combines datasets including bike stands, repair stations, bike lock locations, and cycling paths sourced from the Irish government (2020–present). |
| Advanced Querying Capabilities                 | ✅          | Enables querying of datasets across multiple categories for in-depth insights. |
| Dynamic Map Layers                             | ✅          | - **Segregated Cycleways**: Highlights physically separated cycling infrastructure. |
|                                                |            | - **Shared Cycleways**: Displays shared cycling lanes integrated with roads.  |
|                                                |            | - **No Cycleways**: Identifies areas lacking cycling paths with distinct visual indicators. |
| Parking Locations                              | ✅          | Provides a dropdown to display parking facilities for cyclists.              |
| Repair Stations                                | ✅          | Lists repair station locations for cyclists in an accessible dropdown.       |
| Real-Time User Location                        | ✅          | Displays the user's current location on the map for easy navigation.         |
| Secure User Registration and Login             | ✅          | Supports account creation and login with OWASP-compliant input sanitization. |
| Enhanced Map Legend                            | ✅          | Intuitive map legend to improve layer and route selection clarity.           |
| Live Dublin Bikes Data                         | ✅          | Displays real-time updates for Dublin Bikes availability and stations.       |
| Smart Dublin API Integration                   | ✅          | Adapts APIs for live data from Dublin Bikes, Bleeper Bikes, and Moby Bikes.  |
| Real-Time Routing                              | ✅          | - **Location Search**: Enables location-based search for destinations.       |
|                                                |            | - **Route Planning**: Provides bike-friendly routing to selected map points. |
| Fully Responsive and Optimized UI              | ✅          | Features a Bootstrap-based design with a clean, modern interface.            |
| PWA Optimization                               | ✅          | Offline caching for seamless functionality even without network access.      |
| Dark and Light Mode Support                    | ✅          | Fully themed for both light and dark modes, including Leaflet elements.      |
| Dublin City Parking Integration                | ✅          | Leverages Overpass API for comprehensive parking data.                       |
| OpenAPI Documentation                          | ✅          | API documentation generated using DRF Spectacular with Swagger and ReDoc support - OpenAPI 3.0 schema. |
| Modular Code Architecture                      | ✅          | Refactored CSS and JS for maintainability, extracted from templates.         |
| Dockerized Deployment                          | ✅          | Supports automated builds and deployments; domain and SSL configuration provided separately in deploy-config-only branch. |
| Cloud Hosting                                  | ✅          | Currently hosted on AWS free tier for global availability.                   |
| Unit-Tested APIs                               | ✅          | Comprehensive test suite for robust and reliable API performance.            |


### Preview
![Screenshot 2024-12-19 at 23 19 30](https://github.com/user-attachments/assets/f7238778-93a6-41ad-bf15-36a3807c5e93)
![Screenshot 2024-12-19 at 23 17 44](https://github.com/user-attachments/assets/61d3fe67-18ce-4e95-991c-c36a0d66221b)


