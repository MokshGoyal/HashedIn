# ***AZURE BASICS***

---


***Question:3***

Create a  Standard Load Balancer .

***It must serve traffic to the previously created Virtual Machine Scale Set on  Port 80 . Configure the Load Balancer accordingly.***

* Provision Load Balancer Resource : Create a new Standard SKU Load Balancer resource in the same region as your VMSS
* Configure Frontend IP : Define a Frontend IP configuration assigned with a Public IP address to handle incoming internet traffic.
* Create Backend Pool : Initialize a Backend Pool to define the group of resources that will receive traffic.
* Associate VMSS : Link the Backend Pool directly to the network interface configurations of the previously created  Virtual Machine Scale Set .
* Define Health Probe : Create a Health Probe to monitor the status of the backend instances.
* Configure Probe Protocol : Set the Health Probe protocol to TCP (or HTTP) and configure it to check Port 80 to ensure application availability.
* Create Load Balancing Rule : configure a Load Balancing Rule to govern how traffic is distributed.
* Map Traffic Ports : Within the Load Balancing Rule, map Frontend Port 80 to Backend Port 80 to direct HTTP traffic correctly.
* Link Probe to Rule : Associate the Health Probe with the Load Balancing Rule to ensure traffic is only routed to healthy VMSS instances.
* Finalize Deployment : Deploy the resource to your Resource Group and validate that the Load Balancer is active and routing traffic to the scale set.

---



***Question:5***

***Create a Storage Account , provision a *******static website hosting facility. and enable Azure Front door.***


1. **Create a Storage Account** : Make a new Storage Account in your Resource Group to hold your website files.
3. **Turn on Static Website** : Go to the "Static website" section in the menu and switch it to  **Enabled** .
4. **Set the Main File** : Type `index.html` in the "Index document name" box so the browser knows which page to open first.
5. **Save the Link** : Copy the **Primary endpoint** URL that appears; this is the direct link to your storage website.
6. **Upload Your File** : Go to the new **$web** container and upload your `index.html` file there.
7. **Create Front Door** : Search for **Azure Front Door and CDN** and create a new "Standard" profile.
8. **Add an Endpoint** : In the Front Door designer, add an **Endpoint** to create the main URL your users will visit.
9. **Connect the Origin** : Add an **Origin Group** and paste the storage account link (from Step 4) as the target address.
10. **Set the Route** : Create a **Route** that tells Front Door to send all traffic from the Endpoint to your Storage Account.
11. **Deploy and Test** : Click **Create** to finish the setup, wait for it to deploy, and then open the Front Door URL to see your site.
