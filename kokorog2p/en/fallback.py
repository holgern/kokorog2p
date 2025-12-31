"""Espeak fallback for OOV words with IPA to Kokoro conversion."""

from typing import Optional, Tuple

from kokorog2p.phonemes import from_espeak


class EspeakFallback:
    """Fallback G2P using espeak-ng with Kokoro phoneme conversion."""

    def __init__(self, british: bool = False) -> None:
        """Initialize the espeak fallback.

        Args:
            british: Whether to use British English.
        """
        self.british = british
        self._backend: Optional["EspeakBackend"] = None  # Lazy init  # noqa: F821

    @property
    def backend(self) -> "EspeakBackend":  # noqa: F821
        """Lazily initialize the espeak backend."""
        if self._backend is None:
            from kokorog2p.backends.espeak import EspeakBackend

            language = "en-gb" if self.british else "en-us"
            self._backend = EspeakBackend(language=language)
        return self._backend

    def __call__(self, word: str) -> Tuple[Optional[str], int]:
        """Get phonemes for a word using espeak.

        Args:
            word: Word to phonemize.

        Returns:
            Tuple of (phonemes, rating). Rating is 1 for espeak fallback.
        """
        try:
            # Get phonemes from espeak
            raw_phonemes = self.backend.word_phonemes(word, convert_to_kokoro=False)
            if not raw_phonemes:
                return (None, 0)

            # Convert to Kokoro format
            phonemes = from_espeak(raw_phonemes, british=self.british)
            return (phonemes, 1)
        except Exception:
            return (None, 0)

    def phonemize(self, text: str) -> str:
        """Phonemize text using espeak.

        Args:
            text: Text to phonemize.

        Returns:
            Phoneme string in Kokoro format.
        """
        return self.backend.phonemize(text, convert_to_kokoro=True)
