# AWS reference architecture

This non-production reference sketches isolated subnets, encrypted managed PostgreSQL/Redis, an ECS cluster, and immutable/scanned ECR repositories. It deliberately omits public ingress, DNS, secrets, task definitions, autoscaling, identity federation, observability export, and state backend because those require account-specific threat and cost review.

Run `terraform fmt -check -recursive`. Do not apply without supplying a remote encrypted state backend, reviewing current engine/provider availability and cost, adding least-privilege application security groups, and completing the deployment/security checklist. No AWS environment has been created or validated by this repository.
