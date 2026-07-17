# TruthLens AI

TruthLens AI is a research-oriented platform for explainable fake news detection in Indian digital media.

## Project overview

The platform is being designed for a production-quality portfolio, future research publication, and an MS admissions profile. It separates the frontend, Node.js backend, and Python machine-learning service so each component can evolve independently.

## Development status

Phase 1 - Milestone 1 is complete: the professional repository foundation and development standards are in place. No application functionality, API, dataset, or machine-learning implementation is included in this milestone.

## Planned architecture

```text
Frontend (HTML, CSS, JavaScript)
        |
Node.js and Express backend
        |
Python FastAPI machine-learning service
```

## Repository structure

```text
frontend/     Static web application
backend/      Node.js and Express service
ml-service/   Python machine-learning service
datasets/     Governed data storage areas
research/     Research records, notebooks, and reports
docs/         Engineering and architecture documentation
shared/       Cross-service contracts and shared definitions
scripts/      Project automation scripts
docker/       Container configuration
tests/        Cross-project test resources
```

## Development workflow

Work is implemented through focused feature branches, reviewed through pull requests into `develop`, and only promoted to `main` after the integrated project is stable.
