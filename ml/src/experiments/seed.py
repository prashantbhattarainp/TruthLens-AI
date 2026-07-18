"""Explicit random-seed application and recording for reproducible experiments."""

from __future__ import annotations

import os
import random

import numpy as np


def apply_random_seed(seed: int) -> dict[str, int | str]:
    """Set process-local Python and NumPy seeds and record the deterministic policy."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    return {
        "seed": seed,
        "python_random_seed": seed,
        "numpy_random_seed": seed,
        "pythonhashseed_environment": str(seed),
    }
