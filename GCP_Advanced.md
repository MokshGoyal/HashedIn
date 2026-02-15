# GCP Advanced

---



4. ***Implement Secret rotation mechanism with cloud function
   The trigger should be day 1 of each months
   If the Label is ENV:PROD & hu-devops-26:username the Secret has to base64 encoded
   For any other label values with & hu-devops-26:username just Credential Should be rotated without any base 64
   Skip the Secret rotation if they are having a Label Saying ENV:DEV & & hu-devops-26:username***



1. Store application secrets securely in Secret Manager with appropriate labels.
2. Configure **Cloud Scheduler** to trigger on  **day 1 of every month** .
3. Use Cloud Scheduler to invoke an  **HTTP-triggered Cloud Function** .
4. Cloud Function fetches the list of secrets to be evaluated.
5. For each secret, read and validate its attached labels.
6. Check if label `hu-devops-26:username` is present on the secret.
7. If the username label is missing, skip secret rotation.
8. If label `ENV:DEV` and `hu-devops-26:username` are both present, skip rotation.
9. If label `ENV:PROD` and `hu-devops-26:username` are present, proceed with rotation.
10. Generate a new secret value (rotated credential).
11. Base64-encode the new secret value for `ENV:PROD`.
12. For non-PROD environments, store the rotated secret without Base64 encoding.
13. Create a new secret version with the updated value.
14. Disable or destroy the previous secret version if required by policy.
15. Log rotation, skip, or error status for auditing and traceability.

---

***Q5. Host 2 tier application on GCP in Cloud run and expose with internal Load balancer and get this accessible on VM
Notes:
Take any 2 sample codes and build them in local and push the images to GAR and set the routing policies in the LB one as FE and one as BE and show both the output. Ensure all the resources you are creating are private***



* Prepare two sample applications locally, one for **Frontend (FE)** and one for  **Backend (BE)** .
* Containerize both applications using Docker.
* Push both container images to **Artifact Registry (GAR)** in a private repository.
* Deploy the **Backend application** to Cloud Run as a private service.
* Deploy the **Frontend application** to Cloud Run as a private service.
* Disable public access for both Cloud Run services.
* Create a **Serverless Network Endpoint Group (NEG)** for the Frontend Cloud Run service.
* Create another Serverless NEG for the Backend Cloud Run service.
* Configure an  **Internal HTTP(S) Load Balancer** .
* Create two backend services in the Load Balancer, one mapped to FE NEG and one to BE NEG.
* Configure URL routing rules so FE routes to frontend service and BE routes to backend service.
* Ensure the Load Balancer is internal and attached to a VPC network.
* Create a private VM in the same VPC network.
* Access the application from the VM using the internal Load Balancer IP.
* Verify FE response and BE response separately to confirm routing works.
