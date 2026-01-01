"""kokorog2p - Unified G2P (Grapheme-to-Phoneme) library for Kokoro TTS.

This library provides grapheme-to-phoneme conversion for text-to-speech
applications, supporting multiple languages including English, German, French,
Czech, Chinese, and Japanese.

Supported Languages:
    - English (US/GB): 100k+ dictionary, POS tagging, stress assignment
    - German: 738k+ dictionary, phonological rules, number handling
    - French: Gold dictionary, liaison rules, espeak fallback
    - Czech: Rule-based phonology
    - Chinese: pypinyin with tone sandhi
    - Japanese: pyopenjtalk with mora-based phonemes

Example:
    >>> from kokorog2p import phonemize, get_g2p
    >>> # English
    >>> phonemize("Hello world!", language="en-us")
    'hˈɛlO wˈɜɹld!'
    >>> # German
    >>> phonemize("Guten Tag!", language="de")
    'ɡuːtn̩ taːk!'
    >>> # French
    >>> phonemize("Bonjour!", language="fr")
    'bɔ̃ʒuʁ!'
    >>> # Full control with tokens
    >>> g2p = get_g2p("de")
    >>> tokens = g2p("Das Wetter ist schön.")
    >>> for token in tokens:
    ...     print(f"{token.text} -> {token.phonemes}")
"""

from typing import Any, Literal, Optional, Union

# Core classes
from kokorog2p.token import GToken
from kokorog2p.base import G2PBase
from kokorog2p.phonemes import (
    US_VOCAB,
    GB_VOCAB,
    from_espeak,
    from_goruut,
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

# Punctuation handling
from kokorog2p.punctuation import (
    Punctuation,
    normalize_punctuation,
    filter_punctuation,
    is_kokoro_punctuation,
    KOKORO_PUNCTUATION,
)

# Word mismatch detection
from kokorog2p.words_mismatch import (
    MismatchMode,
    MismatchInfo,
    MismatchStats,
    detect_mismatches,
    check_word_alignment,
    count_words,
)

# Version info
try:
    from kokorog2p._version import __version__, __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)

# Lazy imports for optional dependencies
_g2p_cache: dict[str, G2PBase] = {}

# Backend type hint
BackendType = Literal["espeak", "goruut"]


def get_g2p(
    language: str = "en-us",
    use_espeak_fallback: bool = True,
    use_spacy: bool = True,
    backend: BackendType = "espeak",
    **kwargs: Any,
) -> G2PBase:
    """Get a G2P instance for the specified language.

    This factory function returns an appropriate G2P instance based on the
    language code. Results are cached for efficiency.

    Args:
        language: Language code (e.g., 'en-us', 'en-gb', 'zh', 'ja', 'fr', etc.).
        use_espeak_fallback: Whether to use espeak for out-of-vocabulary words
            (only applies when backend="espeak").
        use_spacy: Whether to use spaCy for tokenization and POS tagging
            (only applies to English).
        backend: Phonemization backend to use: "espeak" (default) or "goruut".
            The goruut backend requires pygoruut to be installed.
        **kwargs: Additional arguments passed to the G2P constructor.

    Returns:
        A G2PBase instance for the specified language.

    Raises:
        ValueError: If the language is not supported and no fallback is available.
        ImportError: If backend="goruut" but pygoruut is not installed.

    Example:
        >>> g2p = get_g2p("en-us")
        >>> tokens = g2p("Hello world!")
        >>> # Chinese
        >>> g2p_zh = get_g2p("zh")
        >>> # Japanese
        >>> g2p_ja = get_g2p("ja")
        >>> # French (uses espeak fallback)
        >>> g2p_fr = get_g2p("fr")
        >>> # Using goruut backend
        >>> g2p_goruut = get_g2p("en-us", backend="goruut")
    """
    # Normalize language code
    lang = language.lower().replace("_", "-")

    # Check cache
    cache_key = f"{lang}:{use_espeak_fallback}:{use_spacy}:{backend}"
    if cache_key in _g2p_cache:
        return _g2p_cache[cache_key]

    # Create G2P instance based on language and backend
    g2p: G2PBase

    if backend == "goruut":
        # Use goruut backend for all languages
        from kokorog2p.goruut_g2p import GoruutOnlyG2P

        g2p = GoruutOnlyG2P(language=language, **kwargs)
    elif lang.startswith("en"):
        from kokorog2p.en import EnglishG2P

        g2p = EnglishG2P(
            language=language,
            use_espeak_fallback=use_espeak_fallback,
            use_spacy=use_spacy,
            **kwargs,
        )
    elif lang in ("zh", "zh-cn", "zh-tw", "cmn", "chinese"):
        from kokorog2p.zh import ChineseG2P

        g2p = ChineseG2P(language=language, **kwargs)
    elif lang in ("ja", "ja-jp", "jpn", "japanese"):
        from kokorog2p.ja import JapaneseG2P

        g2p = JapaneseG2P(language=language, **kwargs)
    elif lang in ("fr", "fr-fr", "fra", "french"):
        from kokorog2p.fr import FrenchG2P

        g2p = FrenchG2P(
            language=language,
            use_espeak_fallback=use_espeak_fallback,
            **kwargs,
        )
    elif lang in ("cs", "cs-cz", "ces", "czech"):
        from kokorog2p.cs import CzechG2P

        g2p = CzechG2P(language=language, **kwargs)
    elif lang in ("de", "de-de", "de-at", "de-ch", "deu", "german"):
        from kokorog2p.de import GermanG2P

        g2p = GermanG2P(
            language=language,
            use_espeak_fallback=use_espeak_fallback,
            **kwargs,
        )
    else:
        # Fallback to espeak-only G2P for other languages
        from kokorog2p.espeak_g2p import EspeakOnlyG2P

        g2p = EspeakOnlyG2P(language=language, **kwargs)

    _g2p_cache[cache_key] = g2p
    return g2p


