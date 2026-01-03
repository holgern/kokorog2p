"""Italian G2P (Grapheme-to-Phoneme) converter.

A rule-based Grapheme-to-Phoneme engine for Italian, designed for Kokoro TTS models.

Italian Phonology Features:
- 5 pure vowels (a, e, i, o, u) - always pronounced clearly
- No vowel reduction (unlike English)
- Predictable stress (usually penultimate syllable)
- Gemination (double consonants) is phonemically distinctive
- Palatals: gn [ɲ], gli [ʎ]
- Affricates: z [ʦ/ʣ], c/ci [ʧ], g/gi [ʤ]
- No diphthongs in standard Italian (consecutive vowels are separate syllables)

Reference:
https://en.wikipedia.org/wiki/Italian_phonology
"""

import re
import unicodedata
from typing import Final

from kokorog2p.base import G2PBase
from kokorog2p.token import GToken

# =============================================================================
# Italian Grapheme-to-Phoneme Mappings
# =============================================================================

# Context-sensitive rules for Italian G2P
# Italian orthography is largely phonemic with predictable rules

# Vowels are straightforward
VOWELS: Final[frozenset[str]] = frozenset("aeiouàèéìòóù")

# Consonants that don't change
SIMPLE_CONSONANTS: Final[dict[str, str]] = {
    "b": "b",
    "d": "d",
    "f": "f",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "r": "r",
    "t": "t",
    "v": "v",
}


