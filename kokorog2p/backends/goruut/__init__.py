"""Goruut/pygoruut backend for phonemization.

This package provides pygoruut integration for converting text to phonemes.
Pygoruut is an alternative to espeak-ng that supports many languages.

Copyright 2024 kokorog2p contributors
Licensed under the Apache License, Version 2.0
"""

from kokorog2p.backends.goruut.backend import GoruutBackend

__all__ = [
    "GoruutBackend",
]
