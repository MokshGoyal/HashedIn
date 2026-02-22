# ***IAC DAY -1***

---

**Assignment 2**

**Deploy an
EC2 Instance with User Data and S3 Access using Terraform.**

**Objective:** Write a Terraform configuration to provision a **t2.micro** Amazon Elastic Compute Cloud (Amazon EC2) instance with a bootstrapping script that
prints instance metadata and displays a “Hello World” banner using  **figlet** , plus a security group restricted to your public IP and permissions to access objects in the Amazon Simple Storage Service (Amazon S3) bucket created in Assignment 1.

**Tasks:**

* **Provision an EC2 instance**
  (instance type  **t2.micro** ) using an Amazon Machine Image (AMI) of your choice, and apply appropriate tags (e.g., name, environment).
* **Add user data (bootstrap script)** that, on first boot:

  * retrieves and displays **EC2 instance metadata** (at minimum show instance ID and availability zone)
  * installs **figlet**
  * prints a banner message: **“Hello World!”**
* **Configure a security group** that:

  * allows inbound  **SSH (22)** ,  **HTTP (80)** , and **HTTPS (443)** **only from your system’s public IP**
  * permits **all outbound traffic**
* **Enable S3 access from the instance** to read an object from the bucket created in Assignment 1

  * Granting **least-privilege** permissions required to list the bucket and read objects (scope access to the specific bucket and, if applicable, the relevant prefix)
* **Demonstrate access to S3** (in documentation) run a command to retrieve a test object from the Assignment 1 bucket (e.g., using the AWS Command Line Interface (AWS CLI) or equivalent tooling available on the AMI).

---

ANSWER -

* Initialize a new Terraform project directory and configure the AWS provider with the correct region and credentials.
* Identify the S3 bucket created in Assignment 1 and note its bucket name for IAM permission scoping.
* Create an IAM role for EC2 that allows least-privilege S3 access.
* Attach an IAM policy to the role with permissions limited only to the Assignment 1 S3 bucket and required actions.
* Create an IAM instance profile and associate it with the EC2 IAM role.
* Fetch your current public IP address and use it to restrict inbound traffic rules.
* Define a security group that allows inbound SSH (22), HTTP (80), and HTTPS (443) only from your public IP, and allows all outbound traffic.
* Choose a suitable Amazon Linux AMI that supports EC2 instance metadata service and package installation.
* Define an EC2 instance resource with instance type set to t2.micro and apply meaningful tags.
* Attach the previously created security group and IAM instance profile to the EC2 instance.
* Add a user data bootstrap script that retrieves instance metadata such as instance ID and availability zone using the metadata service.
* In the same user data script, install figlet using the system package manager.
* Use figlet in the user data script to display a “Hello World!” banner during the first boot of the instance.
* Initialize the Terraform working directory using terraform init.
* Review the execution plan using terraform plan to verify EC2, IAM, and security group resources.
* Apply the configuration using terraform apply to provision the infrastructure.
* After the instance is running, connect via SSH and verify that the metadata output and figlet banner were printed during boot.
* Demonstrate S3 access by running an AWS CLI command on the instance to retrieve a test object from the Assignment 1 bucket

---

**Assignment 5**

**Configure
Azure Blob Storage and an Azure Function**

**Objective:** Set up Azure Blob Storage to host an HTML page and deploy an Azure Function that runs and prints a simple message with the source code uploaded via Terraform.

**Tasks:**

1. Deploy Azure Blob Storage and upload an HTML page (e.g., index.html) using Terraform.
2. Create an Azure Function (language of your choice) that runs and prints/logs a simple message (e.g., “Hello from Function”), and ensure the **function source code artifact is packaged and uploaded from Terraform**
3. Write Terraform tests (terraform test) to verify the deployment:

**Storage
(tests):**

* Test that the Storage Account enforces **HTTPS-only** (secure transfer required).
* Test that **static website hosting** is enabled and the **index document** is set to index.html (if using static website).
* Test that the uploaded blob/object exists with **name **index.html and **content type** text/html.

**Azure
Function (tests):**

* Test that the Function App is deployed with the expected **runtime stack/version** (based on your chosen language).
* Test that the Function App is configured to run from a **Terraform-managed deployment package/artifact** (e.g., zip deploy / run-from-package).

---



* Initialize a new Terraform project and configure the Azure provider with the required subscription, tenant, and authentication details.
* Create a resource group to logically group all Azure resources for the assignment.
* Define an Azure Storage Account with secure transfer (HTTPS-only) enabled.
* Enable static website hosting on the Storage Account and configure the index document as index.html.
* Prepare a simple HTML file (index.html) locally with basic content for static hosting.
* Upload the index.html file to the special static website container using a Terraform-managed blob resource.
* Ensure the uploaded blob explicitly sets the content type to text/html.
* Create a Storage Account container or reuse required storage resources needed by the Azure Function App.
* Choose a function runtime (for example: Node.js, Python, or .NET) and decide the runtime version to be validated later in tests.
* Package the Azure Function source code into a deployment artifact (for example, a zip file) as part of the Terraform workflow.
* Upload the function deployment package to a Terraform-managed location (such as Blob Storage or inline artifact reference).
* Create an Azure Function App configured to run using the uploaded deployment package (run-from-package or zip deployment).
* Configure the Function App with the expected runtime stack and version matching the chosen language.
* Ensure the Function App logs or prints a simple message such as “Hello from Function” when executed.
* Initialize Terraform tests using terraform test with a dedicated test configuration directory.
* Write a test to verify that the Storage Account enforces HTTPS-only (secure transfer required is true).
* Write a test to verify that static website hosting is enabled and the index document is set to index.html.
* Write a test to verify that a blob named index.html exists and has the content type set to text/html.
* Write a test to verify that the Function App is deployed with the expected runtime stack and runtime version.
* Write a test to verify that the Function App is configured to run from a Terraform-managed deployment package (for example, run-from-package enabled).
