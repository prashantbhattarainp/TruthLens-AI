"""Domain-specific failures for reproducible baseline experiments."""


class ExperimentError(Exception):
    """Base failure for the experimentation framework."""


class ExperimentConfigurationError(ExperimentError):
    """Raised when an experiment configuration or approved model is invalid."""


class ExperimentInputError(ExperimentError):
    """Raised when the proposed experiment cohort is malformed or insufficient."""


class ExperimentGovernanceError(ExperimentError):
    """Raised when a run would violate raw-data or output-artifact controls."""
