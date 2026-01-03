"""Fallback options for Czech OOV words."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from kokorog2p.backends.espeak import EspeakBackend
    from kokorog2p.backends.goruut import GoruutBackend


class CzechEspeakFallback:
    """Fallback G2P using espeak-ng for Czech."""

    def __init__(self) -> None:
        """Initialize the Czech espeak fallback."""
        self._backend: EspeakBackend | None = None  # noqa: F821

    @property
    def backend(self) -> Any:
        """Lazily initialize the espeak backend."""
        if self._backend is None:
            from kokorog2p.backends.espeak import EspeakBackend

            self._backend = EspeakBackend(language="cs")
        return self._backend

    def __call__(self, word: str) -> tuple[str | None, int]:
        """Get phonemes for a word using espeak.

        Args:
            word: Word to phonemize.

        Returns:
            Tuple of (phonemes, rating). Rating is 1 for espeak fallback.
        """
        try:
            # Get phonemes from espeak (no Kokoro conversion for Czech)
            raw_phonemes = self.backend.word_phonemes(word, convert_to_kokoro=False)
            if not raw_phonemes:
                return (None, 0)

            # Clean up phonemes for Czech
            phonemes = self._normalize_czech_phonemes(raw_phonemes)
            return (phonemes, 1)
        except Exception:
            return (None, 0)

    def _normalize_czech_phonemes(self, phonemes: str) -> str:
        """Normalize espeak Czech phonemes.

        Args:
            phonemes: Raw phonemes from espeak.

        Returns:
            Normalized phoneme string.
        """
        # Espeak to Czech IPA normalizations
        mappings = {
            # G variants
            "g": "ɡ",
            # Remove tie characters
            "͡": "",
            "^": "",
            # Remove stress marks (Czech has fixed stress on first syllable)
            "ˈ": "",
            "ˌ": "",
        }

        result = phonemes
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
        return self._normalize_czech_phonemes(raw)


class CzechGoruutFallback:
    """Fallback G2P using goruut for Czech."""

    def __init__(self) -> None:
        """Initialize the Czech goruut fallback."""
        self._backend: GoruutBackend | None = None  # noqa: F821

    @property
    def backend(self) -> Any:
        """Lazily initialize the goruut backend."""
        if self._backend is None:
            from kokorog2p.backends.goruut import GoruutBackend

            self._backend = GoruutBackend(language="cs")
        return self._backend

    def __call__(self, word: str) -> tuple[str | None, int]:
        """Get phonemes for a word using goruut.

        Args:
            word: Word to phonemize.

        Returns:
            Tuple of (phonemes, rating). Rating is 1 for goruut fallback.
        """
        try:
            # Get phonemes from goruut (no Kokoro conversion for Czech)
            raw_phonemes = self.backend.word_phonemes(word, convert_to_kokoro=False)
            if not raw_phonemes:
                return (None, 0)

            # Clean up phonemes for Czech
            phonemes = self._normalize_czech_phonemes(raw_phonemes)
            return (phonemes, 1)
        except Exception:
            return (None, 0)

    def _normalize_czech_phonemes(self, phonemes: str) -> str:
        """Normalize goruut Czech phonemes.

        Args:
            phonemes: Raw phonemes from goruut.

        Returns:
            Normalized phoneme string.
        """
        # Goruut to Czech IPA normalizations
        mappings = {
            # G variants
            "g": "ɡ",
            # Remove stress marks (Czech has fixed stress on first syllable)
            "ˈ": "",
            "ˌ": "",
        }

        result = phonemes
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
        return self._normalize_czech_phonemes(raw)
