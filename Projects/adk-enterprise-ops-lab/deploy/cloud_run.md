# Cloud Run

```bash
gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/adk-enterprise-ops-lab
gcloud run deploy adk-enterprise-ops-lab \
  --image gcr.io/$GOOGLE_CLOUD_PROJECT/adk-enterprise-ops-lab \
  --region us-central1 \
  --allow-unauthenticated
```

Use Secret Manager for API keys and configure artifact storage with GCS.

