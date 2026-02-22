# ***IAC DAY - 2***

---

Objective: Deploy a Google Cloud Infrastructure Manager (Terraform) stack to provision Cloud Storage and Compute Engine with enforced guardrails
Important: Use this service account for the Google Cloud Infra Manager (hu-iac-test-sa)
Tasks:
•	Create a Cloud Storage bucket for marketing asset
•	Enforce immutability terraform based guardrails based on env (if env=prod, force Object Versioning enabled and apply a retention policy; fail deployment if retention is missing/below minimum).
•	Deploy a Compute Engine VM for simple file-moving/processing.
•	Enforce machine-type terraform based guardrails based on machine_type and GPU configuration (if machine_type starts with n1- or an NVIDIA GPU is requested, downgrade to e2-micro, remove GPU attachment, and append a warning to VM metadata).
•	Implement dynamic boot disk sizing using workload_intensity (1–10) where Size (GB) = (workload_intensity × 10) + 20.


---





* Initialize a Terraform project and configure the Google provider to use Google Cloud Infrastructure Manager with the specified service account.
* Define required input variables such as environment (env), machine_type, gpu_requested, workload_intensity, region, and zone.
* Create a Cloud Storage bucket resource intended for marketing assets with a deterministic name and proper location settings.
* Implement conditional logic based on env to enforce immutability guardrails for the storage bucket.
* If env is set to prod, force Object Versioning to be enabled on the Cloud Storage bucket.
* If env is set to prod, define and apply a retention policy with a minimum required retention period.
* Add Terraform validation or precondition logic to fail the deployment if env is prod and the retention policy is missing or below the minimum threshold.
* Allow non-production environments to create the bucket without mandatory retention enforcement.
* Define local values or conditional expressions to evaluate requested machine_type and GPU configuration.
* If the machine_type starts with n1- or an NVIDIA GPU is requested, override the machine type to e2-micro.
* If the machine type is overridden, ensure any GPU attachment configuration is removed.
* Append a warning message to the VM metadata indicating that the requested machine type or GPU was downgraded due to guardrails.
* If no guardrail violation occurs, allow the originally requested machine type and GPU configuration.
* Calculate boot disk size dynamically using the formula: Size (GB) = (workload_intensity × 10) + 20.
* Enforce validation on workload_intensity to allow only values between 1 and 10.
* Create a Compute Engine VM resource using the resolved machine type, disk size, and metadata configuration.
* Configure the VM with a basic startup script or tooling suitable for simple file moving or processing tasks.
* Attach the dynamically sized boot disk to the VM during creation.
* Ensure all guardrail logic is implemented directly in Terraform using conditionals, locals, and validations.
* Initialize the deployment using Terraform initialization via Infrastructure Manager.
