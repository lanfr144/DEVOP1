#ident @(#)$Format:PROJECT_NAME:FILE_NAME:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$
# Antigravity Development Guidelines & Testing Policy

As mandated by the DevOps architecture team, all tasks—past, present, and future—must adhere to strict professional standards regarding testing and validation.

## 1. Prerequisite Validation
Before any script, build, or configuration is applied, explicit checks must be implemented to ensure the environment is ready.
* **Example**: Check that required environment variables exist and are not placeholder strings.
* **Example**: Check that directories exist or ports are available before spinning up services.

## 2. Post-Task Testing
Closing a task is strictly prohibited until a corresponding test confirms the action succeeded.
* **Example**: After configuring Discord webhooks, an automated test payload must be successfully delivered.
* **Example**: After updating `docker-compose.yml`, `docker compose config` must be run, and the service status verified.

## 3. Retroactive Auditing
For tasks that have already been closed, tests must be retroactively created and executed to guarantee system integrity. 

Failure to follow these professional guidelines will result in rejected pull requests and blocked deployments.
