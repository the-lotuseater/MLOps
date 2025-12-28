Overview
========

This project involves creating an ETL pipeline using Apache AirFlow using NASAs API, transforms the data, and loads it into PostGres DB. The entire workdlow is orchestrated by AirFlow, a platform that allows scheduling and monitoring and managing workflows.

I am leveraging Docker to run AirFlow and PostGres as services, ensuring an isolated and reproducible environment. We also utilize Airflow hooks and operators to handle the ETL process efficiently.


Run infra/docker-compose.yml before bringing up the project
docker compose up -d

This is enough to get it running locally.

For deploying to astronomer and running it from there.
0. Create an astronomer account
1. Login to astronomer through the CLI using astro login
2. Create a deployment using the astornomer cli using 
    astro deployment create "nasa-etl-stable" --runtime-version 13.3.0
    Note I am using the CLI because the astronomer website won't you use this runtime (astro 2.x)
3. Copy the deployment ID from astro
4. Run astro deploy [deployment-id] -f
5. Create an RDS instance in AWS.
6. Add a inbound security policy to the security group to allow traffic to the designated port through TCP, you can use the preset postgres connection type and allow traffic from anywhere 0.0.0.0/0
7. On the astronomer UI click on deployment >  Open Airflow  to open the Airlfow UI for this deployment.
8. Create a connection for postgres with the hostname of postgres from AWS RDS. Enter details
9. Create a connection for nasa api using the api key.
10. Run the DAG.
Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes one example DAG:
    - `example_astronauts`: This DAG shows a simple ETL pipeline example that queries the list of astronauts currently in space from the Open Notify API and prints a statement for each astronaut. The DAG uses the TaskFlow API to define tasks in Python, and dynamic task mapping to dynamically print a statement for each astronaut. For more on how this DAG works, see our [Getting started tutorial](https://www.astronomer.io/docs/learn/get-started-with-airflow).
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

Start Airflow on your local machine by running 'astro dev start'.

This command will spin up five Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- DAG Processor: The Airflow component responsible for parsing DAGs
- API Server: The Airflow component responsible for serving the Airflow UI and API
- Triggerer: The Airflow component responsible for triggering deferred tasks

When all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You should also be able to access your Postgres Database at 'localhost:5432/postgres' with username 'postgres' and password 'postgres'.

Note: If you already have either of the above ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://www.astronomer.io/docs/astro/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.
