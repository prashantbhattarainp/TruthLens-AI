"""Reproducible baseline-model experimentation for TruthLens AI."""

# Keep package initialisation import-light so model factories can depend on configuration errors
# without creating a circular import through the experiment runner.
