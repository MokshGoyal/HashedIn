# GCP Basics

---

*Q1. You are working on a Google Cloud project where a team needs visibility into files stored in Cloud Storage.
Scenario:
A GCS bucket is used to store files uploaded by different applications. You are asked to create a solution where:
A Cloud Storage bucket is created and at least three files are uploaded into it.
A Cloud Function is developed that, when triggered, retrieves and lists all the files available in the bucket.

1. **Create a Cloud Storage bucket**

* Use a single bucket to store files uploaded by different applications.
* Choose a globally unique bucket name.
* **Upload files to the bucket**

  * Upload at least three files (can be from different applications).
  * These files act as sample data to verify the solution.
* **Decide the Cloud Function trigger type**

  * Use an  **HTTP-triggered Cloud Function** .
* **Choose the Cloud Function runtime**

  * Select a supported runtime such as **Python** or  **Node.js** .
  * Python is preferred for simplicity and readability.
* **Define the purpose of the Cloud Function**

  * The function will:
    * Connect to the Cloud Storage bucket
    * Retrieve metadata of all objects
    * List file names in the response
* **Use the Cloud Storage client library**

  * Import the official Google Cloud Storage SDK in the function code.
  * This library allows programmatic access to bucket contents.
* **Initialize the Storage client inside the function**

  * The client uses the function’s **service account identity** automatically.
  * No credentials are hardcoded.
* **Reference the target bucket in code**

  * Store the bucket name as:
    * A constant, or
    * An environment variable (preferred for flexibility)
* **Fetch the list of objects from the bucket**

  * Call the API method that retrieves all blobs (files) in the bucket.
  * Iterate over the results to extract file names.
* **Deploy the Cloud Function**

  * Configure it as an  **HTTP-triggered function** .
  * Set authentication based on access needs (public or restricted).
* **Assign required permissions (IAM)**

  * Identify the Cloud Function’s service account.
  * Grant it the role:
    **Storage Object Viewer** on the target bucket.

  ---

  *Your organization receives batch CSV files daily that need to be processed and stored for analytics
  Scenario:
  CSV files are uploaded to Google Cloud Storage, and the cleaned data must be stored in BigQuery for reporting. You are asked to build a serverless ETL pipeline using Dataflow that:
  • Reads batch CSV files from a Cloud Storage bucket
  • Applies a simple transformation (such as filtering records, renaming columns, or adding a derived column)
  • Loads the processed data into a BigQuery table
  Describe the steps you would take to build this pipeline, including dataset/table creation, Dataflow job configuration, and how you would validate the data in BigQuery.*
* Create a Cloud Storage bucket to receive daily batch CSV files.
* Ensure all CSV files follow a consistent schema and format.
* Create a BigQuery dataset for analytics storage.
* Create a BigQuery table with the final transformed schema.
* Choose a **batch Dataflow pipeline** since data arrives daily.
* Build the pipeline using Apache Beam (Python or Java SDK).
* Configure Dataflow to read CSV files from the Cloud Storage bucket.
* Parse CSV rows into structured records and skip invalid entries.
* Apply transformations such as filtering records or renaming columns.
* Add derived columns like ingestion timestamp if required.
* Map transformed data to match the BigQuery table schema.
* Configure BigQuery as the output sink with append mode enabled.
* Assign the Dataflow service account read access to GCS and write access to BigQuery.
* Run the Dataflow job and monitor execution logs.
* Validate data in BigQuery using row counts and sample queries.

---

***Q3. Logging using Cloud Function
Scenario : User gets a log file with a list of, the cloud function will triggered every hour and count the number of users and log it in a separate file in GCS in a human readable format , if there is no change for an hour it should log as no change or if thefile is corrupted it should log with appropriate message.***

1. Store the incoming log file containing user data in a Cloud Storage bucket.
2. Configure a **time-based (hourly) trigger** for the Cloud Function using Cloud Scheduler.
3. Trigger the Cloud Function every hour using cron jobs.
4. When triggered, the function reads the latest log file from the GCS bucket.
5. Parse the log file to extract and count the number of users.
6. Validate the file format before processing to detect corruption.
7. If the file is corrupted or unreadable, generate an error message.
8. Compare the current user count with the previous hour’s count.
9. If the count is unchanged, mark the status as “No change detected”.
10. If the count has changed, record the updated user count.

---

4. ***Create a cloud function that will be triggered based on Ip creation This should checkthe Ip reserved is Public Ip if so it should delete it only if the Labels are not present , If Label with key as “Project” is present with any value it should not delete the***

1. Enable logging-based triggers for Compute Engine IP address creation events.
2. Create an **event-driven Cloud Function** triggered by IP reservation creation logs.
3. Configure the trigger to listen for static IP address creation activity.
4. When triggered, extract the IP resource details from the event payload.
5. Check whether the reserved IP is a  **Public IP** .
6. If the IP is not public, exit without any action.
7. If the IP is public, check for the presence of resource labels.
8. Verify whether a label with key **“Project”** exists on the IP resource.
9. If the “Project” label is present (any value), do not delete the IP.
10. If the “Project” label is missing, mark the IP as non-compliant.
11. Delete the public IP address automatically.
12. Log the deletion action with IP name and timestamp.
13. Log a skip message when deletion is not performed due to label presence.
14. Handle API or permission errors gracefully with proper logging.
15. Grant the Cloud Function service account permission to view and delete IP addresses.
