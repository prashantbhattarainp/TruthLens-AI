"""Domain-specific failures for feature extraction."""


class FeatureError(Exception):
    """Base failure for the feature-engineering package."""


class FeatureConfigurationError(FeatureError):
    """Raised when a feature configuration is incomplete or incompatible."""


class FeatureExtractionError(FeatureError):
    """Raised when a feature representation cannot be fitted or transformed."""


class FeatureGovernanceError(FeatureError):
    """Raised when a feature run would violate the immutable-raw boundary."""
