# ANSIBLE

---



***Question 2: Provision an EC2 instance HU-NAME2-2026 from your local machine (WSL), use the demo-keys mentioned above in the configuration. Once the server is deployed create a user named HU-NAME-2026 which has its own home directory and no access to root folder. Create your own SSH keys named HU-NAME-2026. Upload the keys for the user you created. Connect to the server with the new keys and your username and use ansible to install NGINX, After NGINX is installed. collect system facts of the server deployed in YAML format and publish those facts on the NGINX default web page, so they are visible when you browse to the instance’s IP.***




* Use WSL on the local machine as the control node for provisioning and automation.
* Create an EC2 instance  using the provided demo SSH keys.
* Ensure the instance is reachable over SSH from the local WSL environment.
* Connect to the instance using the demo key and default user.
* Create a new user on the server.
* Assign a dedicated home directory to the new user.
* Restrict the user from accessing the root directory.
* Generate a new SSH key pair locally .
* Upload the public SSH key to the new user’s  file.
* Verify SSH login using the new username and newly created key.
* Configure Ansible inventory to point to the EC2 instance using the new user.
* Use Ansible to install **NGINX** on the EC2 instance.
* Run an Ansible task to gather system facts from the server.
* Convert the collected facts into  **YAML format** .
* Publish the YAML facts file as the default NGINX web page.

---

Question 3: The two servers deployed above need to communicate with each other. Update the hosts file of both the server using ansible in such a way that you can communicate between HU-NAME1-2026 ec2 server and HU-NAME2-2026 server using hostname only.
Use single ansible playbook to achieve this.


1. Identify private IPs of **HU-NAME1-2026** and **HU-NAME2-2026** instances.
2. Define both servers in the Ansible inventory with their hostnames.
3. Create a single Ansible playbook to manage both servers.
4. Use Ansible privilege escalation to modify system files.
5. Update `/etc/hosts` on **both servers** with required hostname mappings.
6. Map HU-NAME1-2026 hostname to its private IP.
7. Map HU-NAME2-2026 hostname to its private IP.
8. Ensure idempotency so duplicate entries are not created.
9. Apply the playbook to all hosts at once.
10. Verify hostname resolution using `ping` or `ssh` by hostname.

---

***Question 4: Create a reusable Ansible role to harden both servers and standardize access.
Role 4:
• Configure a new group trainee and add the user trainee-name (from Question 1) and HU-NAME-2026 (from Question 2) to that group.
• Enforce SSH key-only login by setting PasswordAuthentication no and PermitRootLogin no in sshd_config.
• Ensure sshd is restarted using a handler only when config changes.
• Create a banner file /etc/issue.net that includes the server hostname and environment tags, and enable it via Banner /etc/issue.net in sshd_config.
• Apply this role to both servers using a single play, and verify idempotency.***


* Create a reusable Ansible role named `hardening`.
* Define the role to be applied on **both servers** in a single play.
* Create a new group named `trainee` on all servers.
* Add user `trainee-name` to the `trainee` group.
* Add user `HU-NAME-2026` to the `trainee` group.
* Update `sshd_config` to disable password-based authentication.
* Set `PasswordAuthentication no` in `sshd_config`.
* Disable root login by setting `PermitRootLogin no`.
* Create a banner file at `/etc/issue.net`.
* Populate the banner with hostname and environment tags using variables.
* Enable the SSH banner using `Banner /etc/issue.net`.
* Use a **handler** to restart `sshd` only when configuration changes.
* Ensure all tasks are idempotent using Ansible modules.
* Apply the role to both servers using a single play.
* Re-run the playbook to verify no changes occur (idempotency check).
