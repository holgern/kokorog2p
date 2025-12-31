"""kokorog2p - Unified G2P (Grapheme-to-Phoneme) library for Kokoro TTS.

This library provides grapheme-to-phoneme conversion for text-to-speech
applications, with a focus on high-quality English pronunciation.

Example:
    >>> from kokorog2p import phonemize, get_g2p
    >>> # Simple usage
    >>> phonemize("Hello world!")
    'hˈɛlO wˈɜɹld!'
    >>> # Full control
    >>> g2p = get_g2p("en-us")
    >>> tokens = g2p("Hello world!")
    >>> for token in tokens:
    ...     print(f"{token.text} -> {token.phonemes}")
"""

from typing import List, Optional, Union

# Core classes
from kokorog2p.token import GToken
from kokorog2p.base import G2PBase
from kokorog2p.phonemes import (
    US_VOCAB,
    GB_VOCAB,
    from_espeak,
    to_espeak,
    validate_phonemes,
    get_vocab,
    VOWELS,
    CONSONANTS,
)

# Vocabulary encoding/decoding for Kokoro model
from kokorog2p.vocab import (
    encode,
    decode,
    phonemes_to_ids,
    ids_to_phonemes,
    validate_for_kokoro,
    filter_for_kokoro,
    get_vocab as get_kokoro_vocab,
    get_config as get_kokoro_config,
    N_TOKENS,
    PAD_IDX,
)

# Version info
try:
    from kokorog2p._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)

# Lazy imports for optional dependencies
_g2p_cache: dict[str, G2PBase] = {}


def get_g2p(
    language: str = "en-us",
    use_espeak_fallback: bool = True,
    use_spacy: bool = True,
    **kwargs,
) -> G2PBase:
    """Get a G2P instance for the specified language.

    This factory function returns an appropriate G2P instance based on the
    language code. Results are cached for efficiency.

    Args:
        language: Language code (e.g., 'en-us', 'en-gb').
        use_espeak_fallback: Whether to use espeak for out-of-vocabulary words.
        use_spacy: Whether to use spaCy for tokenization and POS tagging.
        **kwargs: Additional arguments passed to the G2P constructor.

    Returns:
        A G2PBase instance for the specified language.

    Raises:
        ValueError: If the language is not supported.

    Example:
        >>> g2p = get_g2p("en-us")
        >>> tokens = g2p("Hello world!")
    """
    # Normalize language code
    lang = language.lower().replace("_", "-")

    # Check cache
    cache_key = f"{lang}:{use_espeak_fallback}:{use_spacy}"
    if cache_key in _g2p_cache:
        return _g2p_cache[cache_key]

    # Create G2P instance based on language
    if lang.startswith("en"):
        from kokorog2p.en import EnglishG2P

        g2p = EnglishG2P(
            language=language,
            use_espeak_fallback=use_espeak_fallback,
            use_spacy=use_spacy,
            **kwargs,
        )
    else:
        raise ValueError(
            f"Unsupported language: {language}. Currently supported: en-us, en-gb"
        )

    _g2p_cache[cache_key] = g2p
    return g2p


def phonemize(
    text: str,
    language: str = "en-us",
    use_espeak_fallback: bool = True,
    use_spacy: bool = True,
) -> str:
    """Convert text to phonemes.

    This is a convenience function that creates a G2P instance and converts
    the text to a phoneme string.

    Args:
        text: Input text to convert.
        language: Language code (e.g., 'en-us', 'en-gb').
        use_espeak_fallback: Whether to use espeak for out-of-vocabulary words.
        use_spacy: Whether to use spaCy for tokenization and POS tagging.

    Returns:
        Phoneme string.

    Example:
        >>> phonemize("Hello world!")
        'hˈɛlO wˈɜɹld!'
    """
    g2p = get_g2p(
        language=language,
        use_espeak_fallback=use_espeak_fallback,
        use_spacy=use_spacy,
    )
    return g2p.phonemize(text)


def tokenize(
    text: str,
    language: str = "en-us",
    use_espeak_fallback: bool = True,
    use_spacy: bool = True,
) -> List[GToken]:
    """Convert text to a list of tokens with phonemes.

    Args:
        text: Input text to convert.
        language: Language code (e.g., 'en-us', 'en-gb').
        use_espeak_fallback: Whether to use espeak for out-of-vocabulary words.
        use_spacy: Whether to use spaCy for tokenization and POS tagging.

    Returns:
        List of GToken objects with phonemes assigned.

    Example:
        >>> tokens = tokenize("Hello world!")
        >>> for token in tokens:
        ...     print(f"{token.text} -> {token.phonemes}")
    """
    g2p = get_g2p(
        language=language,
        use_espeak_fallback=use_espeak_fallback,
        use_spacy=use_spacy,
    )
    return g2p(text)


def clear_cache() -> None:
    """Clear the G2P instance cache.

    This can be useful when you need to free memory or reset state.
    """
    _g2p_cache.clear()


# Public API
__all__ = [
    # Version
    "__version__",
    "__version_tuple__",
    # Core classes
    "GToken",
    "G2PBase",
    # Main functions
    "phonemize",
    "tokenize",
    "get_g2p",
    "clear_cache",
    # Phoneme utilities
    "US_VOCAB",
    "GB_VOCAB",
    "VOWELS",
    "CONSONANTS",
    "from_espeak",
    "to_espeak",
    "validate_phonemes",
    "get_vocab",
    # Kokoro vocabulary encoding
    "encode",
    "decode",
    "phonemes_to_ids",
    "ids_to_phonemes",
    "validate_for_kokoro",
    "filter_for_kokoro",
    "get_kokoro_vocab",
    "get_kokoro_config",
    "N_TOKENS",
    "PAD_IDX",
]
