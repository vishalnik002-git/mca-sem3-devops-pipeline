# DevOps Control Center — setup (Windows PowerShell)

## Local setup (no cloud credentials needed)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. Click **Run tests** to execute the included Python unit tests. The test result, timings and logs are saved in `data/pipeline.db` (SQLite).

If PowerShell blocks activation, open Command Prompt and run `venv\Scripts\activate.bat`.

## Optional Docker image build button

Only on a trusted local machine with Docker Desktop running:

```powershell
$env:ENABLE_DOCKER_BUILDS="1"
python app.py
```

Now **Build image** performs `docker build -t mca-devops-app:local .` and saves output. Do not enable this option on a public instance. There is no login/authentication layer on this local dashboard.

## Dockerize the dashboard

```powershell
docker build -t mca-devops-dashboard .
docker run --rm -p 5000:5000 mca-devops-dashboard
```

The Docker build button is disabled in a container by default. SQLite data inside a disposable container will not persist unless mounted to a writable volume.

## What is / is not live

- Live: Flask health, local Python tests, optional local Docker build, SQLite job log, run metrics.
- Not connected: GitHub Actions runs, Azure registry, Azure App Service, Terraform apply. These require credentials and integration and are **not** represented as deployed.
- GitHub Actions workflow now runs Python tests before building and pushing image to the existing ACR. To use its push step, configure `ACR_USERNAME` / `ACR_PASSWORD` repository secrets and ensure the registry matches your subscription.
- Production deployment requires additional security and infrastructure verification. Never expose the job runner publicly without authentication and authorization.
