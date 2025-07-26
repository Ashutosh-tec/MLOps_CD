# Iris API on GCP (CI/CD with CML + GKE)

This project contains a FastAPI-based Iris Classification API containerized with Docker, deployed to Google Kubernetes Engine (GKE), and continuously deployed using CML (Continuous Machine Learning).

---

## 🐳 Build Docker Image
```
docker build -t iris-api .
```

## ☁️ Authenticate GCP and Tag Image

```
gcloud auth login
gcloud auth configure-docker
docker tag iris-api gcr.io/<PROJECT-ID>/iris-api

```


## 📤 Push to Google Container Registry (GCR)

```
docker push gcr.io/<PROJECT-ID>/iris-api

```


## ☸️ Create GKE Cluster (Kubernetes)
```
gcloud container clusters create iris-cluster --zone us-central1

```

## 🔑 Get GKE Credentials
```
gcloud container clusters get-credentials iris-cluster --zone us-central1

```

## 📦 Deploy App on GKE
```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

```

## 🌐 Access API
```
kubectl get services
```
#Note the EXTERNAL-IP of `iris-service`
#Open in browser: http://<EXTERNAL-IP>/predict?...

## 🧪 Verify API
```
curl http://<EXTERNAL-IP>/predict?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2

```

## 🔁 Install & Use CML for CI/CD 
(NOTE: through npm as pip was not working)
```
sudo apt update
sudo apt install nodejs npm -y
npm install -g @dvcorg/cml

```

## ✍️ Maintainer
Ashutosh Barnwal
Email: kumarbarnwalashutosh@gmail.com
