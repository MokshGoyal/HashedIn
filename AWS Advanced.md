# AWS ADVANCED

---

***Question 1:
TechStart Inc. is launching a new web-based analytics dashboard for their clients. To ensure fast
deployment and easy scaling, the team decides to containerize the application using Docker and
host it on AWS App Runner. They push the Docker image to Amazon ECR and use a YAML
configuration file to set up the App Runner service. To handle varying traffic, they configure auto
scaling with a minimum of 1 and a maximum of 2 instances. For security and reliability, they enable
HTTPS, set environment variables for API keys, and configure CloudWatch logging to monitor
application performance and troubleshoot issues. This setup allows TechStart Inc. to deliver a
secure, scalable, and well-monitored analytics dashboard with minimal operational overhead.***

*Task: Deploy and manage a Docker Application on AWS App Runner
• Subtask 2.1: Create and Deploy Docker Application
o Build a Docker image (nginx) for your application and push it to Amazon Elastic Container Registry (Amazon ECR).
▪ NGINX image
▪ Private ECR repo created with AWS Managed Keys
o Deploy the application to AWS App Runner
▪ Add Env variables
▪ 0.25 vCPU and 0.5 GB memory
▪ Private Subnets with “hu-primary-vpc-endpoint” and “hu-devops-vpc
connector”*

Subtask 2.1: Create and Deploy Docker Application

**Step 1: Create Private ECR Repository with Managed Keys (Console)**

1. Navigate to the Amazon ECR console and click Create repository.
2. Choose Private for the visibility settings.
3. Enter the repository name: techstart-nginx-repo.
4. Scroll down to Encryption settings and enable KMS encryption.
5. Select AWS managed key from the dropdown.
6. Click Create repository.

**Step 2: Build and Push NGINX Image (Terminal)**
Note: CLI is necessary here to get the local image into AWS ECR.

1. Create a file named Dockerfile on your computer with two lines: FROM nginx:latest and EXPOSE 80.
2. Authenticate Docker to ECR using this command
3. Build the image:
   docker build -t techstart-nginx-repo .
4. Tag the image:
   docker tag techstart-nginx-repo:latest
5. Push the image to ECR:
   docker push

**Step 3: Start App Runner Deployment (Console)**

1. Navigate to the AWS App Runner console and click Create an App Runner service.
2. Under Source and deployment, select Container registry and choose Amazon ECR as the provider.
3. Click Browse and select the techstart-nginx-repo image you just pushed.
4. Under Deployment settings, select Automatic or Manual.
5. Select an existing ECR access role (or let AWS create a new one).
6. Click Next.

---

*• Subtask 2.2: Configure Auto Scaling
o Set up auto scaling for the App Runner service.
o Configure the Concurrency=100, minimum number of instances to 1 and the
maximum to 2.*

**Step 4: Configure Compute and Environment Variables (Console)**

1. On the Configure service page, enter a Service name like techstart-analytics-dashboard.
2. Under Virtual CPU & memory, select exactly 0.25 vCPU and 0.5 GB.
3. Under Environment variables, click Add environment variable to set your API keys (e.g., Key: API_KEY, Value: your-secret-value).

**Step 5: Configure Auto Scaling (Console)**

1. Scroll down to the Auto scaling section.
2. Select Custom configuration and click Add new.
3. Name the configuration (e.g., techstart-scaling).
4. Set Concurrency to 100.
5. Set Minimum size to 1.
6. Set Maximum size to 2.
7. Click Save or Create and use this configuration.

**Step 6: Configure Private Subnets and VPC Connector (Console)**

1. to the Networking section.
2. Under Outgoing network traffic, select Custom VPC.
3. Select the specific Private Subnets associated with that endpoint.
4. Select Security groups.
5. use this VPC connector.

---

• *Subtask 2.3: Enable Service Features and Monitoring
o Enable HTTPS for secure access to the App Runner service.
o Set environment variables for application configuration.
o Enable Amazon CloudWatch logging for the App Runner service to monitor
application health and traffic.*

**Step 7: Enable HTTPS, CloudWatch, and Deploy (Console)**

1. Note on HTTPS: You do not need to manually enable HTTPS. AWS App Runner automatically issues a TLS certificate and provides a secure HTTPS endpoint by default.
2. Note on CloudWatch: Scroll to the Observability section. You do not need to check a box for logs; App Runner automatically enables Amazon CloudWatch logging for application output and deployment logs by default.
3. Once the service status changes to Running, click the Default domain URL provided in the console to securely access your NGINX application.

---

***Question 2:
Scenario Story
Acme Corp wants to automate deployments for their static website (served by Nginx in Docker)
using AWS. The team will use AWS CodeCommit for source control, CodeBuild for building Docker
images, CodePipeline for orchestration, Amazon ECR for storing Docker images, and ECS Fargate
for deployment. They also want notifications, monitoring, and Linux best practices.***

*Task: CI/CD Pipeline for Containerized Application on AWS
• **Subtask 1: Set Up Source Control and Artifact Storage
o Create an AWS CodeCommit repository and push your application code (including
Dockerfile and index.html).
o Create an Amazon Elastic Container Registry (Amazon ECR) repository to store
Docker images.***

Step 1: Create AWS CodeCommit Repository (Console)

1. Open the **AWS CodeCommit** console.
2. Click  **Create repository** .

Step 2: Create and Push Application Code (Terminal)

*Note: You must use the terminal to create files and push them to the repository. Ensure you have Git installed and AWS credentials configured.*

1. Create a project folder and navigate into it:
   mkdir acme-website && cd acme-website
2. Create the **index.html** file:
   echo "`<h1>`Welcome to Acme Corp `</h1>`" > index.html
