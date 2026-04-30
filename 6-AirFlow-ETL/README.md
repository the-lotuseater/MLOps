# NASA APOD ETL Pipeline (Airflow + Astronomer)

An automated daily ETL pipeline built with Apache Airflow and deployed on Astronomer. Ingests NASA's [Astronomy Picture of the Day (APOD)](https://api.nasa.gov/) API, transforms the response, and loads structured records into a PostgreSQL database.

## Pipeline Overview

The DAG (`nasa_apod_postgres`) runs on a `@daily` schedule and executes 4 tasks in order:

```
create_table >> extract_apod >> transform_apod_data >> load_data_to_postgres
```

| Step | Task | Description |
|------|------|-------------|
| 1 | `create_table` | Creates the `apod_data` table in PostgreSQL if it doesn't exist |
| 2 | `extract_apod` | Fetches daily data from the NASA APOD API via `HttpOperator` |
| 3 | `transform_apod_data` | Extracts relevant fields: title, explanation, URL, date, media type |
| 4 | `load_data_to_postgres` | Inserts the transformed record into PostgreSQL using `PostgresHook` |

## Schema

```sql
CREATE TABLE apod_data (
    id           SERIAL PRIMARY KEY,
    title        TEXT,
    explanation  TEXT,
    url          TEXT,
    date         DATE,
    media_type   VARCHAR(50)
);
```

## Run Locally

Requires [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli) and Docker.

```bash
astro dev start
```

This spins up 5 containers (Scheduler, API Server, DAG Processor, Triggerer, Postgres metadata DB) and opens the Airflow UI at `http://localhost:8080`.

Then in the Airflow UI, create two connections:

- **`nasa_api`** — HTTP connection to `https://api.nasa.gov` with your NASA API key in the extras as `{"api_key": "YOUR_KEY"}`
- **`my_postgres_db`** — Postgres connection pointing to `localhost:5432` (username: `postgres`, password: `postgres`)

## Deploy to Astronomer + AWS RDS

1. Create an [Astronomer](https://www.astronomer.io/) account and login via CLI:
   ```bash
   astro login
   ```

2. Create a deployment (using CLI because the Astronomer website restricts this runtime version):
   ```bash
   astro deployment create "nasa-etl-stable" --runtime-version 13.3.0
   ```

3. Deploy the project (replace with your deployment ID):
   ```bash
   astro deploy <deployment-id> -f
   ```

4. Create an **AWS RDS PostgreSQL** instance. Add an inbound rule to its security group allowing TCP traffic on port `5432` from `0.0.0.0/0`.

5. In the Astronomer UI, open the Airflow UI for your deployment and create the same two connections (`nasa_api`, `my_postgres_db`) using the RDS hostname.

6. Trigger or wait for the scheduled DAG run.

## Tech Stack

- **Apache Airflow** via Astronomer (Astro Runtime)
- **NASA APOD API**
- **PostgreSQL** (local Docker or AWS RDS)
- **Docker**
