# mlops-pipeline-demo
End-to-End MLflow Tracking Pipeline with MinIO, PostgreSQL, and Docker Compose

A complete, production-style ML pipeline setup using:
- **MLflow** (experiment tracking, model registry)
- **MinIO** (S3-compatible artifact store)
- **PostgreSQL** (MLflow backend)
- **Docker Compose** (orchestration)
- **Sklearn client** (demo training + artifact logging)

## Project Structure Overview

| Path/Folders         | Description                                                                |
|----------------------|----------------------------------------------------------------------------|
| `client/`            | Python client for running ML pipeline scripts, model training & logging.    |
| `Dockerfile`      | Build instructions for the client container (installs sklearn, mlflow, etc.)|
| `requirements.txt`| Python dependencies for the client (sklearn, mlflow, matplotlib, etc.)      |
| `src/`            | All ML scripts go here (e.g. `train_iris.py`, `utils/`, etc.)              |
| `train_iris.py`| Demo MLflow training + artifact logging script (Iris dataset)               |
|                                                                                                |
| `mlflow/`            | MLflow tracking server setup (as a service)                                |
| `Dockerfile`      | Build instructions for MLflow service (installs mlflow, boto3, etc.)        |
| `requirements.txt`| Python dependencies for MLflow server                                       |
|                                                                                                |
| `docker-compose.yml` | Main orchestrator file — spins up all services: db, minio, mlflow, client  |
|                                                                                                |
| `minio_data/`        | (auto-generated) MinIO persistent volume (S3 backend storage)              |
|                                                                                                |
| `postgres_data/`     | (auto-generated) PostgreSQL persistent data volume                         |

# Folder Detail
Folder and File Descriptions
## client/
Contains everything needed for running ML pipelines, model training, and artifact logging.
This is where users/data scientists put their own training scripts.
- Dockerfile — Instructions to build the client image, installing Python, MLflow, scikit-learn, etc.
- requirements.txt — All Python dependencies required by the client.
- src/ — Source code folder for your ML scripts.
- train_iris.py — Example script that trains a model on the Iris dataset and logs results/artifacts to MLflow.
- utils/ — (Optional) Place for utility functions, modules, etc.
## mlflow/
Contains files for setting up the MLflow tracking server as a container service.
- Dockerfile — Builds the MLflow tracking server image (installs mlflow, boto3, psycopg2, etc).
- requirements.txt — Python packages needed for MLflow service (typically, no need to change this).
## docker-compose.yml
The orchestration file. Launches all services together: PostgreSQL, MinIO, MLflow, and the client.
Just run docker compose up to get a full working environment.
## minio_data/
Automatically generated volume by Docker Compose for MinIO’s persistent data (object storage for artifacts).
Do not edit manually.
## postgres_data/
Automatically generated volume for PostgreSQL’s persistent data.
Do not edit manually.
# Usage
1. Prerequisites
  - Docker & Docker Compose (Recommended: Docker Desktop)
2. Clone the Repository
```bash
git clone https://github.com/Tale98/mlops-pipeline-demo
cd mlops-pipeline-demo
```
3. Start All Services
```bash
docker compose up -d
```
This will launch:
  - PostgreSQL (backend DB)
  - MinIO (artifact storage)
  - MLflow Tracking Server
  - (Optional) Client container (can be used to run scripts)
4. Accessing Services
  - MLflow UI: http://localhost:5050
  - MinIO Console: http://localhost:9001
5. Prepare the Artifact Bucket (One Time Only)
  Before running experiments, log into the MinIO Console and create a bucket
  - http://localhost:9001 login with username/password default is username: minioadmin, password: minioadmin (can be config in .env MINIO_ROOT_USER, MINIO_ROOT_PASSWORD).
  - click create "Create Bucket" and create bucket called 'mlflow' (can be config in .env MLFLOW_ARTIFACT_ROOT).
6. Running Example Training Scripts (inside client container is recommended)
```bash
docker compose exec client bash
# (now inside the container)
cd src
python train_iris.py
```
also can run outside container but you have to pass env variable yourself ref from .env
  - MLFLOW_TRACKING_URI: ${MLFLOW_TRACKING_URI}
  - AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
  - AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
  - MLFLOW_S3_ENDPOINT_URL: ${MLFLOW_S3_ENDPOINT_URL}
  - MLFLOW_ARTIFACT_ROOT: ${MLFLOW_ARTIFACT_ROOT}
  - AWS_REGION: ${AWS_REGION}
7. View Experiment Results
  - Open the MLflow UI (http://localhost:5050)
  - Check your experiment name (e.g. iris-demo)
  - Explore metrics, params, and artifacts (plots, reports, model files, etc)
# Tear Down
Stop and remove all services
```bash
docker compose down
```
## (Delete minio_data/ and postgres_data/ if you want to reset all persisted data.)
# Contributors

- Apisit 
  - [GitHub](https://github.com/Tale98)
  - [LinkedIn](https://www.linkedin.com/in/apisit-chiamkhunthod-2a11221b4/)
  - Email: oh.oh.159852357@gmail.com

Feel free to reach out if you have any questions or want to collaborate!
