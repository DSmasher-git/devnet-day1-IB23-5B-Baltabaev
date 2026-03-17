# Day 3 Report – School Library API

## Objective
Complete API automation tasks, authentication, and Postman integration.

## Tasks Completed

### B2 – Token & API Operations
- Successfully obtained access token via `/loginViaBasic`
- Used token for authorization (Bearer / X-API-KEY)
- Tested the following endpoints:
  - GET /books
  - POST /books
  - DELETE /books/{id}

### B3 – Postman
- Created Postman Collection
- Configured Environment variables:
  - base_url
  - token
- Tested API requests in Postman
- Exported:
  - postman_collection.json
  - postman_environment.json

### Automation
- Implemented Python script for:
  - Authentication
  - Adding books
  - Generating artifacts
- All pytest tests passed successfully.
- summary.json generated and validated via schema.

## Result
All Day 3 requirements completed successfully.