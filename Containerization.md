# ***CONTAINERIZATION AND VIRTUALIZATION***


---

***QUESTION 2:
Containerize and run a two-tier application using Podman:
Tier 1: Flask REST API
Tier 2: MySQL Database
Objective:
The objective is to validate how you can design, containerize, and reliably run a simple multi
container application (API + database) using rootless Podman in a way that is secure,
configurable, persistent, and usable from a Windows browser through WSL.
Note: Zip file will be shared.
Mandatory Requirements
➢ Containerize flask app given in the repo with best practices.
➢ The Flask app should allow users to add and list tasks stored in MySQL.
➢ Flask app and MySQL must run in separate containers
➢ Use rootless Podman
➢ Use a Podman network or pod
➢ MySQL version must be build-time configurable
➢ Flask container must wait for DB readiness
➢ Containers must restart cleanly without data loss
➢ Must be accessible from Windows browser via WSL
NOTE:  Name of the database should be “mydb” and the mysql container should be named
as “mysql” only, Details given below
DB name- hudb, username-huuser, password- hupassword***



* **Create Podman Network** : Create a dedicated network to allow the Flask app and MySQL database to communicate securely.
* **Create Persistent Volume** : Create a Podman volume to ensure database records persist even if the container restarts.
* **Run MySQL Container** : Launch the MySQL container  attached to the network and mount the volume
* **Configure DB Credentials** : Set the environment variables for the MySQL container:
* **Prepare Flask Dockerfile** : Create a `Dockerfile` for the Flask application that uses a Python base image, copies the code, and installs dependencies from `requirements.txt`.
* **Implement Wait Strategy** : Ensure the Flask application (or its entry script) includes a check to wait for the database to be fully ready before starting the server.
* **Build Flask Image** : Run the `podman build` command to create the application image, ensuring the MySQL version is passed as a build argument if required.
* **Run Flask Container** : Start the Flask container on the same network and publish port `5000` to the host (5000:5000).
* **Connect App to DB** : Pass the database hostname `mysql` and the credentials to the Flask container as environment variables.
* **Verify in Browser** : Open a browser on Windows and navigate to `http://localhost:5000` to confirm you can add and list tasks via the WSL forwarded port.

---



***Question 3
Your team is containerizing an app (any language) using Buildah/Podman
Objective:
You are asked to build the same application in two different ways:***

***Using a single-stage Dockerfile

Tasks:
Using a multi-stage Dockerfile
➢ Build the application using a single-stage image and note the final image size.
➢ Build the same application using a multi-stage image and note the final image size.
Compare both image sizes.
➢ Clearly explain what components were removed in the final multi-stage image (for
example: build tools, source code, dev dependencies, cache, etc.).
➢ Explain why multi-stage builds reduce image size.***



1. **Create a Simple App** : Write a small program in a compiled language like Go, Java, or C++
2. **Write Single-Stage Dockerfile** : Create a file named `Dockerfile.single` that starts with a full base image copies the source code, and compiles it.
3. **Build Single-Stage Image** : Run the build command (e.g., `podman build -f Dockerfile.single -t app-single`) to create the first image.
4. **Check Image Size** : Run `podman images` and write down the size of `app-single` 
5. **Write Multi-Stage Dockerfile** : Create a `Dockerfile.multi` with two sections: a "Builder" stage to compile the code and a "Runner" stage for the final app.
6. **Configure Builder Stage** : In the first section, use the full SDK image (like `golang:alpine`) to copy the source and build the binary.
7. **Configure Runner Stage** : In the second section, use a tiny base image (like `alpine` or `distroless`) and copy **only** the compiled binary from the Builder stage.
8. **Build Multi-Stage Image** : Run the build command (e.g., `podman build -f Dockerfile.multi -t app-multi`) to create the optimized image.
9. **Compare Sizes** : Run `podman images` again and compare `app-multi` against `app-single` to see the massive size reduction (often 90% smaller).
10. **Explain the Difference** : Note that the multi-stage image is smaller because it discarded the heavy compilers, source code, and build tools, keeping only what is needed to run the app.
