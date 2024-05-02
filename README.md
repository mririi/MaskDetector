
## Live demo
This application is live on [here](http://35.189.243.91/)

## Tools
VS Code, Google Collab, Google Kubernetes Engine, Google Cloud Shell, Google Container Registery

## Framework
Flask

## Deep Learning
### Description 
The model was trained on Convolutional Neural Network (CNN) and using the Keras library for image classification tasks.

### Test it yourself
Clone the repository
```
git clone https://github.com/mririi/MaskDetector.git
```
Open virtual enviroment
```
python -m venv venv
```
Activate virtual enviroment
```
venv\Scripts\activate
```
Install requirements
```
pip install -r requirements.txt
```
Launch application
```
py app.py
```
## Deployment on GKE
### Description
We deploy the application on Google Kubernetes Engine

### Do it yourself
#### Open Google Cloud Shell and enter the following commands:
Clone the repository
```
git clone https://github.com/mririi/MaskDetector.git
```
Create variable PROJECT_ID (your project id, you can find it in the Dashboard)
```
export PROJECT_ID=your-project-id
```
Enter the github project directory
```
cd mask-detector-main
```
Build a docker image based on the Dockerfile inside the project
```
docker build -t gcr.io/${PROJECT_ID}/mask-detector-app:v1 .
```
Authenticate  Container Registry (you need to run this only once)
```
gcloud auth configure-docker
```
Push the docker image
```
docker push gcr.io/${PROJECT_ID}/mask-detector-app:v1
```
Set your project ID and Compute Engine zone options for the gcloud tool
```
gcloud config set project $PROJECT_ID 
gcloud config set compute/zone zone europe-west1-b
```
Create a cluster
```
gcloud container clusters create mask-detector-cluster --num-nodes=2
```
Create Deployment
```
kubectl create deployment mask-detector-app --image=gcr.io/${PROJECT_ID}/mask-detector-app:v1
```
Expose the app
```
kubectl expose deployment mask-detector-app --type=LoadBalancer --port 80 --target-port 8081
```
## CI/CT/CD Pipline
### Description
Create a continous integration, training and deployment pipline and make it run on every push

### Do it yourself
Create .github/workflows directory
```
mkdir .github/workflows
cd .github/workflows
```
Create a file name it what you want and make sure its .yaml and put the code inside the file ci-cd.yaml in it
```
name: Continuous Integration/Training/Deployment Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Clone the repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Run tests
        run: pytest

      - name: Train model
        run: python train.py

      - name: Set up Google Cloud SDK
        uses: google-github-actions/setup-gcloud@v0.2.0
        with:
          project_id: new-new-419022
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          export_default_credentials: true

      - name: Install gke-gcloud-auth-plugin
        run: gcloud components install gke-gcloud-auth-plugin

      - name: Authenticate Docker with GCR
        run: gcloud auth configure-docker gcr.io

      - name: Get current version from deployment.yaml
        id: get_version
        run: echo ::set-output name=version::$(grep 'image:' kubernetes/deployment.yaml | awk -F':' '{print $3}')

      - name: Increment version
        id: increment_version
        run: |
          # Extract version components
          MAJOR=$(echo "${{ steps.get_version.outputs.version }}" | cut -d. -f1)
          MINOR=$(echo "${{ steps.get_version.outputs.version }}" | cut -d. -f2)
          PATCH=$(echo "${{ steps.get_version.outputs.version }}" | cut -d. -f3)

          # Increment PATCH version
          PATCH=$((PATCH+1))

          # Set new version
          NEW_VERSION="$MAJOR.$MINOR.$PATCH"
          echo "::set-output name=new_version::$NEW_VERSION"

      - name: Update deployment.yaml with new version
        run: |
          sed -i "s/image: gcr.io\/new-new-419022\/mask-detector-app:${{ steps.get_version.outputs.version }}/image: gcr.io\/new-new-419022\/mask-detector-app:${{ steps.increment_version.outputs.new_version }}/" kubernetes/deployment.yaml

      - name: Build and push Docker image
        run: |
          docker build -t gcr.io/new-new-419022/mask-detector-app:${{ steps.increment_version.outputs.new_version }} .
          docker push gcr.io/new-new-419022/mask-detector-app:${{ steps.increment_version.outputs.new_version }}

      - name: Deploy to GKE
        run: |
          gcloud container clusters get-credentials mask-detector-cluster --zone europe-west1-b --project new-new-419022
          kubectl apply -f kubernetes/deployment.yaml

      - name: Verify deployment
        run: |
          kubectl get services 
          kubectl get pods
          kubectl rollout status deployment/mask-detector-app
```
Now get back to the main directory and create tests directory
```
cd ../..
mkdir tests
```
Now create the test file (make sure its in this format ``test_thenameofthepythonfileyouwanttotest.py``) and put this code
```
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

```
Now create the a kubernetes directory
```
cd ..
mkdir kubernetes
```
And create a deployment.yaml file that contains the cluster deployment details
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mask-detector-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mask-detector-app
  template:
    metadata:
      labels:
        app: mask-detector-app
    spec:
      containers:
      - name: mask-detector-app
        image: gcr.io/new-new-419022/mask-detector-app:v2
        ports:
        - containerPort: 8081
---
apiVersion: v1
kind: Service
metadata:
  name: mask-detector-app
spec:
  selector:
    app: mask-detector-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8081
  type: LoadBalancer
```

We are done!

