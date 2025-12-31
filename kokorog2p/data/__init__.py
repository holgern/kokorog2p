"""Data files for kokorog2p.

This module provides access to bundled data files including
the Kokoro model configuration.
"""

import importlib.resources
import json
from typing import Any

# Use importlib.resources for Python 3.9+ compatible resource access
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files  # type: ignore


def load_kokoro_config() -> dict[str, Any]:
    """Load the Kokoro model configuration.

    Returns:
        Dictionary containing the model configuration including vocabulary.
    """
    config_file = files(__package__).joinpath("kokoro_config.json")
    return json.loads(config_file.read_text(encoding="utf-8"))


def get_kokoro_vocab() -> dict[str, int]:
    """Get the Kokoro vocabulary mapping.

    Returns:
        Dictionary mapping tokens (phonemes, punctuation) to indices.
    """
    config = load_kokoro_config()
    return config["vocab"]
