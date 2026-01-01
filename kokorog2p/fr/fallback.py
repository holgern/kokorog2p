"""Espeak fallback for French OOV words."""

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from kokorog2p.backends.espeak import EspeakBackend


class FrenchFallback:
    """Fallback G2P using espeak-ng for French."""

    def __init__(self) -> None:
        """Initialize the French espeak fallback."""
        self._backend: Optional["EspeakBackend"] = None

    @property
    def backend(self) -> Any:
        """Lazily initialize the espeak backend."""
        if self._backend is None:
            from kokorog2p.backends.espeak import EspeakBackend

            self._backend = EspeakBackend(language="fr-fr")
        return self._backend

    def __call__(self, word: str) -> tuple[Optional[str], int]:
        """Get phonemes for a word using espeak.

        Args:
            word: Word to phonemize.

        Returns:
            Tuple of (phonemes, rating). Rating is 1 for espeak fallback.
        """
        try:
            # Get phonemes from espeak (no Kokoro conversion for French)
            raw_phonemes = self.backend.word_phonemes(word, convert_to_kokoro=False)
            if not raw_phonemes:
                return (None, 0)

            # Clean up phonemes for French
            phonemes = self._normalize_french_phonemes(raw_phonemes)
            return (phonemes, 1)
        except Exception:
            return (None, 0)

    def _normalize_french_phonemes(self, phonemes: str) -> str:
        """Normalize espeak French phonemes.

        Args:
            phonemes: Raw phonemes from espeak.

        Returns:
            Normalized phoneme string.
        """
        # Espeak to French IPA normalizations
        mappings = {
            # R variants -> uvular R
            "ʀ": "ʁ",
            "r": "ʁ",
            "ɹ": "ʁ",
            # G variants
            "g": "ɡ",
        }

        result = phonemes
        for old, new in mappings.items():
            result = result.replace(old, new)

        # Remove stress marks (French doesn't have lexical stress)
        result = result.replace("ˈ", "").replace("ˌ", "")

        return result

    def phonemize(self, text: str) -> str:
        """Phonemize text using espeak.

        Args:
            text: Text to phonemize.

        Returns:
            Phoneme string.
        """
        raw = self.backend.phonemize(text, convert_to_kokoro=False)
        return self._normalize_french_phonemes(raw)
