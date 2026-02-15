KUBERNETES DAY 1

---



Question 5: PV, PVC, Services, Network Policy


Objective: Provision persistent storage, expose applications via Services, validate in-cluster service discovery, and enforce cross namespace controls using NetworkPolicies.
Task 5.1 — PersistentVolume, PersistentVolumeClaim, and Data Persistence
• Create a PersistentVolume (PV) named logs-pv that:
o Uses hostPath: /var/logs
o Access modes: ReadWriteOnce and ReadOnlyMany
o Storage capacity: 5Gi
• Verify the PV status shows Available
• Create a PersistentVolumeClaim (PVC) named logs-pvc that:
o Uses access mode ReadWriteOnce
o Requests capacity 2Gi
• Verify the PV status shows Bound
• Create a Pod running image nginx that mounts logs-pvc at /var/log/nginx
• Open an interactive shell to the container and create file my-nginx.log in /var/log/nginx
• Exit the Pod
• Delete the Pod and recreate it using the same YAML manifest
• Open an interactive shell again and verify the file my-nginx.log still exists in /var/log/nginx


Task 5.2 — NodePort Service with Multiple Ports
You need to expose a web application externally and also expose a metrics endpoint.
• Create a Deployment named webapp using image nginxdemos/hello:0.4-plain-text with three replicas
• Create a Service named webapp-service with:
o Type: NodePort
o Port 80 exposed as port 80, named web
o Port 9090 exposed as port 9090, named metrics
o NodePort for web set to 30080
o Selectors that correctly target the webapp Pods
• Verify the Service works by accessing it via the ClusterIP



Task 5.3 — ClusterIP Service Discovery (Frontend → Database)
You have a backend database and a frontend app; both must remain internal to the cluster.
• Create a Deployment named database with one replica using image mysql:9.4.0 and set:
o MYSQL_ROOT_PASSWORD=secretpass
o MYSQL_DATABASE=myapp
• Create a ClusterIP Service named database-service that:
o Exposes port 3306
o Targets the database Pods
• Create a Deployment named frontend with two replicas using image busybox:1.35 that runs:
o sh -c "while true; do nc -zv database-service 3306; sleep 5; done"
• Verify the frontend Pods can resolve database-service and successfully connect to port 3306



Task 5.4 — Cross-Namespace NetworkPolicies
Two teams operate in separate namespaces. Implement policies controlling cross-namespace communication.
• Download 4.4-setup.yaml
• Create the objects from setup.yaml
• Inspect objects in namespaces team-alpha and team-beta
• In namespace team-alpha, create a NetworkPolicy that:
o Allows the alpha-app Pod to connect only to the team-beta namespace
o Denies all other egress traffic except DNS
• In namespace team-beta, create a NetworkPolicy that:
o Allows the beta-app Pod to receive traffic from the team-alpha namespace on port 80
o Denies all other ingress traffic
• Test and verify:
o alpha-app can reach beta-app
o alpha-app cannot reach external sites
o beta-app cannot receive traffic from other sources



---

## Task 5.1 — PV, PVC, and Data Persistence

1. Create a PersistentVolume `logs-pv` using hostPath `/var/logs` with 5Gi storage.
   ```yaml
   accessModes: [ReadWriteOnce, ReadOnlyMany]
   ```
2. Apply the PV manifest.
   ```bash
   kubectl apply -f logs-pv.yaml
   ```
3. Verify PV status is  **Available** .
   ```bash
   kubectl get pv
   ```
4. Create a PersistentVolumeClaim `logs-pvc` requesting 2Gi with `ReadWriteOnce`.
5. Apply the PVC manifest.
   ```bash
   kubectl apply -f logs-pvc.yaml
   ```
6. Verify PV status changes to  **Bound** .
   ```bash
   kubectl get pv,pvc
   ```
7. Create a Pod using image `nginx` mounting `logs-pvc` at `/var/log/nginx`.
8. Apply the Pod manifest.
   ```bash
   kubectl apply -f nginx-pod.yaml
   ```
9. Open interactive shell inside the Pod.
   ```bash
   kubectl exec -it nginx-pod -- sh
   ```
10. Create file `my-nginx.log` inside `/var/log/nginx`.
11. Exit the Pod shell.
12. Delete the Pod.

```bash
kubectl delete pod nginx-pod
```

13. Recreate the Pod using the same YAML.
14. Exec into the Pod again and verify `my-nginx.log` still exists.
15. Confirm data persistence through PVC.

---

## Task 5.2 — NodePort Service with Multiple Ports

1. Create a Deployment `webapp` with 3 replicas using image `nginxdemos/hello:0.4-plain-text`.
2. Apply the Deployment manifest.
   ```bash
   kubectl apply -f webapp-deploy.yaml
   ```
3. Create a NodePort Service `webapp-service`.
4. Expose port `80` named `web` with NodePort `30080`.
5. Expose port `9090` named `metrics`.
6. Configure selectors to target `webapp` Pods.
7. Apply the Service manifest.
   ```bash
   kubectl apply -f webapp-svc.yaml
   ```
8. Verify Service details.
   ```bash
   kubectl get svc webapp-service
   ```
9. Access the service using ClusterIP from inside the cluster.
10. Confirm both ports respond correctly.

---

## Task 5.3 — ClusterIP Service Discovery (Frontend → Database)

1. Create a Deployment `database` with image `mysql:9.4.0`.
2. Set environment variables `MYSQL_ROOT_PASSWORD` and `MYSQL_DATABASE`.
3. Apply the database Deployment.
   ```bash
   kubectl apply -f database-deploy.yaml
   ```
4. Create a ClusterIP Service `database-service` exposing port `3306`.
5. Apply the Service manifest.
   ```bash
   kubectl apply -f database-svc.yaml
   ```
6. Create a Deployment `frontend` using image `busybox:1.35`.
7. Configure command to continuously test connectivity using `nc`.
8. Apply the frontend Deployment.
   ```bash
   kubectl apply -f frontend-deploy.yaml
   ```
9. Check frontend Pod logs.
   ```bash
   kubectl logs <frontend-pod>
   ```
10. Verify successful resolution of `database-service` and port `3306`.

---

## Task 5.4 — Cross-Namespace NetworkPolicies

1. Download `4.4-setup.yaml`.
2. Create all objects from the file.
   ```bash
   kubectl apply -f 4.4-setup.yaml
   ```
3. Inspect Pods and Services in namespaces `team-alpha` and `team-beta`.
   ```bash
   kubectl get all -n team-alpha
   kubectl get all -n team-beta
   ```
4. In `team-alpha`, create a NetworkPolicy for egress control.
5. Allow `alpha-app` Pod to communicate only with namespace `team-beta`.
6. Allow DNS traffic explicitly.
7. Deny all other egress traffic.
8. Apply the NetworkPolicy.
   ```bash
   kubectl apply -f alpha-egress-policy.yaml -n team-alpha
   ```
9. In `team-beta`, create an ingress NetworkPolicy.
10. Allow traffic only from `team-alpha` namespace on port `80`.
11. Deny all other ingress traffic.
12. Apply the NetworkPolicy.

```bash
kubectl apply -f beta-ingress-policy.yaml -n team-beta
```

13. Exec into `alpha-app` Pod and test connectivity to `beta-app`.
14. Verify `alpha-app` cannot access external sites.
15. Verify `beta-app` rejects traffic from other namespaces.
