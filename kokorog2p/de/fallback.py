"""Fallback options for German OOV words."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from kokorog2p.backends.espeak import EspeakBackend
    from kokorog2p.backends.goruut import GoruutBackend


class GermanEspeakFallback:
    """Fallback G2P using espeak-ng for German."""

    def __init__(self) -> None:
        """Initialize the German espeak fallback."""
        self._backend: EspeakBackend | None = None  # noqa: F821

    @property
    def backend(self) -> Any:
        """Lazily initialize the espeak backend."""
        if self._backend is None:
            from kokorog2p.backends.espeak import EspeakBackend

            self._backend = EspeakBackend(language="de-de")
        return self._backend

    def __call__(self, word: str) -> tuple[str | None, int]:
        """Get phonemes for a word using espeak.

        Args:
            word: Word to phonemize.

        Returns:
            Tuple of (phonemes, rating). Rating is 1 for espeak fallback.
        """
        try:
            # Get phonemes from espeak (no Kokoro conversion for German)
            raw_phonemes = self.backend.word_phonemes(word, convert_to_kokoro=False)
            if not raw_phonemes:
                return (None, 0)

            # Clean up phonemes for German
            phonemes = self._normalize_german_phonemes(raw_phonemes)
            return (phonemes, 1)
        except Exception:
            return (None, 0)

    def _normalize_german_phonemes(self, phonemes: str) -> str:
        """Normalize espeak German phonemes.

        Args:
            phonemes: Raw phonemes from espeak.

        Returns:
            Normalized phoneme string.
        """
        # Import the normalization function from g2p module
        from kokorog2p.de.g2p import normalize_to_kokoro

        # Apply normalization (handles affricates, combining diacritics, etc.)
        result = normalize_to_kokoro(phonemes)

        # Additional espeak-specific normalizations
        mappings = {
            # G variants
            "g": "ɡ",
            # Remove tie characters
            "͡": "",
            "^": "",
        }

        for old, new in mappings.items():
            result = result.replace(old, new)

        return result

    def phonemize(self, text: str) -> str:
        """Phonemize text using espeak.

        Args:
            text: Text to phonemize.

        Returns:
            Phoneme string.
        """
        raw = self.backend.phonemize(text, convert_to_kokoro=False)
        return self._normalize_german_phonemes(raw)


class GermanGoruutFallback:
    """Fallback G2P using goruut for German."""

    def __init__(self) -> None:
        """Initialize the German goruut fallback."""
        self._backend: GoruutBackend | None = None  # noqa: F821

    @property
    def backend(self) -> Any:
        """Lazily initialize the goruut backend."""
        if self._backend is None:
            from kokorog2p.backends.goruut import GoruutBackend

            self._backend = GoruutBackend(language="de-de")
        return self._backend

    def __call__(self, word: str) -> tuple[str | None, int]:
        """Get phonemes for a word using goruut.

        Args:
            word: Word to phonemize.

        Returns:
            Tuple of (phonemes, rating). Rating is 1 for goruut fallback.
        """
        try:
            # Get phonemes from goruut (no Kokoro conversion for German)
            raw_phonemes = self.backend.word_phonemes(word, convert_to_kokoro=False)
            if not raw_phonemes:
                return (None, 0)

            # Clean up phonemes for German
            phonemes = self._normalize_german_phonemes(raw_phonemes)
            return (phonemes, 1)
        except Exception:
            return (None, 0)

    def _normalize_german_phonemes(self, phonemes: str) -> str:
        """Normalize goruut German phonemes.

        Args:
            phonemes: Raw phonemes from goruut.

        Returns:
            Normalized phoneme string.
        """
        # Import the normalization function from g2p module
        from kokorog2p.de.g2p import normalize_to_kokoro

        # Apply normalization (handles affricates, combining diacritics, etc.)
        result = normalize_to_kokoro(phonemes)

        # Additional goruut-specific normalizations
        mappings = {
            # G variants
            "g": "ɡ",
        }

        for old, new in mappings.items():
            result = result.replace(old, new)

        return result

    def phonemize(self, text: str) -> str:
        """Phonemize text using goruut.

        Args:
            text: Text to phonemize.

        Returns:
            Phoneme string.
        """
        raw = self.backend.phonemize(text, convert_to_kokoro=False)
        return self._normalize_german_phonemes(raw)
