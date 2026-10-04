# Delivery & Cloud Lab

Executable delivery configuration for the collection: Docker images, PostgreSQL, React/nginx frontend, FastAPI Ops Studio, HTTP monitoring with Prometheus/Blackbox, provisioned Grafana dashboard, Kubernetes workloads and AWS Terraform foundations. A Python policy program reviews Terraform JSON plans locally.

## Docker Compose
Install Docker Engine/Desktop and Compose. Set `POSTGRES_PASSWORD`, `DATABASE_URL` (using hostname `db`), `ADMIN_PASSWORD` (12+ characters), `OPS_TOKEN` (32+ random characters), and `GRAFANA_PASSWORD` in your shell or an ignored `.env` in this directory. URL-encode special characters in the database URL.
```sh
docker compose config --quiet
docker compose up --build
```
Open Operations at http://127.0.0.1:8085, Ops Studio at http://127.0.0.1:8090, Prometheus at http://127.0.0.1:9090 and Grafana at http://127.0.0.1:3001 (admin + configured password). Grafana includes the real HTTP probe dashboard. `docker compose down` stops the containers and preserves volumes. Do not add `-v` unless you intend to delete data. The images require internet access to build/pull. This setup has not been executed in the authoring environment.

## AWS foundation
`terraform/` defines a private VPC/subnet and versioned encrypted S3 artifact bucket with public-access blocking. It does **not** deploy the application or provision EKS. Supply your own globally unique `bucket_name`, region and AWS credentials using your normal AWS profile.
```sh
terraform -chdir=terraform init
terraform -chdir=terraform validate
terraform -chdir=terraform plan -out=plan.bin -var='bucket_name=YOUR-UNIQUE-NAME'
terraform -chdir=terraform show -json plan.bin > plan.json
python policy.py plan.json
```
Review any real plan and costs before applying it yourself. No cloud resources have been created. Terraform state and JSON plans may contain sensitive information; they are ignored by this collection. The checker evaluates three focused policies and must not be treated as complete approval.

Offline check: `python policy.py examples/unsafe-plan.json` deliberately exits 1 with an open-SSH finding. `python -m unittest discover -s tests -v` tests the checker.

## Kubernetes local lab
Requires a local cluster with a default dynamic storage class (for example a configured Minikube cluster).
1. Build the API and web images using the Dockerfiles/contexts above, tag them `sachibara-operations-api:local` and `sachibara-operations-web:local`, and load them into the cluster's image store.
2. Create namespace `sachibara-lab` and a Secret named `operations-secrets` there containing `POSTGRES_PASSWORD`, `DATABASE_URL` (hostname `postgres`), `ADMIN_PASSWORD` and `ADMIN_EMAIL`. Use a locally prepared secret file excluded from Git; no credentials are embedded here.
3. Run `kubectl apply --dry-run=client -f kubernetes/app.yaml`, inspect, then apply in your local cluster.
4. Wait for PostgreSQL and application readiness, then `kubectl -n sachibara-lab port-forward service/web 8085:8080`.
The manifests are a one-replica demo with persistent PostgreSQL. Cluster access, TLS ingress, backups, image supply-chain controls and database migrations need deployment-specific work. No cluster was connected or modified here.
