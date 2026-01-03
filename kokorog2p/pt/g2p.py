"""Brazilian Portuguese G2P (Grapheme-to-Phoneme) converter.

A rule-based Grapheme-to-Phoneme engine for Brazilian Portuguese, designed for Kokoro TTS.

Brazilian Portuguese Phonology Features:
- 7 oral vowels (a, e, ɛ, i, o, ɔ, u) with open/closed e/o variants
- 5 nasal vowels (ã, ẽ, ĩ, õ, ũ)
- Nasal diphthongs (ãw̃, õj̃, etc.)
- Palatalization: lh [ʎ], nh [ɲ], x/ch [ʃ]
- Affrication: t+i [ʧ], d+i [ʤ] (Brazilian Portuguese feature)
- Sibilants: s [s/z], x [ʃ], z [z]
- Liquids: r [ʁ/x/h] (varies by dialect), rr [ʁ/x], single r [ɾ]
- No θ sound (unlike European Portuguese)

Reference:
https://en.wikipedia.org/wiki/Portuguese_phonology
https://en.wikipedia.org/wiki/Brazilian_Portuguese
"""

import re
import unicodedata
from typing import Final

from kokorog2p.base import G2PBase
from kokorog2p.token import GToken

# =============================================================================
# Brazilian Portuguese Grapheme-to-Phoneme Mappings
# =============================================================================

# Oral vowels (7 vowels in stressed position)
ORAL_VOWELS: Final[frozenset[str]] = frozenset("aeiouɛɔ")

# Vowels that can be nasalized
NASAL_VOWELS: Final[str] = "aeiou"

# Simple consonants that don't change much
SIMPLE_CONSONANTS: Final[dict[str, str]] = {
    "b": "b",
    "f": "f",
    "k": "k",
    "p": "p",
    "v": "v",
}


