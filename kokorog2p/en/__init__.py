"""English G2P module for kokorog2p."""

from kokorog2p.en.g2p import EnglishG2P
from kokorog2p.en.lexicon import Lexicon

# Optional: NumberConverter requires num2words
try:
    from kokorog2p.en.numbers import NumberConverter

    __all__ = ["EnglishG2P", "Lexicon", "NumberConverter"]
except ImportError:
    __all__ = ["EnglishG2P", "Lexicon"]
