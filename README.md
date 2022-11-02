# flask-test-app

# Files
Linux systemd file that runs Gunicorn3 as a service: flask-app.service

sudo systemctl enable flask-app

sudo systemctl start flask-app

sudo systemctl daemon-reload

GCP VM configuration - VM_configuration.txt

# Test environment:
conda activate flask-test-app

In VS Code, open the Command Palette (View > Command Palette or (Ctrl+Shift+P)). Then select the Python: Select Interpreter command:

pip install -r requirements.txt

python main.py

Database: https://console.cloud.google.com/sql/instances/mysql-5-7-instance/connections/networking?authuser=7&cloudshell=true&project=sonic-column-358417


In progress:

### Proces wgrywania obrazu na cluster GCP 

1. budowanie obrazka
docker build -t 110kc3/flaskapp . 

docker images #see build images

docker run -p 8080:8080 -d 110kc3/flasktest

docker ps #see running images

docker push 110kc3/flaskapp
(https://hub.docker.com/)

docker kill $(docker ps -q)

2. Autentykacja container registry
https://cloud.google.com/container-registry/docs/advanced-authentication#windows

net localgroup docker-users desktop-49qn32k\kamil /add

From <https://cloud.google.com/container-registry/docs/advanced-authentication#windows> 

-----------------------------  installing gcloud CLI
https://cloud.google.com/sdk/docs/install-sdk

3. Push obrazu do container-registry w GCP
https://cloud.google.com/container-registry/docs/pushing-and-pulling

docker tag 110kc3/flaskapp:latest gcr.io/oceanic-glazing-347308/flaskapp
docker push gcr.io/oceanic-glazing-347308/flaskapp



4. deployment
https://cloud.google.com/kubernetes-engine/docs/deploy-app-cluster

gcloud config set project sonic-column-358417

gcloud config set compute/zone europe-central2-a 

gcloud config set compute/region europe-central2

gcloud container clusters get-credentials cluster-2

kubectl create secret generic flask-token-secret --from-literal XXXXX

kubectl apply -f service-account.yaml
kubectl apply -f .\proxy_with_workload_identity.yaml 

// kubectl create deployment flaskapp-deployment-gcp --image=gcr.io/oceanic-glazing-347308/flaskapp
	
	
kubectl expose deployment flaskapp-deployment-gcp  --type LoadBalancer --port 80 --target-port 8080




//quick deployment of new image

docker build -t 110kc3/flaskapp . 
docker tag 110kc3/flaskapp:latest gcr.io/oceanic-glazing-347308/flaskapp
docker push gcr.io/oceanic-glazing-347308/flaskapp
kubectl apply -f .\proxy_with_workload_identity.yaml 

///other checks:

kubectl get svc
kubectl port-forward flaskapp-deployment-iamxxx      8080:8080

Konfiguracja Cloud SQL proxy as a sidecar
https://github.com/GoogleCloudPlatform/cloudsql-proxy/tree/main/examples/k8s-sidecar
https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/

Options explaining configuration:
Connecting to Cloud SQL from Kubernetes - https://www.youtube.com/watch?v=CNnzbNQgyzo

Remember to add k8s cluster IP to database allowed list