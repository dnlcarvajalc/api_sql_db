# Globant’s Data Engineering Coding Challenge
For the solution of this coding challenge I implemented this system. It combines a FastAPI application with AWS infrastructure provisioned via Terraform, featuring automated deployment through GitHub Actions workflows.

## API IMPLEMENTATION:
The application provides HTTP endpoints for CSV data upload and metrics reporting, using SQLite for database operations.

### Upload Function Implementation
The upload_table_csv function at app/routes/upload.py implements the core upload logic:

* **Schema Extraction**: Gets column names from the SQLAlchemy model's table definition
* **CSV Reading**: Uses pandas to read CSV files without headers, mapping to model columns
* **Batch Processing**: Processes data in configurable chunks to optimize database performance
* **Object Creation**: Converts DataFrame rows to SQLAlchemy model instances
* **Bulk Insertion**: Uses bulk_save_objects for efficient database insertion
* **Error Handling**: Raises appropriate HTTP exceptions for CSV and database errors

# Metrics Routes Module

The **metrics routes module** provides `GET` endpoints for analytical reporting.
These endpoints execute custom SQL queries from external files to generate business intelligence reports.

## Metrics Endpoints

| Endpoint                          | Query File                              | Purpose                                               | Parameters                |
|-----------------------------------|-----------------------------------------|-------------------------------------------------------|---------------------------|
| `/metrics/hired-employees`        | `app/sql/employees_hired_job.sql`       | Employees hired per job and department by quarter     | `year` (default: `2021`) |
| `/metrics/departments-above-mean` | `app/sql/departments_above_mean.sql`    | Departments hiring above mean in a year               | `year` (default: `2021`) |

# Integration with CI/CD
The Makefile complements the CI/CD pipeline by providing local development automation that mirrors the quality checks and testing performed in the automated workflows.

Use command ```make``` in the terminal to create environtment, install dependencies and run linter, clean code and run test.  
use command ```make server``` to run all before and uvicorn server.

# Key Configuration Variables
The `Makefile` defines tool paths using a virtual environment approach:

- **`VENV_DIR=venv`** – Virtual environment directory  
- **`PYTHON`, `PIP`, `UVICORN`, `LINTER`** – Tool paths within the virtual environment  

---

# MakeFile Targets

## Development Workflow Targets
- **`all`**: Executes the complete development workflow (`env`, `activate`, `lint`, `format`, `clean`, `test`)
- **`server`**: Runs the full workflow and starts the development server

---

## Environment Management
- **`env`**: Creates virtual environment, upgrades pip, and installs dependencies from `requirements.txt`
- **`activate`**: Displays the command to activate the virtual environment


---

## Code Quality
- **`lint`**: Runs `flake8` linter on the `app/` directory with `--exit-zero` flag
- **`format`**: Applies `black` code formatting to the `app/` directory
- **`clean`**: Removes Python cache files and pytest artifacts

---

## Testing and Execution
- **`test`**: Executes `pytest` with coverage reporting for the `app/` module
- **`run`**: Kills any process on port 8000 and starts the FastAPI server with reload


WARNING: Using make server will kill anything in port 8000

# Container Configuration
The `Dockerfile` creates a lightweight container optimized for the FastAPI application runtime.  
It exposes the application on **port 8000** using **Uvicorn** as the server, following a standard build process that copies `requirements.txt` first to leverage Docker layer caching for dependency installation.  

---

# Integration with Deployment Pipeline
The `Dockerfile` is central to the automated deployment workflow defined in **`.github/workflows/push_image.yml`**.  

- The GitHub Actions workflow builds the Docker image:  
  ```bash
  docker build -t $ECR_REPOSITORY:$IMAGE_TAG .
Then pushes it to AWS ECR for automatic deployment to App Runner.

Local Development Support
The Dockerfile also supports local development:

```
docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app
```
# Infrastructure
The infrastructure is provisioned and managed using Terraform configuration files, providing a containerized FastAPI application hosted on AWS App Runner with ECR for container registry services.

## Infrastructure Overview

The system infrastructure consists of three main AWS services working together to provide a scalable, containerized application hosting environment:

| Service       | Purpose                          | Resource Name                        |
|---------------|----------------------------------|--------------------------------------|
| **Amazon ECR** | Container image registry         | `globant-api`                        |
| **AWS App Runner** | Container hosting service       | `globant-api`                        |
| **AWS IAM**    | Access control and permissions   | `globant-project-apprunner-ecr-access` |

# CI/CD
The container deployment process transforms the application source code into a deployable Docker image and pushes it to AWS ECR, which triggers automatic updates to the App Runner service.

The workflow uses Ubuntu latest runners and requires AWS credentials configured as GitHub secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_ACCOUNT_ID).

# Workflows Overview

## ECR Repository Creation Workflow
The **`create_ecr_repo.yml`** workflow provisions the Amazon ECR repository for storing Docker images.  
It runs manually via `workflow_dispatch` and uses Terraform targeting to create only the ECR resource.  

### Docker Image Build and Push
The **`push_image.yml`** workflow handles application containerization and deployment.  
It triggers automatically on pushes to the deployment branch and builds/pushes Docker images to ECR.  

## App Runner Deployment Workflow
The **`terraform_app_runner.yml`** workflow deploys the AWS App Runner service and associated IAM resources.  
It targets multiple resources including the App Runner service, IAM role, and policy attachments.  

## Infrastructure Destruction Workflow
The **`terraform-destroy.yml`** workflow provides complete teardown of all AWS resources.  
It runs `terraform destroy` without targeting specific resources to remove everything.  

# Raw SQL for Analytics

The most significant SQL usage occurs in the metrics endpoints, which execute external SQL files for complex analytical queries.  

## Metrics Endpoints SQL Execution

Both analytics endpoints follow the same pattern:

1. **Load SQL query** from external file using `Path.read_text()`  

2. **Execute parameterized query** using SQLAlchemy’s `text()` function  

3. **Transform results to JSON format**  


## External SQL Files

The application uses two external SQL files:

- `app/sql/employees_hired_job.sql` → Quarterly hiring metrics  

- `app/sql/departments_above_mean.sql` → Departments hiring above average  