def phonemize(
    text: str,
    language: str = "en-us",
    use_espeak_fallback: bool = True,
    use_spacy: bool = True,
    backend: BackendType = "espeak",
) -> str:
    """Convert text to phonemes.

    This is a convenience function that creates a G2P instance and converts
    the text to a phoneme string.

    Args:
        text: Input text to convert.
        language: Language code (e.g., 'en-us', 'en-gb').
        use_espeak_fallback: Whether to use espeak for out-of-vocabulary words
            (only applies when backend="espeak").
        use_spacy: Whether to use spaCy for tokenization and POS tagging
            (only applies to English with espeak backend).
        backend: Phonemization backend to use: "espeak" (default) or "goruut".
            The goruut backend requires pygoruut to be installed.

    Returns:
        Phoneme string.

    Example:
        >>> phonemize("Hello world!")
        'hˈɛlO wˈɜɹld!'
        >>> # Using goruut backend
        >>> phonemize("Hello world!", backend="goruut")
        'həlˈO wˈɜɹld'
    """
    g2p = get_g2p(
        language=language,
        use_espeak_fallback=use_espeak_fallback,
        use_spacy=use_spacy,
        backend=backend,
    )
    return g2p.phonemize(text)


def tokenize(
    text: str,
    language: str = "en-us",
    use_espeak_fallback: bool = True,
    use_spacy: bool = True,
    backend: BackendType = "espeak",
) -> list[GToken]:
    """Convert text to a list of tokens with phonemes.

    Args:
        text: Input text to convert.
        language: Language code (e.g., 'en-us', 'en-gb').
        use_espeak_fallback: Whether to use espeak for out-of-vocabulary words
            (only applies when backend="espeak").
        use_spacy: Whether to use spaCy for tokenization and POS tagging
            (only applies to English with espeak backend).
        backend: Phonemization backend to use: "espeak" (default) or "goruut".
            The goruut backend requires pygoruut to be installed.

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
        backend=backend,
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
    "from_goruut",
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
    # Punctuation handling
    "Punctuation",
    "normalize_punctuation",
    "filter_punctuation",
    "is_kokoro_punctuation",
    "KOKORO_PUNCTUATION",
    # Word mismatch detection
    "MismatchMode",
    "MismatchInfo",
    "MismatchStats",
    "detect_mismatches",
    "check_word_alignment",
    "count_words",
]