3. Create the  **Dockerfile** :
   echo "FROM nginx:alpine" > Dockerfile
   echo "COPY index.html /usr/share/nginx/html" >> Dockerfile
4. Initialize Git and add the files:
5. Add the remote repository
6. Push the code to AWS CodeCommit:
   git push -u origin master

Step 3: Create Amazon ECR Repository (Console)

1. Open the **Amazon ECR** console.
2. Create Repo

**• Subtask 2: Configure CI/CD Pipeline with AWS CodePipeline and CodeBuild
o Set up AWS CodePipeline to trigger on changes in CodeCommit.
o Configure AWS CodeBuild to build the Docker image and push it to ECR using a
buildspec.yml file.***

Step 1: Add buildspec.yml to Repository

1. Create a file named **buildspec.yml** in your local repository folder. Add the required code
2. **Push the file to CodeCommit using these commands in your terminal:**
   git  add buildspec.yml
   **git commit -m "Add builds**pec.yml
   **git push origin master**

---

***• Subtask 3: Deploy Application Using AWS ECS Fargate
o Create an Amazon Elastic Container Service (Amazon ECS) cluster and service
using AWS Fargate.
Configure the service to pull the Docker image from ECR and run the container.***

---

***Question 4:
Create Resources using CLI:
• Subtask 2.1: Create ALB, Proxy Methods with Load Balancer URL
• Create an Application Load Balancer (ALB), target group for EC2 and configure
another security group for the ALB to allow inbound HTTP traffic on port 80
• Create a proxy GET and POST method using the Application Load
Balancer URL.
• Ensure that the proxy is configured to route traffic through a Web
Application Firewall (WAF) that you create.
• Using AWS CLI***

***Subtask 2.2: Install and Configure Kinesis Agent and NGINX
• On the Question-3 EC2 instance, install the Kinesis Agent and NGINX.
• Configure NGINX to pass data through a Kinesis stream and direct the data to Kinesis
Data Analytics for further analysis.
• Using AWS CLI***

.Answer:

1)Set variables (region, VPC, subnets, EC2)

2)Create a Security Group for the ALB (allow inbound HTTP 80)

3)CreateTarget Group (EC2 targets) and register the instance

4)Create the Application Load Balancer and Listener (HTTP:80 → Target Group)

5)Create a WAF (WAFv2) Web ACL and associate it to the ALB

6)Create API Gateway “proxy” GET and POST methods pointing to the ALB URL

7)Create a Kinesis Data Stream (for NGINX logs)

8)Grant the EC2 instance permissions to put records into the stream

9)Install NGINX and Kinesis Agent on the EC2 instance (using AWS CLI via SSM)

10)Configure NGINX logging (so the agent has data to ship)

11)Configure the Kinesis Agent to tail NGINX access logs → Kinesis stream

12)Connect Kinesis Data Analytics to the Kinesis stream

13)Validate end-to-end

---

***Question 5:
TechNova is building a serverless REST API to manage customer orders. They want secure,
scalable, and monitored endpoints using AWS services.
Task: Serverless Order Management API
• Subtask 1: API Gateway Setup
o Create a REST API using Amazon API Gateway.
o Define resources and methods for order creation, retrieval, and deletion.
• Subtask 2: Lambda Integration
o Implement AWS Lambda functions for each API endpoint to handle business logic.
o Use environment variables and logging (Linux concepts) in Lambda code.
• Subtask 3: Data Storage with DynamoDB
o Set up an Amazon DynamoDB table to store order data.
o Grant Lambda functions permission to read/write to DynamoDB.
• Subtask 4: Security and Access Control
o Enable API Gateway authorization using AWS Identity and Access Management
(IAM) roles or API keys.
o Configure usage plans and throttling for the API.
• Subtask 5: Architecture Diagram (draw.io)
o Create an architecture diagram in draw.io (diagrams.net) that illustrates the end
to-end solution flow, Ex: Client → API Gateway (REST API) → Lambda
(Create/Get/Delete) → DynamoDB, including IAM authorization/API keys, usage
plans & throttling, and CloudWatch logging/monitoring.***

**1) Create DynamoDB table**

Open AWS Console → DynamoDB → Tables → Create table

* Table name: Orders
* Partition key: orderId
* Add attributes you’ll store: customerID,status,createdAt,items

2)**Create IAM role for Lambda**

Open IAM → Roles → Create role

* Trusted entity: AWS service → Lambda
* Attach permissions:CloudWatch Logs permissions
* DynamoDB permissions scoped to the Order table
* Name role: lamba-order-role

**3)Create Lambda functions**

Answer:Open AWS Console → Lambda → Create function

Create 3 functions :

1)CreateOrderFunction

2)GetOrderFunction

3)DeleteOrderFunction

Execution role: select lamba-order-role

Environment variables (Configuration → Environment variables):

**4)Create REST API in API Gateway**

Open AWS Console → API Gateway → Create API → REST API

API name: OrderManagementAPI

**Add methods and integrate with Lambda**

POST /orders:intergrate with createOrderFunction

GET /orders/{orderId} : integrate with getOrderFunction

Delete /order/{orderId}:intergrate with DeleteOrderFunction

**5)Grant Api Gateway permisson to invoke lambda**

For each Lambda, add an API Gateway trigger

6)**Security and access control choose IAM auth or API Key**

Answer: API Gateway -> API Keys _> Create

* Usage Plans ->Create

  Set throttling : rate and burst limits and Set quota  requests/day
* Attach :Your API stage, your API Key
* For each method, enable: API Key Required = true

**7)Deploy the API and test**

Api gateway -> Deploy API

Stage name: dev

test:

Post/orders {create}

Get/orders/{orderId}

Delete/orders/{orderId}

**8)Monitoring**

answer: Cloudwatch logs
