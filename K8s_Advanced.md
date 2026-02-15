

KUBERENETES DAY 2

---



Question 4: Gateway API (NGINX Gateway Fabric)
Objective: Configure ingress traffic management using the Kubernetes Gateway API so two internal services are reachable from outside the cluster.
Scenario: You are setting up Gateway API–based ingress for a new application using the NGINX Gateway Fabric controller implementation. The application has two components (web and api) that must be accessible externally.


Tasks
Task 4.1 — Deploy Applications and Services (default namespace)
• Create a Deployment named web-app:
o Replicas: 2
o Image: nginx:1.21
• Create a Deployment named api-app:
o Replicas: 2
o Image: httpd:2.4
• Expose both Deployments as ClusterIP Services on port 80
Shortcut option: Apply the provided setup.yaml.


Task 4.2 — Create Gateway
• Create a Gateway named main-gateway in the default namespace
• Configure it to:
o Listen on port 80
o Use protocol HTTP
o Use hostname example.local


Task 4.3 — Create HTTPRoute
• Create an HTTPRoute named app-routes
• Configure routing using PathPrefix matching:
o Requests with path prefix /web → web-app Service (port 80)
o Requests with path prefix /api → api-app Service (port 80)
• Bind the HTTPRoute to main-gateway


Task 4.4 — Validate and Test
• Verify the Gateway is Ready and has an assigned IP/hostname
• Verify the HTTPRoute is Accepted and Bound to the Gateway
• Test connectivity by sending requests to the Gateway for:
o /web
o /api

---




## Task 4.1 — Deploy Applications and Services

1. Create Deployment `web-app` with 2 replicas using image `nginx:1.21`.
   ```bash
   kubectl apply -f web-deploy.yaml
   ```
2. Create Deployment `api-app` with 2 replicas using image `httpd:2.4`.
   ```bash
   kubectl apply -f api-deploy.yaml
   ```
3. Expose `web-app` as a ClusterIP Service on port 80.
   ```bash
   kubectl apply -f web-svc.yaml
   ```
4. Expose `api-app` as a ClusterIP Service on port 80.
   ```bash
   kubectl apply -f api-svc.yaml
   ```
5. Verify Deployments and Services are running.
   ```bash
   kubectl get deploy,svc
   ```

*(Shortcut: `kubectl apply -f setup.yaml` if provided)*

---

## Task 4.2 — Create Gateway

6. Create a Gateway named `main-gateway` in default namespace.
7. Configure Gateway to listen on port 80 using HTTP protocol.
8. Set hostname to `example.local`.
9. Apply the Gateway manifest.
   ```bash
   kubectl apply -f gateway.yaml
   ```
10. Verify Gateway status.
    ```bash
    kubectl get gateway main-gateway
    ```

---

## Task 4.3 — Create HTTPRoute

11. Create HTTPRoute named `app-routes`.
12. Configure PathPrefix `/web` to route traffic to `web-app` Service on port 80.
13. Configure PathPrefix `/api` to route traffic to `api-app` Service on port 80.
14. Bind the HTTPRoute to `main-gateway`.
15. Apply the HTTPRoute manifest.
    ```bash
    kubectl apply -f httproute.yaml
    ```

---

## Task 4.4 — Validate and Test

16. Verify HTTPRoute is Accepted and attached to the Gateway.
    ```bash
    kubectl get httproute app-routes
    ```
17. Check Gateway has an assigned IP or hostname.
18. Send request to Gateway for `/web` path.
    ```bash
    curl http://<GATEWAY_IP>/web
    ```
19. Send request to Gateway for `/api` path.
    ```bash
    curl http://<GATEWAY_IP>/api
    ```
20. Confirm correct responses from web and api services.
