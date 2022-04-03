# Airflow k8 DBT Demo
This is a repo with code examples on how to run DBT jobs on Cloud Composer 2 with Airflow 2

## Structure
- `dags`: this folder contains a sample DAG using k8 pod operator
- `dbt`: this folder has a sample dbt project and Dockerfile to build the dbt container

## Build the dbt container

### Build
First, replace the properties of `project` and `impersonate_service_account` in dbt/profiles.yml with your own one, then execute
```
export PROJECT_ID=<replace with your gcp project id>
docker build . -f ./dbt/Dockerfile -t eu.gcr.io/$PROJECT_ID/airflow-k8-dbt-demo:latest
```

### Tag
```
export VERSION=<replace with version, i.e. 1.0.1>
docker tag eu.gcr.io/$PROJECT_ID/airflow-k8-dbt-demo \
    eu.gcr.io/$PROJECT_ID/airflow-k8-dbt-demo:$VERSION
```

### Push to GCR
```
gcloud auth configure-docker
docker push eu.gcr.io/$PROJECT_ID/airflow-k8-dbt-demo:$VERSION
```

## Deploy DAGs
> Note it's better to use gsutil rsync for production deployment
```
export $BUCKET_ID=<replace with your composer cloud storage bucket id>
gsutil cp -r dags/* gs://$BUCKET_ID/dags
```

## Configure Workload Identity for the Composer 2 Cluster
Cloud Composer 2 runs on the GKE Auto Pilot cluster which means you don't get to configure or manage node or node pools. 

Follow instructions [here](https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to) but the following steps can be ignored.
> reading the full instructions https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity is still recommended 
```
8. Update your Pod spec to schedule the workloads on nodes that use Workload Identity and to use the annotated Kubernetes service account.
9. Apply the updated configuration to your cluster: kubectl apply -f DEPLOYMENT_FILE
```

And this is what I did to the cluster I had for the demo
```
kubectl create namespace k8-executor

kubectl create serviceaccount composer --namespace k8-executor

gcloud iam service-accounts add-iam-policy-binding composer@rocketech-de-pgcp-sandbox.iam.gserviceaccount.com \
    --role roles/iam.workloadIdentityUser \
    --member "serviceAccount:rocketech-de-pgcp-sandbox.svc.id.goog[k8-executor/composer]"

kubectl annotate serviceaccount composer \
    --namespace k8-executor \
    iam.gke.io/gcp-service-account=composer@rocketech-de-pgcp-sandbox.iam.gserviceaccount.com
```