"""Domain-specific preprocessing errors."""


class PreprocessingError(Exception):
    """Base error for preprocessing failures."""


class ConfigurationError(PreprocessingError):
    """Raised when a preprocessing configuration is invalid."""


class ModelCapabilityError(PreprocessingError):
    """Raised when enabled NLP steps require an unavailable spaCy capability."""


class GovernanceError(PreprocessingError):
    """Raised when a run would violate immutable-raw-data safeguards."""
