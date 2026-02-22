# ***CI/CD DAY - 2***

---



Question-3 (Jenkins).

Scenario: You manage a Jenkins pipeline for a Java application with multiple long-lived branches
(main, develop, release/*). Builds must:

• Run on different agent labels depending on the branch (e.g., main on prod agents, develop on dev-agents, release/* on release-agents).
• Accept a parameter to optionally skip integration tests.
• Archive build artifacts only for successful builds on main and release/*. Task: Design a Jenkins file (Declarative or Scripted) that:
• Implements dynamic agent selection and parameterized test skipping.
• Ensures artifact archiving is conditional as described.
• Explain your logic for agent selection and artifact handling, and how you would test the pipeline for all branch types and parameter combinations.



---



* Use a Jenkins Multibranch Pipeline so branch names are available at runtime.
* Define a boolean parameter to optionally skip integration tests.
* Disable the global agent and select agents dynamically at the stage level.
* Detect the branch name using the pipeline environment variable.
* Run builds on prod-agents when the branch is main.
* Run builds on dev-agents when the branch is develop.
* Run builds on release-agents when the branch name matches release/*.
* Always run the compilation stage for all branches.
* Always run unit tests for all branches.
* Execute integration tests only when the skip parameter is false.
* Skip the integration test stage when the parameter is enabled.
* Ensure the build fails if compilation or required tests fail.
* Generate build artifacts during the build process.
* Archive artifacts only when the build result is successful.
* Restrict artifact archiving to main and release/* branches.
* Do not archive artifacts for develop branch builds.
* Ensure failed builds never archive artifacts regardless of branch.
* Test the pipeline by running builds on main, develop, and release/* branches.
* Validate correct agent selection for each branch.
* Validate artifact archiving behavior for all branch and parameter combinations.

---



Question-5 (GitHub)

You have to trigger the pipeline manually. Use the custom actions from the previous question.Implement the main pipeline with a matrix strategy. The docker image should be pushed to AWS ECR registry. Use secure authentication to AWS (OIDC Setup). Implement the gated deployment in each environment. Approval of the gated deployment should be you and the Track helpers.


1. Create a GitHub Actions workflow configured to be triggered manually using workflow_dispatch.
2. Reuse the custom GitHub Actions created in the previous question for build, test, and deployment steps.
3. Define a matrix strategy in the main pipeline to run the workflow across multiple environments.
4. Include environments such as dev, staging, and prod in the matrix configuration.
5. Build the Docker image once per matrix execution using the custom build action.
6. Tag the Docker image dynamically based on the environment and commit reference.
7. Configure AWS authentication using GitHub Actions OpenID Connect (OIDC) without static AWS credentials.
8. Create an AWS IAM role with a trust policy allowing GitHub OIDC access.
9. Grant the IAM role least-privilege permissions required to authenticate and push images to Amazon ECR.
10. Authenticate the workflow to AWS ECR using the assumed IAM role.
11. Push the Docker image to the appropriate AWS ECR repository.
12. Configure GitHub Environments corresponding to each deployment stage.
13. Enable required reviewers for each environment to enforce gated deployment.
14. Set the required approvers as yourself and the Track helpers.
15. Ensure deployment jobs are associated with GitHub Environments to enforce approval gates.
16. Prevent production deployment from proceeding without explicit approval.
17. Verify that each environment deployment waits for approval before execution.
18. Manually trigger the pipeline and test execution for each matrix environment.
19. Confirm successful image push to AWS ECR for approved environments.
20. Validate that unapproved deployments do not proceed.
