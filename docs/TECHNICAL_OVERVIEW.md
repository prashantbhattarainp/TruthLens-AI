# Technical Overview

TruthLens AI is a dependency-light browser application with a Node.js API and a Python ML service.

- The frontend is a static SPA with hash routing and vanilla JavaScript modules.
- The backend uses Express, Zod validation, structured logs, request identifiers, and upstream retries.
- The ML service uses FastAPI and Pydantic models.
- Shared JSON schemas describe the public prediction request and response.
- Explainability details are optional response data and are rendered safely with DOM APIs.

Run pnpm test in frontend, pnpm lint in backend, and the ML-service unit tests before shipping a change.
