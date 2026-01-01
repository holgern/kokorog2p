"""High-level espeak backend for Kokoro TTS phonemization.

This module provides a convenient interface for converting text to phonemes
using espeak-ng, with automatic conversion to Kokoro's phoneme format.

Copyright 2024 kokorog2p contributors
Licensed under the Apache License, Version 2.0
"""

from kokorog2p.backends.espeak.wrapper import Phonemizer
from kokorog2p.phonemes import from_espeak


class EspeakBackend:
    """High-level espeak backend for Kokoro TTS phonemization.

    This class provides a simple interface for converting text to phonemes
    using espeak-ng. It automatically converts espeak's IPA output to
    Kokoro's phoneme format.

    Example:
        >>> backend = EspeakBackend("en-us")
        >>> backend.phonemize("hello world")
        'hˈɛlO wˈɜɹld'
    """

    def __init__(
        self,
        language: str = "en-us",
        with_stress: bool = True,
        tie: str = "^",
    ) -> None:
        """Initialize the espeak backend.

        Args:
            language: Language code (e.g., "en-us", "en-gb", "fr-fr").
            with_stress: Whether to include stress markers in output.
            tie: Tie character mode. "^" uses tie character for affricates.
        """
        self.language = language
        self.with_stress = with_stress
        self.tie = tie
        self._phonemizer: Phonemizer | None = None

    @property
    def wrapper(self) -> Phonemizer:
        """Get the underlying Phonemizer instance (lazy initialization)."""
        if self._phonemizer is None:
            self._phonemizer = Phonemizer()
            self._phonemizer.set_voice(self.language)
        return self._phonemizer

    @property
    def is_british(self) -> bool:
        """Check if using British English variant."""
        return self.language.lower() in ("en-gb", "en_gb")

    def phonemize(
        self,
        text: str,
        convert_to_kokoro: bool = True,
    ) -> str:
        """Convert text to phonemes.

        Args:
            text: Text to convert to phonemes.
            convert_to_kokoro: If True, convert espeak IPA to Kokoro format.
                              If False, return raw espeak IPA output.

        Returns:
            Phoneme string.
        """
        # Use tie character for better handling of affricates (dʒ, tʃ)
        use_tie = self.tie == "^"
        raw_phonemes = self.wrapper.phonemize(text, use_tie=use_tie)

        if convert_to_kokoro:
            return from_espeak(raw_phonemes, british=self.is_british)
        return raw_phonemes

    def phonemize_list(
        self,
        texts: list[str],
        convert_to_kokoro: bool = True,
    ) -> list[str]:
        """Convert multiple texts to phonemes.

        Args:
            texts: List of texts to convert.
            convert_to_kokoro: If True, convert to Kokoro format.

        Returns:
            List of phoneme strings.
        """
        return [self.phonemize(text, convert_to_kokoro) for text in texts]

    def word_phonemes(
        self,
        word: str,
        convert_to_kokoro: bool = True,
    ) -> str:
        """Convert a single word to phonemes.

        Args:
            word: Word to convert.
            convert_to_kokoro: If True, convert to Kokoro format.

        Returns:
            Phoneme string for the word (without separators).
        """
        result = self.phonemize(word, convert_to_kokoro)
        # Clean up: remove separators and trailing whitespace
        return result.strip().replace("_", "")

    @property
    def version(self) -> str:
        """Get espeak version as string (e.g., "1.51.1")."""
        return ".".join(str(v) for v in self.wrapper.version)

    def __repr__(self) -> str:
        return f"EspeakBackend(language={self.language!r})"
