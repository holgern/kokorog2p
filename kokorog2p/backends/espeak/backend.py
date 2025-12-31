"""High-level espeak backend for phonemization.

Based on phonemizer by Mathieu Bernard, licensed under GPL-3.0.
"""

from typing import List, Optional

from kokorog2p.backends.espeak.wrapper import EspeakWrapper
from kokorog2p.phonemes import from_espeak


class EspeakBackend:
    """A high-level espeak backend for phonemization.

    This provides a simpler interface than EspeakWrapper for common
    phonemization tasks, with automatic conversion to Kokoro phonemes.
    """

    def __init__(
        self,
        language: str = "en-us",
        with_stress: bool = True,
        tie: str = "^",
    ) -> None:
        """Initialize the espeak backend.

        Args:
            language: Language code (e.g., 'en-us', 'en-gb', 'fr-fr').
            with_stress: Whether to include stress markers.
            tie: Tie character for phoneme clusters.
        """
        self.language = language
        self.with_stress = with_stress
        self.tie = tie
        self._wrapper: Optional[EspeakWrapper] = None

    @property
    def wrapper(self) -> EspeakWrapper:
        """Lazily initialize the espeak wrapper."""
        if self._wrapper is None:
            self._wrapper = EspeakWrapper()
            self._wrapper.set_voice(self.language)
        return self._wrapper

    @property
    def is_british(self) -> bool:
        """Check if using British English."""
        return self.language.lower() in ("en-gb", "en_gb")

    def phonemize(
        self,
        text: str,
        convert_to_kokoro: bool = True,
    ) -> str:
        """Convert text to phonemes.

        Args:
            text: Text to phonemize.
            convert_to_kokoro: Whether to convert espeak IPA to Kokoro format.

        Returns:
            Phoneme string.
        """
        # Use tie character for better handling of affricates
        use_tie = self.tie == "^"
        raw_phonemes = self.wrapper.text_to_phonemes(text, tie=use_tie)

        if convert_to_kokoro:
            return from_espeak(raw_phonemes, british=self.is_british)
        return raw_phonemes

    def phonemize_list(
        self,
        texts: List[str],
        convert_to_kokoro: bool = True,
    ) -> List[str]:
        """Convert a list of texts to phonemes.

        Args:
            texts: List of texts to phonemize.
            convert_to_kokoro: Whether to convert espeak IPA to Kokoro format.

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
            word: Word to phonemize.
            convert_to_kokoro: Whether to convert espeak IPA to Kokoro format.

        Returns:
            Phoneme string for the word.
        """
        result = self.phonemize(word, convert_to_kokoro)
        # Strip any trailing separators
        return result.strip().replace("_", "")

    @property
    def version(self) -> str:
        """Get the espeak version."""
        return ".".join(str(v) for v in self.wrapper.version)

    def __repr__(self) -> str:
        return f"EspeakBackend(language={self.language!r})"
