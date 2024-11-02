# Dublin Cycling Web App

This project is a django GIS web application designed to enhance the cycling experience in Dublin by providing information on bike stands, repair stations, bike lock locations, and cycling paths.  
The application integrates various datasets from the Irish government, ranging from 2020 to the present, and offers features such as querying datasets, calculating the longest safe journey by bike, and highlighting areas without cycling paths.

## Environment Variables

The application requires the following environment variables to be set in a `.env` file:

| Variable                    | Description                         | Example Value                   |
| --------------------------- | ----------------------------------- | ------------------------------- |
| `DJANGO_SUPERUSER_USERNAME` | Superuser username for Django admin | `admin`                         |
| `DJANGO_SUPERUSER_EMAIL`    | Superuser email for Django admin    | `admin@example.com`             |
| `DJANGO_SUPERUSER_PASSWORD` | Superuser password for Django admin | `supersecretpassword`           |
| `DJANGO_SECRET_KEY`         | Secret key for Django application   | `django-insecure-yourtokenhere` |
| `DJANGO_DEBUG`              | Debug mode for Django               | `True`                          |
| `POSTGRES_DB`               | PostgreSQL database name            | `gis`                           |
| `POSTGRES_USER`             | PostgreSQL username                 | `docker`                        |
| `POSTGRES_PASSWORD`         | PostgreSQL password                 | `docker`                        |
| `POSTGRES_HOST`             | PostgreSQL host                     | `postgis`                       |
| `POSTGRES_PORT`             | PostgreSQL port                     | `5432`                          |
| `PGADMIN_DEFAULT_EMAIL`     | Default email for pgAdmin           | `admin@example.com`             |
| `PGADMIN_DEFAULT_PASSWORD`  | Default password for pgAdmin        | `samplepassword`                |

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
