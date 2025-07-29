# Iris ML API with Logging & Telemetry on GKE

This project demonstrates a FastAPI-based Iris classification API deployed on GKE with Google Cloud Logging, Monitoring, and Trace using OpenTelemetry.

---

## 🚀 Features

- FastAPI app for iris species prediction (`/predict`)
- Health checks (`/live_check`, `/ready_check`)
- Structured JSON logging
- OpenTelemetry + Cloud Trace integration
- Horizontal pod autoscaling (HPA)
- Deployed to GKE via Kubernetes manifests

---

## 🛠️ Setup Steps

### 1. Enable required GCP services:

```bash
gcloud services enable   container.googleapis.com   logging.googleapis.com   monitoring.googleapis.com   cloudtrace.googleapis.com
```

### 2. Build and push Docker image:

```bash
docker build -t iris-pipeline .
docker tag iris-pipeline us-central1-docker.pkg.dev/<PROJECT_ID>/my-repo/iris-pipeline:latest
docker push us-central1-docker.pkg.dev/<PROJECT_ID>/my-repo/iris-pipeline:latest
```

### 3. Create GKE cluster:

```bash
gcloud container clusters create demo-log-ml-cluster   --zone=us-central1-a   --num-nodes=3   --workload-pool=$(gcloud config get-value project).svc.id.goog   --logging=SYSTEM,WORKLOAD   --monitoring=SYSTEM
```

### 4. Create service account for telemetry:

```bash
gcloud iam service-accounts create telemetry-access   --display-name "Access for GKE ML service"

PROJECT_ID=$(gcloud config get-value project)

gcloud projects add-iam-policy-binding $PROJECT_ID   --member="serviceAccount:telemetry-access@$PROJECT_ID.iam.gserviceaccount.com"   --role="roles/logging.logWriter"

gcloud projects add-iam-policy-binding $PROJECT_ID   --member="serviceAccount:telemetry-access@$PROJECT_ID.iam.gserviceaccount.com"   --role="roles/cloudtrace.agent"
```

### 5. Link GKE SA with IAM SA:

```bash
kubectl create serviceaccount telemetry-access

kubectl annotate serviceaccount telemetry-access   --namespace default   iam.gke.io/gcp-service-account=telemetry-access@$PROJECT_ID.iam.gserviceaccount.com

gcloud iam service-accounts add-iam-policy-binding telemetry-access@$PROJECT_ID.iam.gserviceaccount.com   --role roles/iam.workloadIdentityUser   --member "serviceAccount:$PROJECT_ID.svc.id.goog[default/telemetry-access]"
```

---

## 🚀 Deploy

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
```

---

## 🧪 Test the API

```bash
curl -X POST http://<EXTERNAL-IP>/predict   -H "Content-Type: application/json"   -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

> Replace `<EXTERNAL-IP>` with the output from:
```bash
kubectl get service demo-log-ml-service
```

---

## 🛠️ Useful Commands

- Restart deployment:  
  `kubectl rollout restart deployment demo-log-ml-service`

- Check rollout status:  
  `kubectl rollout status deployment demo-log-ml-service`

- Check pod image and status:  
  `kubectl describe pod <pod-name>`

- Check probes:  
  `kubectl describe pod <pod-name>`

---

## 📈 Performance Test

```bash
sudo apt-get install wrk
wrk -t4 -c100 -d30s --latency -s post.lua http://<EXTERNAL-IP>/predict
```

---

## ✅ Health Probes

- Liveness: `/live_check`
- Readiness: `/ready_check`

These ensure the pod is restarted if it crashes or becomes unhealthy.

---

## ✅ Telemetry Validation

To confirm telemetry is working:

```bash
kubectl get serviceaccount telemetry-access
kubectl describe serviceaccount telemetry-access
gcloud iam service-accounts get-iam-policy telemetry-access@$PROJECT_ID.iam.gserviceaccount.com
```

---

## 🧠 Notes

- App runs on port `8000` inside the container.
- Kubernetes service maps it to port `80` via LoadBalancer.
- `FastAPI` + `OpenTelemetry` + `Cloud Trace` used for observability.
