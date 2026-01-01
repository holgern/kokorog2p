"""German G2P module for kokorog2p.

This module provides grapheme-to-phoneme conversion for German text.
"""

from kokorog2p.de.g2p import GermanG2P
from kokorog2p.de.lexicon import GermanLexicon
from kokorog2p.de.numbers import (
    GermanNumberConverter,
    expand_number,
    number_to_german,
    ordinal_to_german,
)

__all__ = [
    "GermanG2P",
    "GermanLexicon",
    "GermanNumberConverter",
    "expand_number",
    "number_to_german",
    "ordinal_to_german",
]