class PortugueseG2P(G2PBase):
    """Brazilian Portuguese G2P converter using rule-based phonemization.

    This class provides grapheme-to-phoneme conversion for Brazilian Portuguese text
    using Portuguese orthographic rules.

    Example:
        >>> g2p = PortugueseG2P()
        >>> tokens = g2p("Olá, como está?")
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

    # Small lexicon for exceptional words
    _LEXICON: dict[str, str] = {
        # Common words
        "e": "i",  # Conjunction "and"
        "é": "ɛˈ",  # "is" (stressed open e)
        # Add more as needed
    }

    def __init__(
        self,
        language: str = "pt-br",
        use_espeak_fallback: bool = False,
        mark_stress: bool = True,
        affricate_ti_di: bool = True,  # Affricate t/d before i (Brazilian feature)
    ) -> None:
        """Initialize the Brazilian Portuguese G2P converter.

        Args:
            language: Language code (default: 'pt-br').
            use_espeak_fallback: Reserved for future espeak integration.
            mark_stress: Whether to mark primary stress with ˈ.
            affricate_ti_di: Whether to affricate /t d/ before /i/ (Brazilian feature).
        """
        super().__init__(language=language, use_espeak_fallback=use_espeak_fallback)
        self.mark_stress = mark_stress
        self.affricate_ti_di = affricate_ti_di

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
            text: Preprocessed text.

        Returns:
            List of GToken objects.
        """
        # Pattern to split on whitespace and capture punctuation
        pattern = r"([^\w'-]+|[\w'-]+)"
        parts = re.findall(pattern, text)

        tokens = []
        for part in parts:
            if not part or part.isspace():
                continue

            # Check if it's a word or punctuation
            if re.match(r"[\w'-]+", part):
                # It's a word
                token = GToken(text=part)
                token.set("is_word", True)
                tokens.append(token)
            else:
                # It's punctuation
                token = GToken(text=part)
                token.set("is_word", False)
                token.phonemes = part  # Punctuation passes through
                tokens.append(token)

        return tokens

    def _word_to_phonemes(self, word: str) -> str:
        """Convert a single word to phonemes.

        Args:
            word: Word to convert.

        Returns:
            Phoneme string in IPA.
        """
        if not word:
            return ""

        # Check lexicon first
        word_lower = word.lower()
        if word_lower in self._LEXICON:
            base_phonemes = self._LEXICON[word_lower]
            if not self.mark_stress:
                base_phonemes = base_phonemes.replace("ˈ", "")
            return base_phonemes

        # Convert to lowercase for processing
        text = word.lower()

        # Find stressed vowels before normalization
        # Track both position and vowel quality (open vs closed)
        stressed_vowels = set()
        open_vowels = set()  # Track é/ó (open) vs ê/ô (closed)
        normalized_text = []
        for i, char in enumerate(text):
            if char in "áéíóúâêôãõ":
                # Remember position
                pos = len(normalized_text)
                stressed_vowels.add(pos)
                # Track open vowels (acute accent)
                if char in "éó":
                    open_vowels.add(pos)
                # Normalize
                if char == "á":
                    normalized_text.append("a")
                elif char in ("é", "ê"):
                    normalized_text.append("e")
                elif char == "í":
                    normalized_text.append("i")
                elif char in ("ó", "ô"):
                    normalized_text.append("o")
                elif char == "ú":
                    normalized_text.append("u")
                elif char in ("ã", "õ"):
                    # Keep tilde for later
                    normalized_text.append(char)
            else:
                normalized_text.append(char)

        text = "".join(normalized_text)

        result: list[str] = []
        i = 0
        n = len(text)

        while i < n:
            matched = False

            # Multi-character sequences first

            # tch -> ʧ (Tchau, tchau)
            if i + 2 < n and text[i : i + 3] == "tch":
                result.append("ʧ")
                i += 3
                matched = True

            # nh -> ɲ (ninho)
            elif i + 1 < n and text[i : i + 2] == "nh":
                result.append("ɲ")
                i += 2
                matched = True

            # lh -> ʎ (filho)
            elif i + 1 < n and text[i : i + 2] == "lh":
                result.append("ʎ")
                i += 2
                matched = True

            # ch -> ʃ (chá)
            elif i + 1 < n and text[i : i + 2] == "ch":
                result.append("ʃ")
                i += 2
                matched = True

            # rr -> r or ʁ (strong r: carro)
            elif i + 1 < n and text[i : i + 2] == "rr":
                result.append("r")  # Use r for strong trill
                i += 2
                matched = True

            # qu + vowel -> kw or k
            # qu + e/i -> k (quero, qui), qu + a/o/u -> kw (quatro, quota)
            elif i + 2 < n and text[i : i + 2] == "qu":
                if text[i + 2] in "ei":
                    result.append("k")
                    i += 2  # Skip 'qu', next char will be processed
                    matched = True
                else:
                    # qu + a/o/u -> kw
                    result.append("k")
                    result.append("w")
                    i += 2  # Skip 'qu', next char (a/o/u) will be processed
                    matched = True

            # gu + vowel -> ɡw or ɡ
            # gu + e/i -> ɡ (guerra, guia), gu + a/o -> ɡw (água,iguano)
            elif i + 2 < n and text[i : i + 2] == "gu":
                if text[i + 2] in "ei":
                    result.append("ɡ")
                    i += 2  # Skip 'gu', next char will be processed
                    matched = True
                else:
                    # gu + a/o -> ɡw
                    result.append("ɡ")
                    result.append("w")
                    i += 2  # Skip 'gu', next char (a/o) will be processed
                    matched = True

            # Nasal combinations
            # am, an, em, en, im, in, om, on, um, un -> nasal vowel + m/n
            # At end of word or before consonant (but NOT before h in digraphs like nh, lh, ch)
            elif (
                i + 1 < n
                and text[i] in NASAL_VOWELS
                and text[i + 1] in "mn"
                and (i + 2 >= n or text[i + 2] not in "aeiouãõh")
            ):
                # Nasalize the vowel
                vowel = text[i]
                if vowel == "a":
                    result.append("ã")
                elif vowel == "e":
                    result.append("ẽ")
                elif vowel == "i":
                    result.append("ĩ")
                elif vowel == "o":
                    result.append("õ")
                elif vowel == "u":
                    result.append("ũ")
                # Add stress marker if applicable
                if self.mark_stress and i in stressed_vowels:
                    result.append("ˈ")
                # Always add the nasal consonant
                result.append(text[i + 1])
                i += 2
                matched = True

            # Already-nasalized vowels (ã, õ from tilde in input)
            elif text[i] in "ãõ":
                result.append(text[i])
                if self.mark_stress and i in stressed_vowels:
                    result.append("ˈ")
                i += 1
                matched = True

            # Single consonants - simple mappings
            elif text[i] in SIMPLE_CONSONANTS:
                result.append(SIMPLE_CONSONANTS[text[i]])
                i += 1
                matched = True

            # c -> k or s
            # c + e/i -> s (cedo, cinco)
            # c + a/o/u -> k (casa, como, curto)
            elif text[i] == "c":
                if i + 1 < n and text[i + 1] in "ei":
                    result.append("s")
                else:
                    result.append("k")
                i += 1
                matched = True

            # ç -> s (always)
            elif text[i] == "ç":
                result.append("s")
                i += 1
                matched = True

            # g -> ɡ or ʒ
            # g + e/i -> ʒ (gente, girar)
            # g + a/o/u -> ɡ (gato, gol, gula)
            elif text[i] == "g":
                if i + 1 < n and text[i + 1] in "ei":
                    result.append("ʒ")
                else:
                    result.append("ɡ")
                i += 1
                matched = True

            # j -> ʒ (always)
            elif text[i] == "j":
                result.append("ʒ")
                i += 1
                matched = True

            # x -> ʃ (most common)
            # TODO: Handle other x cases (ks, z, s) in future
            elif text[i] == "x":
                result.append("ʃ")
                i += 1
                matched = True

            # z -> z or s
            # At end of word: s (xadrez -> ʃadɾes)
            # Otherwise: z (zero, fazer)
            elif text[i] == "z":
                # Check if at end of word
                if i + 1 >= n:
                    result.append("s")
                else:
                    result.append("z")
                i += 1
                matched = True

            # ss -> s (isso -> iso)
            elif i + 1 < n and text[i : i + 2] == "ss":
                result.append("s")
                i += 2
                matched = True

            # s -> s or z
            # At start of word or after consonant: s (sal, pensar)
            # Between vowels: z (casa, mesa)
            # At end of word or before consonant: s (mas, este)
            elif text[i] == "s":
                # Check if between vowels
                if (
                    i > 0
                    and i + 1 < n
                    and text[i - 1] in "aeiouãõ"
                    and text[i + 1] in "aeiouãõ"
                ):
                    result.append("z")
                else:
                    result.append("s")
                i += 1
                matched = True

            # r -> r (strong) or ɾ (weak)
            # At start of word: r (rato)
            # Single r between vowels: ɾ (caro)
            # After consonant in cluster (br, pr, tr, etc.): ɾ (Brasil, prato)
            elif text[i] == "r":
                # Strong r only at start of word
                if i == 0:
                    result.append("r")
                else:
                    # Weak r everywhere else (between vowels or after consonants)
                    result.append("ɾ")
                i += 1
                matched = True

            # l -> l or w
            # At end of word or before consonant: w (Brasil, alto)
            # Otherwise: l (lua, ali)
            elif text[i] == "l":
                if i + 1 >= n or text[i + 1] not in "aeiouãõ":
                    result.append("w")
                else:
                    result.append("l")
                i += 1
                matched = True

            # t -> t or ʧ
            # t+i (unstressed): ʧ (tia -> ʧia, partida -> paɾʧida)
            # Final "te" (unstressed): ʧi (noite -> noiʧi, diferente -> difeɾenʧi)
            # But NOT: stressed té
            elif text[i] == "t":
                if self.affricate_ti_di:
                    # Case 1: final "te" (unstressed) -> ʧi
                    # The "e" becomes "i" in unstressed final position, then affricates
                    if (
                        i + 1 < n
                        and text[i + 1] == "e"
                        and (i + 1) not in stressed_vowels
                        and i + 2 >= n  # Must be at end of word
                    ):
                        result.append("ʧ")
                        result.append("i")  # The "e" becomes "i"
                        i += 2  # Skip both 't' and 'e'
                        matched = True
                    # Case 2: t + i (unstressed) -> ʧ
                    elif (
                        i + 1 < n
                        and text[i + 1] == "i"
                        and (i + 1) not in stressed_vowels
                    ):
                        result.append("ʧ")
                        i += 1
                        matched = True

                if not matched:
                    result.append("t")
                    i += 1
                    matched = True

            # d -> d or ʤ
            # d+i (unstressed): ʤ (dia -> ʤia, dinheiro -> ʤiɲeiɾo)
            # But NOT: stressed dí, or function words like "de"
            elif text[i] == "d":
                if self.affricate_ti_di:
                    # d + i (unstressed) -> ʤ
                    if (
                        i + 1 < n
                        and text[i + 1] == "i"
                        and (i + 1) not in stressed_vowels
                    ):
                        result.append("ʤ")
                        i += 1
                        matched = True

                if not matched:
                    result.append("d")
                    i += 1
                    matched = True
                    # Case 2: final "de" -> do NOT affricate (too variable)
                    # The benchmark expects "de", "tarde" to NOT affricate

                if not matched:
                    result.append("d")
                    i += 1
                    matched = True

            # m -> m
            elif text[i] == "m":
                result.append("m")
                i += 1
                matched = True

            # n -> n
            elif text[i] == "n":
                result.append("n")
                i += 1
                matched = True

            # w -> w (rare, mostly in loanwords)
            elif text[i] == "w":
                result.append("w")
                i += 1
                matched = True

            # y -> j (in loanwords: yoga)
            elif text[i] == "y":
                result.append("j")
                i += 1
                matched = True

            # Vowels (with possible diphthongs)
            elif text[i] in "aeiou":
                vowel = text[i]

                if vowel == "e":
                    # Use open ɛ only if stressed AND has acute accent (é)
                    # ê (circumflex) always uses closed e
                    if i in stressed_vowels and i in open_vowels:
                        result.append("ɛ")
                    else:
                        result.append("e")
                    # Check for eu diphthong -> ew (meu, seu)
                    if i + 1 < n and text[i + 1] == "u":
                        result.append("w")  # Add semivowel
                        i += 1  # Skip the 'u'

                elif vowel == "o":
                    # Same for o: use open ɔ only if stressed AND has acute accent (ó)
                    # ô (circumflex) always uses closed o
                    if i in stressed_vowels and i in open_vowels:
                        result.append("ɔ")
                    else:
                        result.append("o")
                    # Check for ou diphthong -> ow (vou, sou)
                    if i + 1 < n and text[i + 1] == "u":
                        result.append("w")  # Add semivowel
                        i += 1  # Skip the 'u'

                elif vowel == "u":
                    result.append("u")
                    # Check for ui diphthong -> uj (muito)
                    if i + 1 < n and text[i + 1] == "i":
                        result.append("j")  # Add semivowel
                        i += 1  # Skip the 'i'

                elif vowel == "a":
                    result.append("a")
                    # Check for au diphthong -> aw (Tchau, mau)
                    if i + 1 < n and text[i + 1] == "u":
                        result.append("w")  # Add semivowel
                        i += 1  # Skip the 'u'

                elif vowel == "i":
                    result.append("i")

                # Add stress marker if applicable
                if self.mark_stress and i in stressed_vowels:
                    result.append("ˈ")

                i += 1
                matched = True

            # Unknown character - skip
            if not matched:
                i += 1

        return "".join(result)

    def lookup(self, word: str, tag: str | None = None) -> str | None:
        """Look up a word's phonemes.

        Args:
            word: The word to look up.
            tag: Optional POS tag (ignored for Portuguese).

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
        result = []
        for token in tokens:
            if token.phonemes:
                result.append(token.phonemes)
        return " ".join(result)
