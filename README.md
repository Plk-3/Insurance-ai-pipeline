# Insurance AI Pipeline

[![Insurance AI Pipeline CI](https://github.com/Plk-3/Insurance-ai-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/Plk-3/Insurance-ai-pipeline/actions/workflows/ci.yml)

**A Python-based insurance data engineering project demonstrating automated data ingestion, schema mapping, validation, SQL persistence, REST API development, containerization, and continuous integration.**

## Project Overview

Insurance organizations often receive policy data from multiple carriers using different file formats, column names, and data conventions. These inconsistencies can complicate data integration, reporting, and downstream analytics.

The Insurance AI Pipeline demonstrates how a standardized ingestion architecture can address these challenges.

The application processes fictional insurance policy datasets from three carriers, converts their data into a common schema, validates records, stores approved policies in a SQLite database, and exposes the resulting information through a FastAPI REST API.

The project also includes an optional OpenAI-powered schema mapping integration. For development and testing, the pipeline defaults to a deterministic mock mapping mode that does not require paid API access.

**This is a portfolio demonstration using fictional data, not a production insurance system.**

## Key Features

- **Multi-carrier ingestion:** Processes CSV files from three fictional insurance carriers.
- **Schema standardization:** Converts carrier-specific fields into a consistent insurance policy schema.
- **AI integration:** Includes an optional OpenAI API integration for suggesting source-to-target column mappings.
- **Data validation:** Checks required fields, premiums, deductibles, policy dates, and duplicate policy identifiers.
- **SQL database integration:** Stores validated policies in SQLite using parameterized SQL queries and upsert operations.
- **SQL reporting:** Generates policy summaries by carrier, premium analyses by coverage type, and highest-premium policy reports.
- **REST API:** Provides HTTP endpoints for retrieving insurance policy data.
- **Docker support:** Packages the application into a containerized environment.
- **Docker Compose:** Simplifies running the application.
- **Automated testing:** Includes 25 tests covering the pipeline, mapping, validation, database, and API functionality.
- **Continuous integration:** Uses GitHub Actions to run tests and verify Docker builds on repository updates.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development and data processing |
| Pandas | CSV ingestion and data transformation |
| SQLite | Relational database storage |
| SQL | Data retrieval, aggregation, and reporting |
| FastAPI | REST API development |
| Uvicorn | ASGI application server |
| OpenAI API | Optional AI-assisted schema mapping |
| Pytest | Automated software testing |
| Docker | Application containerization |
| Docker Compose | Container configuration and execution |
| GitHub Actions | Continuous integration |
| Git and GitHub | Version control and source code management |

## System Architecture

```text
          FICTIONAL INSURANCE CARRIERS
          ┌──────────┬──────────┬──────────┐
          │ Carrier A│ Carrier B│ Carrier C│
          └────┬─────┴────┬─────┴────┬─────┘
               │          │          │
               └──────────┼──────────┘
                          │
                          ▼
                   CSV INGESTION
                          │
                          ▼
                  SCHEMA MAPPING
                 ┌────────────────┐
                 │ Predefined     │
                 │ Mock AI        │
                 │ Optional OpenAI│
                 └────────────────┘
                          │
                          ▼
                  DATA VALIDATION
                     /         \
                    ▼           ▼
               VALID DATA   INVALID DATA
                    │           │
                    ▼           ▼
              SQLite DB     Error CSV
                    │
             ┌──────┴──────┐
             ▼             ▼
         SQL Reports    FastAPI
                           │
                           ▼
                      REST Clients
```

The system uses predefined mappings for Carriers A and B. Carrier C supports mock mapping for free development or an optional live OpenAI API request.

## Standardized Insurance Policy Schema

All three carrier datasets are transformed into the following fields:

| Field | Description |
|---|---|
| `policy_number` | Carrier policy identifier |
| `customer_name` | Name of insured customer |
| `effective_date` | Policy coverage start date |
| `expiration_date` | Policy coverage end date |
| `coverage_type` | Type of insurance coverage |
| `annual_premium` | Annual policy premium |
| `deductible` | Policy deductible |
| `source_carrier` | Original insurance carrier |

## Data Validation

The validation component evaluates incoming policy records for:

- Missing required values
- Invalid or nonpositive premiums
- Negative deductibles
- Invalid effective or expiration dates
- Expiration dates that do not follow effective dates
- Duplicate policy identifiers within the same carrier

Valid and invalid records are separated into different CSV outputs.

Only valid records are inserted into the SQLite database.

## AI-Assisted Schema Mapping

The project supports two mapping modes.

### Mock Mode (Default)

Uses predefined sample mappings to simulate the AI mapping interface.

```bash
python main.py
```

Mock mode is deterministic, requires no API key, and makes no paid API requests.

### Live OpenAI Mode (Optional)

Uses the OpenAI API to request structured source-to-target column mappings.

```bash
MAPPING_MODE=live python main.py
```

Live mode requires an `OPENAI_API_KEY` environment variable and an API account with available billing credits.

The application validates returned mappings before using them for data transformation.

**Implementation status:** The live OpenAI integration is implemented but has not been successfully verified against the API due to an account quota limitation. Automated testing and the working pipeline use mock mode.

## REST API

The application exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome and status message |
| GET | `/health` | Application health response |
| GET | `/policies/count` | Total number of stored policies |
| GET | `/policies` | Retrieve policies with pagination |
| GET | `/policies/{policy_number}` | Retrieve an individual policy |

Interactive API documentation is available at:

`http://localhost:8000/docs`

When running with the provided Docker Compose configuration, use:

`http://localhost:8001/docs`

### Example API Response

Request:

```http
GET /policies/count
```

Response:

```json
{
  "total_policies": 25
}
```

## Running Locally

### Prerequisites

- Python 3.11 or a compatible Python version
- Git
- pip

### Installation

Clone the repository:

```bash
git clone https://github.com/Plk-3/Insurance-ai-pipeline.git
cd Insurance-ai-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Linux or macOS:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Execute the Data Pipeline

```bash
python main.py
```

The pipeline ingests the sample data, standardizes and validates records, and populates the SQLite database.

### Generate SQL Reports

```bash
python run_reports.py
```

### Start the REST API

```bash
python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

Open:

`http://localhost:8000/docs`

## Running with Docker

Build the Docker image:

```bash
docker build -t insurance-ai-pipeline .
```

Populate the database:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  insurance-ai-pipeline python main.py
```

Start the containerized API:

```bash
docker run --rm \
  -p 8001:8000 \
  -v "$(pwd)/data:/app/data" \
  insurance-ai-pipeline
```

The API is accessible at:

`http://localhost:8001/docs`

## Running with Docker Compose

After populating the database, start the application using:

```bash
docker compose up --build -d
```

Check container status:

```bash
docker compose ps
```

Stop the application:

```bash
docker compose down
```

Docker Compose mounts the local `data` directory to preserve SQLite database files across container restarts.

## Automated Testing

The project includes 25 automated tests.

| Test Category | Number of Tests |
|---|---:|
| Pipeline, schema mapping, and validation | 12 |
| SQLite database functionality | 5 |
| FastAPI endpoints | 8 |
| **Total** | **25** |

Run the full test suite:

```bash
python -m pytest -v
```

Tests cover data validation, mapping behavior, integration between pipeline components, SQL database operations, duplicate prevention, record updates, API responses, pagination, and error handling.

## Continuous Integration

GitHub Actions automatically executes the continuous integration workflow when code is pushed to the `main` branch or a pull request targets `main`.

The workflow:

1. Checks out the repository.
2. Configures Python 3.11.
3. Installs project dependencies.
4. Runs automated tests in mock mapping mode.
5. Builds the Docker image.

The CI status badge at the top of this README displays the latest workflow status.

## Future Enhancements

Potential next steps include:

- PostgreSQL database integration
- SQL-backed API filtering and pagination
- Authentication and authorization
- Cloud deployment
- Expanded AI-assisted schema matching
- Model evaluation and mapping confidence checks
- Monitoring, structured logging, and observability
- Additional data quality reporting
- Production-oriented security improvements

## Project Purpose

This project was developed as a hands-on engineering portfolio to demonstrate practical experience with Python development, data engineering, API design, relational databases, containerization, automated testing, and CI/CD.

It also provides a foundation for exploring AI-assisted data integration and machine learning engineering workflows.

## Disclaimer

All insurance carriers, customers, and policy records used in this project are fictional and intended for educational and portfolio demonstration purposes.
