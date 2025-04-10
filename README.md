# AirFlow

## Sign Into Docker Hub

```bash
# login
# can also use user name zubair
docker login -u 'username@gmail.com' -p 'PAAAASWORD'

# images will be on zubair/image-name:version

# logout
docker logout
```

## Add Docker Hub Secret

```bash
# add
kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v1/ --docker-username=zubair --docker-password='PAAAASWORD' --docker-email=username@gmail.com

# check
kubectl get secret
```

## Build Images

Make sure you are signed in

In your usual compose project, add the tags for the built image in the `image` key. The username is the Docker Hub account username. Please use unique image names for our image repo. If unsure please check already pushed images and usecases.

```yaml
services:

  airflow:
    container_name: airflow
    restart: always    
    build:
      context: ./airflow
      dockerfile: Dockerfile
    image: zubair/airflow:latest
```

Use a `docker compose up --build -d` to check if you application works, this command will also build your images. You can build the images without the running the application.

```bash
# push the images
docker compose push
```

Check that the images were sent to Docker Hub repo.

## Kubernetes Manifest File

Use Kompose `convert`

```bash
# run convert
# this is the windows environment variable name for kompose, on linux it will be just "kompose"
kompose-windows-amd64.exe convert -f .\docker-compose.yml --out manifest-queue-1s-public.yaml
```

You should have a Manifest file output. If you are testing on our VMs with Kubernetes you can apply the Manifest file.

Add the Docker hub repo secret (will need a way to script this), `imagePullSecrets` key.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    kompose.cmd: C:\kompose\kompose-windows-amd64.exe convert -f .\docker-compose.yml --out manifest-queue-1s-public.yaml
    kompose.version: 1.35.0 (9532ceef3)
  labels:
    io.kompose.service: airflow
  name: airflow
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: airflow
  template:
    metadata:
      annotations:
        kompose.cmd: C:\kompose\kompose-windows-amd64.exe convert -f .\docker-compose.yml --out manifest-queue-1s-public.yaml
        kompose.version: 1.35.0 (9532ceef3)
      labels:
        io.kompose.service: airflow
    spec:
      containers:
        - env:
            - name: DEBIAN_FRONTEND
              value: noninteractive
            - name: TZ
              value: Africa/Johannesburg
          image: zubair/airflow-public:latest
          name: airflow
          ports:
            - containerPort: 8080
              protocol: TCP
      restartPolicy: Always
      imagePullSecrets:
      - name: regcred
```

Apply the manifest file

```bash
kubectl apply -f manifest-queue-1s-public.yaml

# test on port 8080
kubectl port-forward svc/airflow 8080:8080
```
