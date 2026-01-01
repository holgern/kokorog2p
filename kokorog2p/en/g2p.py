"""English G2P (Grapheme-to-Phoneme) converter."""

from kokorog2p.base import G2PBase
from kokorog2p.en.fallback import EspeakFallback
from kokorog2p.en.lexicon import Lexicon, TokenContext
from kokorog2p.token import GToken


class EnglishG2P(G2PBase):
    """English G2P converter using dictionary lookup and espeak fallback.

    This class provides grapheme-to-phoneme conversion for English text,
    using a tiered dictionary system (gold/silver) with espeak-ng as a
    fallback for out-of-vocabulary words.

    Example:
        >>> g2p = EnglishG2P(language="en-us")
        >>> tokens = g2p("Hello world!")
        >>> for token in tokens:
        ...     print(f"{token.text} -> {token.phonemes}")
    """

    def __init__(
        self,
        language: str = "en-us",
        use_espeak_fallback: bool = True,
        use_spacy: bool = True,
        unk: str = "❓",
    ) -> None:
        """Initialize the English G2P converter.

        Args:
            language: Language code ('en-us' or 'en-gb').
            use_espeak_fallback: Whether to use espeak for OOV words.
            use_spacy: Whether to use spaCy for tokenization and POS tagging.
            unk: Character to use for unknown words when fallback is disabled.
        """
        super().__init__(language=language, use_espeak_fallback=use_espeak_fallback)

        self.unk = unk
        self.use_spacy = use_spacy

        # Initialize lexicon
        self.lexicon = Lexicon(british=self.is_british)

        # Initialize fallback (lazy)
        self._fallback: EspeakFallback | None = None

        # Initialize spaCy (lazy)
        self._nlp: object | None = None

    @property
    def fallback(self) -> EspeakFallback | None:
        """Lazily initialize the espeak fallback."""
        if self.use_espeak_fallback and self._fallback is None:
            self._fallback = EspeakFallback(british=self.is_british)
        return self._fallback

    @property
    def nlp(self) -> object:
        """Lazily initialize spaCy."""
        if self._nlp is None:
            import spacy

            name = "en_core_web_sm"
            if not spacy.util.is_package(name):
                spacy.cli.download(name)  # type: ignore[attr-defined]
            self._nlp = spacy.load(name, enable=["tok2vec", "tagger"])
        return self._nlp

    def __call__(self, text: str) -> list[GToken]:
        """Convert text to a list of tokens with phonemes.

        Args:
            text: Input text to convert.

        Returns:
            List of GToken objects with phonemes assigned.
        """
        if not text.strip():
            return []

        # Tokenize
        if self.use_spacy:
            tokens = self._tokenize_spacy(text)
        else:
            tokens = self._tokenize_simple(text)

        # Process tokens in reverse order for context
        ctx = TokenContext()
        for i in range(len(tokens) - 1, -1, -1):
            token = tokens[i]

            # Skip tokens that already have phonemes (punctuation)
            if token.phonemes is not None:
                ctx = self._update_context(ctx, token.phonemes, token)
                continue

            # Try lexicon lookup
            ps, rating = self.lexicon(token.text, token.tag, None, ctx)

            if ps is not None:
                token.phonemes = ps
                token.set("rating", rating)
            elif self.fallback is not None:
                # Try espeak fallback
                ps, rating = self.fallback(token.text)
                if ps is not None:
                    token.phonemes = ps
                    token.set("rating", rating)

            # Update context
            ctx = self._update_context(ctx, token.phonemes, token)

        # Handle remaining unknown words
        for token in tokens:
            if token.phonemes is None:
                token.phonemes = self.unk

        return tokens

    def _tokenize_spacy(self, text: str) -> list[GToken]:
        """Tokenize text using spaCy.

        Args:
            text: Input text.

        Returns:
            List of GToken objects.
        """
        doc = self.nlp(text)  # type: ignore
        tokens: list[GToken] = []

        for tk in doc:
            token = GToken(
                text=tk.text,
                tag=tk.tag_,
                whitespace=tk.whitespace_,
            )

            # Handle punctuation
            if tk.tag_ in (
                ".",
                ",",
                "-LRB-",
                "-RRB-",
                "``",
                '""',
                "''",
                ":",
                "$",
                "#",
                "NFP",
            ):
                token.phonemes = self._get_punct_phonemes(tk.text, tk.tag_)
                token.set("rating", 4)

            tokens.append(token)

        # Merge contractions (e.g., "Do" + "n't" -> "Don't")
        tokens = self._merge_contractions(tokens)

        return tokens

    def _merge_contractions(self, tokens: list[GToken]) -> list[GToken]:
        """Merge contraction suffixes with their base words.

        spaCy splits contractions like "don't" into "do" + "n't",
        and double contractions like "I'd've" into "I" + "'d" + "'ve".
        This method merges them back together for better lexicon lookup.

        Args:
            tokens: List of tokens from spaCy.

        Returns:
            List of tokens with contractions merged.
        """
        # Common contraction suffixes
        contractions = {"n't", "'s", "'m", "'re", "'ve", "'d", "'ll"}

        merged: list[GToken] = []
        i = 0

        while i < len(tokens):
            token = tokens[i]

            # Collect all consecutive contraction suffixes
            merged_text = token.text
            merged_tag = token.tag
            j = i + 1

            # Keep merging while next token is a contraction suffix
            while j < len(tokens) and tokens[j].text in contractions:
                merged_text += tokens[j].text
                j += 1

            # If we merged anything, create a new token
            if j > i + 1:
                merged_token = GToken(
                    text=merged_text,
                    tag=merged_tag,  # Use the tag of the main word
                    whitespace=tokens[
                        j - 1
                    ].whitespace,  # Use whitespace from last suffix
                )
                merged.append(merged_token)
                i = j  # Skip all merged tokens
            else:
                merged.append(token)
                i += 1

        return merged

    def _tokenize_simple(self, text: str) -> list[GToken]:
        """Simple tokenization without spaCy.

        Args:
            text: Input text.

        Returns:
            List of GToken objects.
        """
        import re

        tokens: list[GToken] = []
        # Tokenize with support for contractions (e.g., I've, we're, don't)
        # Pattern matches:
        # 1. Words with apostrophes (contractions): \w+'\w+
        # 2. Regular words: \w+
        # 3. Punctuation sequences: [^\w\s]+
        # 4. Whitespace: \s+
        for match in re.finditer(r"(\w+'\w+|\w+|[^\w\s]+|\s+)", text):
            word = match.group()
            if word.isspace():
                if tokens:
                    tokens[-1].whitespace = word
                continue

            token = GToken(text=word, tag="", whitespace="")

            # Handle punctuation (but not contractions with apostrophes)
            if not word.isalnum() and "'" not in word:
                token.phonemes = word if word in ".,;:!?-—…" else ""
                token.set("rating", 4)

            tokens.append(token)

        return tokens

    @staticmethod
    def _get_punct_phonemes(text: str, tag: str) -> str:
        """Get phonemes for punctuation tokens."""
        punct_map = {
            "-LRB-": "(",
            "-RRB-": ")",
            "``": chr(8220),  # Left double quote
            '""': chr(8221),  # Right double quote
            "''": chr(8221),  # Right double quote
        }
        if tag in punct_map:
            return punct_map[tag]

        # Keep common punctuation
        puncts = frozenset(';:,.!?—…"""')
        return "".join(c for c in text if c in puncts)

    def _update_context(
        self, ctx: TokenContext, phonemes: str | None, token: GToken
    ) -> TokenContext:
        """Update context based on processed token."""
        from kokorog2p.en.lexicon import CONSONANTS, VOWELS

        non_quote_puncts = frozenset(";:,.!?—…")

        future_vowel = ctx.future_vowel
        if phonemes:
            for c in phonemes:
                if c in VOWELS:
                    future_vowel = True
                    break
                elif c in CONSONANTS:
                    future_vowel = False
                    break
                elif c in non_quote_puncts:
                    future_vowel = None
                    break

        future_to = token.text.lower() in ("to",) and token.tag in ("TO", "IN", "")

        return TokenContext(future_vowel=future_vowel, future_to=future_to)

    def lookup(self, word: str, tag: str | None = None) -> str | None:
        """Look up a word in the dictionary.

        Args:
            word: The word to look up.
            tag: Optional POS tag for disambiguation.

        Returns:
            Phoneme string or None if not found.
        """
        ps, _ = self.lexicon(word, tag, None, None)
        return ps
