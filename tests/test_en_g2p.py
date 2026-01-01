"""Tests for the English G2P module."""

import pytest

from kokorog2p.token import GToken


class TestEnglishG2PNoFallback:
    """Tests for EnglishG2P without espeak fallback."""

    def test_creation(self, english_g2p_no_espeak):
        """Test G2P creation."""
        assert english_g2p_no_espeak.language == "en-us"
        assert english_g2p_no_espeak.use_espeak_fallback is False
        assert english_g2p_no_espeak.use_spacy is False

    def test_is_british(self, english_g2p_no_espeak):
        """Test is_british property."""
        assert english_g2p_no_espeak.is_british is False

    def test_call_returns_tokens(self, english_g2p_no_espeak):
        """Test calling G2P returns list of tokens."""
        tokens = english_g2p_no_espeak("hello world")
        assert isinstance(tokens, list)
        assert all(isinstance(t, GToken) for t in tokens)

    def test_known_word_phonemization(self, english_g2p_no_espeak):
        """Test phonemizing known words."""
        tokens = english_g2p_no_espeak("hello")
        assert len(tokens) >= 1
        # "hello" should be in the dictionary
        assert tokens[0].phonemes is not None
        assert tokens[0].text == "hello"

    def test_unknown_word_without_fallback(self, english_g2p_no_espeak):
        """Test unknown word without fallback uses unk marker."""
        tokens = english_g2p_no_espeak("xyzqwerty")
        assert len(tokens) >= 1
        # Should get the unk marker
        assert tokens[0].phonemes == english_g2p_no_espeak.unk

    def test_empty_input(self, english_g2p_no_espeak):
        """Test empty input returns empty list."""
        tokens = english_g2p_no_espeak("")
        assert tokens == []

        tokens2 = english_g2p_no_espeak("   ")
        assert tokens2 == []

    def test_phonemize_method(self, english_g2p_no_espeak):
        """Test phonemize method returns string."""
        result = english_g2p_no_espeak.phonemize("hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_lookup_method(self, english_g2p_no_espeak):
        """Test lookup method."""
        ps = english_g2p_no_espeak.lookup("hello")
        assert ps is not None
        assert isinstance(ps, str)

        # Unknown word
        ps2 = english_g2p_no_espeak.lookup("xyzqwerty")
        assert ps2 is None

    def test_repr(self, english_g2p_no_espeak):
        """Test string representation."""
        result = repr(english_g2p_no_espeak)
        assert "EnglishG2P" in result
        assert "en-us" in result


@pytest.mark.espeak
class TestEnglishG2PWithEspeak:
    """Tests for EnglishG2P with espeak fallback."""

    def test_unknown_word_with_fallback(self, english_g2p_with_espeak):
        """Test unknown word uses espeak fallback."""
        tokens = english_g2p_with_espeak("xyzqwerty")
        assert len(tokens) >= 1
        # With fallback, should get actual phonemes (not unk marker)
        # Unless espeak also fails
        phonemes = tokens[0].phonemes
        assert phonemes is not None

    def test_mixed_known_unknown(self, english_g2p_with_espeak):
        """Test mixing known and unknown words."""
        tokens = english_g2p_with_espeak("hello xyzqwerty world")
        assert len(tokens) >= 3
        # All should have phonemes with fallback
        for token in tokens:
            if token.is_word:
                assert token.phonemes is not None


@pytest.mark.spacy
class TestEnglishG2PWithSpacy:
    """Tests for EnglishG2P with spaCy."""

    def test_creation_with_spacy(self, english_g2p_with_spacy):
        """Test G2P creation with spaCy."""
        assert english_g2p_with_spacy.use_spacy is True

    def test_pos_tagging(self, english_g2p_with_spacy):
        """Test that POS tags are assigned."""
        tokens = english_g2p_with_spacy("The cat sat on the mat.")
        # With spaCy, tokens should have POS tags
        word_tokens = [t for t in tokens if t.is_word]
        assert any(t.tag != "" for t in word_tokens)

    def test_punctuation_handling(self, english_g2p_with_spacy):
        """Test punctuation is handled correctly."""
        tokens = english_g2p_with_spacy("Hello, world!")
        # Should have punctuation tokens
        assert any(t.text == "," for t in tokens)
        assert any(t.text == "!" for t in tokens)

    def test_contraction_phonemes_with_spacy(self, english_g2p_with_spacy):
        """Test contractions are phonemized correctly with spaCy.

        SpaCy splits contractions (e.g., I've -> I + 've), so we need to
        ensure the suffix parts ('ve, 're, etc.) have correct phonemes.
        """
        test_cases = [
            ("I've learned", "ˈIv lˈɜɹnd"),
            ("We've worked", "wˌiv wˈɜɹkt"),
            ("You're welcome", "jˌuɹ wˈɛlkəm"),
            ("They're here", "ðˌAɹ hˈɪɹ"),
        ]
        for text, expected in test_cases:
            result = english_g2p_with_spacy.phonemize(text)
            assert (
                result == expected
            ), f"'{text}': expected '{expected}', got '{result}'"


@pytest.mark.espeak
@pytest.mark.spacy
class TestEnglishG2PFull:
    """Tests for fully-featured EnglishG2P."""

    def test_full_sentence(self, english_g2p_full):
        """Test full sentence processing."""
        tokens = english_g2p_full("The quick brown fox jumps over the lazy dog.")
        assert len(tokens) > 0
        # All word tokens should have phonemes
        for token in tokens:
            if token.is_word:
                assert token.phonemes is not None
                assert token.phonemes != ""

    def test_context_dependent_pronunciation(self, english_g2p_full):
        """Test context-dependent pronunciations."""
        # "the" before vowel vs consonant
        tokens_vowel = english_g2p_full("the apple")
        tokens_consonant = english_g2p_full("the book")

        the_vowel = [t for t in tokens_vowel if t.text.lower() == "the"][0]
        the_consonant = [t for t in tokens_consonant if t.text.lower() == "the"][0]

        # They might be different (ði vs ðə)
        # This tests the context mechanism is working
        assert the_vowel.phonemes is not None
        assert the_consonant.phonemes is not None


class TestEnglishG2PTokenization:
    """Tests for tokenization in EnglishG2P."""

    def test_simple_tokenization(self, english_g2p_no_espeak):
        """Test simple tokenization without spaCy."""
        tokens = english_g2p_no_espeak("hello world")
        texts = [t.text for t in tokens]
        assert "hello" in texts
        assert "world" in texts

    def test_punctuation_tokenization(self, english_g2p_no_espeak):
        """Test punctuation tokenization."""
        tokens = english_g2p_no_espeak("Hello, world!")
        texts = [t.text for t in tokens]
        assert "Hello" in texts
        assert "," in texts
        assert "world" in texts
        assert "!" in texts

    def test_whitespace_handling(self, english_g2p_no_espeak):
        """Test whitespace is captured in tokens."""
        tokens = english_g2p_no_espeak("hello world")
        # First token should have trailing whitespace
        assert tokens[0].whitespace == " " or any(t.whitespace for t in tokens)

    def test_contraction_tokenization(self, english_g2p_no_espeak):
        """Test contractions are tokenized as single tokens."""
        # Test various contractions
        contractions = ["I've", "we've", "you've", "they've", "don't", "won't", "can't"]
        for contraction in contractions:
            tokens = english_g2p_no_espeak(contraction)
            # Should be a single token (not split by apostrophe)
            word_tokens = [t for t in tokens if t.text == contraction]
            assert len(word_tokens) == 1, f"'{contraction}' should be a single token"

    def test_contraction_phonemes(self, english_g2p_no_espeak):
        """Test contractions have correct phonemes."""
        # Test that contractions get proper phonemes from the lexicon
        # Note: Capitalized forms may have different stress patterns
        test_cases = [
            ("I've", "ˌIv"),
            ("we've", "wiv"),  # lowercase has no secondary stress
            ("We've", "wˌiv"),  # capitalized has secondary stress
            ("you've", "juv"),
            ("they've", "ðAv"),
            ("don't", "dˈOnt"),
            ("won't", "wˈOnt"),
            ("can't", "kˈænt"),
            ("he's", "hiz"),
            ("she's", "ʃiz"),
            ("it's", "ɪts"),
        ]
        for word, expected_phonemes in test_cases:
            tokens = english_g2p_no_espeak(word)
            assert len(tokens) >= 1, f"Should have token for '{word}'"
            actual = tokens[0].phonemes
            assert (
                actual == expected_phonemes
            ), f"'{word}': expected '{expected_phonemes}', got '{actual}'"

    def test_contraction_in_sentence(self, english_g2p_no_espeak):
        """Test contractions work correctly within sentences."""
        # Test "I've learned"
        tokens = english_g2p_no_espeak("I've learned")
        texts = [t.text for t in tokens]
        assert "I've" in texts, "I've should be a single token"

        # Check phonemes
        ive_token = [t for t in tokens if t.text == "I've"][0]
        assert ive_token.phonemes == "ˌIv", f"I've phonemes: {ive_token.phonemes}"

        # Test "We've worked"
        tokens = english_g2p_no_espeak("We've worked")
        texts = [t.text for t in tokens]
        assert "We've" in texts, "We've should be a single token"

        weve_token = [t for t in tokens if t.text == "We've"][0]
        assert weve_token.phonemes == "wˌiv", f"We've phonemes: {weve_token.phonemes}"


class TestMainAPI:
    """Tests for the main kokorog2p API."""

    def test_import_main_api(self):
        """Test importing main API."""
        from kokorog2p import get_g2p, phonemize, tokenize

        assert callable(phonemize)
        assert callable(tokenize)
        assert callable(get_g2p)

    def test_get_g2p_caching(self):
        """Test G2P instances are cached."""
        from kokorog2p import clear_cache, get_g2p

        clear_cache()
        g2p1 = get_g2p("en-us", use_espeak_fallback=False, use_spacy=False)
        g2p2 = get_g2p("en-us", use_espeak_fallback=False, use_spacy=False)
        assert g2p1 is g2p2

        # Different options should create different instances
        get_g2p("en-us", use_espeak_fallback=True, use_spacy=False)
        # Note: Can't test this without espeak, but the cache key is different

    def test_get_g2p_unsupported_language(self):
        """Test unsupported language falls back to EspeakOnlyG2P."""
        from kokorog2p import clear_cache, get_g2p
        from kokorog2p.espeak_g2p import EspeakOnlyG2P

        clear_cache()
        g2p = get_g2p("de-de")
        assert isinstance(g2p, EspeakOnlyG2P)

    def test_clear_cache(self):
        """Test cache clearing."""
        from kokorog2p import clear_cache, get_g2p

        g2p1 = get_g2p("en-us", use_espeak_fallback=False, use_spacy=False)
        clear_cache()
        g2p2 = get_g2p("en-us", use_espeak_fallback=False, use_spacy=False)
        # After clearing, should be a new instance
        assert g2p1 is not g2p2

    def test_phonemize_function(self):
        """Test phonemize convenience function."""
        from kokorog2p import phonemize

        result = phonemize("hello", use_espeak_fallback=False, use_spacy=False)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_tokenize_function(self):
        """Test tokenize convenience function."""
        from kokorog2p import GToken, tokenize

        tokens = tokenize("hello world", use_espeak_fallback=False, use_spacy=False)
        assert isinstance(tokens, list)
        assert all(isinstance(t, GToken) for t in tokens)

    def test_version_available(self):
        """Test version is available."""
        from kokorog2p import __version__

        assert isinstance(__version__, str)