class ItalianG2P(G2PBase):
    """Italian G2P converter using rule-based phonemization.

    This class provides grapheme-to-phoneme conversion for Italian text
    using Italian orthographic rules. Italian has fairly regular spelling,
    making rule-based conversion quite accurate.

    Example:
        >>> g2p = ItalianG2P()
        >>> tokens = g2p("Ciao, come stai?")
        >>> for token in tokens:
        ...     print(f"{token.text} -> {token.phonemes}")
    """

    # Punctuation normalization map
    _PUNCT_MAP = {
        chr(171): '"',  # «
        chr(187): '"',  # »
        chr(8216): "'",  # '
        chr(8217): "'",  # '
        chr(8220): '"',  # "
        chr(8221): '"',  # "
        chr(8212): "-",  # —
        chr(8211): "-",  # –
        chr(8230): "...",  # …
    }

    def __init__(
        self,
        language: str = "it-it",
        use_espeak_fallback: bool = False,
        mark_stress: bool = True,
        mark_gemination: bool = True,
    ) -> None:
        """Initialize the Italian G2P converter.

        Args:
            language: Language code (default: 'it-it').
            use_espeak_fallback: Reserved for future espeak integration.
            mark_stress: Whether to mark primary stress with ˈ.
            mark_gemination: Whether to mark double consonants with ː.
        """
        super().__init__(language=language, use_espeak_fallback=use_espeak_fallback)
        self.mark_stress = mark_stress
        self.mark_gemination = mark_gemination

    def __call__(self, text: str) -> list[GToken]:
        """Convert text to a list of tokens with phonemes.

        Args:
            text: Input text to convert.

        Returns:
            List of GToken objects with phonemes assigned.
        """
        if not text.strip():
            return []

        # Preprocess
        text = self._preprocess(text)

        # Tokenize
        tokens = self._tokenize(text)

        # Process tokens
        for token in tokens:
            # Skip tokens that already have phonemes (punctuation)
            if token.phonemes is not None:
                continue

            # Convert word to phonemes
            if token.is_word:
                phonemes = self._word_to_phonemes(token.text)
                if phonemes:
                    token.phonemes = phonemes
                    token.set("rating", 3)  # Rule-based rating

        # Handle remaining unknown words
        for token in tokens:
            if token.phonemes is None and token.is_word:
                token.phonemes = "?"

        return tokens

    def _preprocess(self, text: str) -> str:
        """Preprocess text before G2P conversion.

        Args:
            text: Raw input text.

        Returns:
            Preprocessed text.
        """
        # Normalize Unicode
        text = unicodedata.normalize("NFC", text)

        # Normalize punctuation
        for old, new in self._PUNCT_MAP.items():
            text = text.replace(old, new)

        # Remove non-breaking spaces
        text = text.replace("\u00a0", " ")
        text = text.replace("\u202f", " ")

        # Collapse multiple spaces
        text = re.sub(r" +", " ", text)

        return text.strip()

    def _tokenize(self, text: str) -> list[GToken]:
        """Tokenize text into words and punctuation.

        Args:
            text: Input text.

        Returns:
            List of GToken objects.
        """
        tokens: list[GToken] = []

        # Simple word/punct split
        for match in re.finditer(r"(\w+|[^\w\s]+|\s+)", text, re.UNICODE):
            word = match.group()
            if word.isspace():
                if tokens:
                    tokens[-1].whitespace = word
                continue

            token = GToken(text=word, tag="", whitespace="")

            # Handle punctuation
            if not any(c.isalnum() for c in word):
                token.phonemes = self._get_punct_phonemes(word)
                token.set("rating", 4)

            tokens.append(token)

        return tokens

    @staticmethod
    def _get_punct_phonemes(text: str) -> str:
        """Get phonemes for punctuation tokens."""
        # Keep common punctuation
        puncts = frozenset(";:,.!?-\"'()[]")
        return "".join(c for c in text if c in puncts)

    def _word_to_phonemes(self, word: str) -> str:
        """Convert a single word to phonemes using Italian rules.

        Args:
            word: Word to convert.

        Returns:
            Phoneme string in IPA.
        """
        if not word:
            return ""

        # Convert to lowercase for processing
        text = word.lower()

        # Find stressed vowels before normalization
        stressed_vowels = set()
        normalized_text = []
        for i, char in enumerate(text):
            if char in "àèéìòóù":
                # Remember the position of the normalized vowel
                stressed_vowels.add(len(normalized_text))
                # Normalize the accented vowel
                if char == "à":
                    normalized_text.append("a")
                elif char in "èé":
                    normalized_text.append("e")
                elif char == "ì":
                    normalized_text.append("i")
                elif char in "òó":
                    normalized_text.append("o")
                elif char == "ù":
                    normalized_text.append("u")
            else:
                normalized_text.append(char)

        text = "".join(normalized_text)

        result: list[str] = []
        i = 0
        n = len(text)

        while i < n:
            matched = False
            chars_consumed = 0

            # Try multi-character sequences first
            # Check for double consonants first (cch, ggh, cqu, etc.)

            # cqu -> kːw (acqua)
            if i + 2 < n and text[i : i + 3] == "cqu":
                result.append("k")
                result.append("ː")
                result.append("w")
                i += 3
                matched = True

            # cch -> kːk  (occhi)
            elif i + 2 < n and text[i : i + 3] == "cch":
                result.append("k")
                result.append("ː")
                i += 2  # Skip to the 'h'
                matched = True

            # ggh -> ɡːɡ (agghiacciare)
            elif i + 2 < n and text[i : i + 3] == "ggh":
                result.append("ɡ")
                result.append("ː")
                i += 2  # Skip to the 'h'
                matched = True

            # gn -> ɲ (gnocchi), check for doubling after
            elif i + 1 < n and text[i : i + 2] == "gn":
                result.append("ɲ")
                i += 2
                # Check if followed by another consonant for gemination
                if self.mark_gemination and i < n and text[i] == "n":
                    result.append("ː")
                    i += 1
                matched = True

            # gli -> ʎ (famiglia), but only before vowel or word-final
            elif i + 2 < n and text[i : i + 3] == "gli":
                if i + 3 >= n or text[i + 3] in VOWELS:
                    result.append("ʎ")
                    i += 3
                    matched = True
                else:
                    # gl before non-vowel -> g + l
                    result.append("ɡ")
                    i += 1
                    matched = True

            # gl before i -> ʎ
            elif (
                i + 1 < n
                and text[i : i + 2] == "gl"
                and i + 2 < n
                and text[i + 2] == "i"
            ):
                result.append("ʎ")
                i += 2
                matched = True

            # sc before e/i -> ʃ (pesce)
            elif i + 1 < n and text[i : i + 2] == "sc":
                if i + 2 < n and text[i + 2] in "ei":
                    result.append("ʃ")
                    i += 2
                    matched = True
                else:
                    # sc before other -> sk
                    result.append("s")
                    result.append("k")
                    i += 2
                    matched = True

            # ch -> k (che, chi)
            elif i + 1 < n and text[i : i + 2] == "ch":
                result.append("k")
                i += 2
                matched = True

            # gh -> ɡ (ghetto, ghiro)
            elif i + 1 < n and text[i : i + 2] == "gh":
                result.append("ɡ")
                i += 2
                matched = True

            # cci/cce -> ʧː (cappuccino)
            elif i + 2 < n and text[i : i + 2] == "cc" and text[i + 2] in "ei":
                if self.mark_gemination:
                    result.append("ʧ")
                    result.append("ː")
                    i += 2
                else:
                    result.append("ʧ")
                    i += 1
                matched = True

            # ci/ce -> ʧ (ciao, cento)
            elif text[i] == "c":
                if i + 1 < n and text[i + 1] in "ei":
                    result.append("ʧ")
                    i += 1
                    matched = True
                elif i + 1 < n and text[i + 1] == "c":
                    # Double c before a/o/u -> k:
                    result.append("k")
                    result.append("ː")
                    i += 2
                    matched = True
                else:
                    # c before a/o/u -> k
                    result.append("k")
                    i += 1
                    matched = True

            # ggi/gge -> ʤː (oggi)
            elif i + 2 < n and text[i : i + 2] == "gg" and text[i + 2] in "ei":
                if self.mark_gemination:
                    result.append("ʤ")
                    result.append("ː")
                    i += 2
                else:
                    result.append("ʤ")
                    i += 1
                matched = True

            # gi/ge -> ʤ (giorno, gente)
            elif text[i] == "g":
                if i + 1 < n and text[i + 1] in "ei":
                    result.append("ʤ")
                    i += 1
                    matched = True
                elif i + 1 < n and text[i + 1] == "g":
                    # Double g before a/o/u -> ɡ:
                    result.append("ɡ")
                    result.append("ː")
                    i += 2
                    matched = True
                else:
                    # g before a/o/u -> ɡ
                    result.append("ɡ")
                    i += 1
                    matched = True

            # z -> ʦ or ʣ (context-dependent, default to voiceless)
            elif text[i] == "z":
                # Check for double z
                if self.mark_gemination and i + 1 < n and text[i + 1] == "z":
                    result.append("ʦ")
                    result.append("ː")
                    i += 2
                    matched = True
                else:
                    # Simplified: use ʦ (voiceless) by default
                    result.append("ʦ")
                    i += 1
                    matched = True

            # qu -> kw
            elif i + 1 < n and text[i : i + 2] == "qu":
                result.append("k")
                result.append("w")
                i += 2
                matched = True

            # h is silent
            elif text[i] == "h":
                i += 1
                matched = True

            # s -> s (can be [s] or [z], default to s)
            elif text[i] == "s":
                # Check for gemination (double s)
                if self.mark_gemination and i + 1 < n and text[i + 1] == "s":
                    result.append("s")
                    result.append("ː")  # length marker
                    i += 2
                    matched = True
                else:
                    result.append("s")
                    i += 1
                    matched = True

            # Simple consonants
            elif text[i] in SIMPLE_CONSONANTS:
                consonant = SIMPLE_CONSONANTS[text[i]]
                # Check for gemination
                if self.mark_gemination and i + 1 < n and text[i + 1] == text[i]:
                    result.append(consonant)
                    result.append("ː")  # length marker
                    i += 2
                    matched = True
                else:
                    result.append(consonant)
                    i += 1
                    matched = True

            # Vowels
            elif text[i] in "aeiou":
                result.append(text[i])
                # Add stress mark AFTER the vowel if this vowel is stressed
                if self.mark_stress and i in stressed_vowels:
                    result.append("ˈ")
                i += 1
                matched = True

            # j -> j (semivowel)
            elif text[i] == "j":
                result.append("j")
                i += 1
                matched = True

            # w -> w (in loan words)
            elif text[i] == "w":
                result.append("w")
                i += 1
                matched = True

            # x -> ks (in loan words)
            elif text[i] == "x":
                result.append("k")
                result.append("s")
                i += 1
                matched = True

            # y -> i (in loan words)
            elif text[i] == "y":
                result.append("i")
                i += 1
                matched = True

            # Unknown character
            if not matched:
                # Skip unknown characters
                i += 1

        return "".join(result)

    def lookup(self, word: str, tag: str | None = None) -> str | None:
        """Look up a word's phonemes.

        Args:
            word: The word to look up.
            tag: Optional POS tag (ignored for Italian).

        Returns:
            Phoneme string or None.
        """
        return self._word_to_phonemes(word)

    def phonemize(self, text: str) -> str:
        """Convert text to phonemes.

        Args:
            text: Input text to convert.

        Returns:
            Phoneme string.
        """
        tokens = self(text)
        return " ".join(t.phonemes or "" for t in tokens if t.phonemes)

    def __repr__(self) -> str:
        return f"ItalianG2P(language={self.language!r})"
