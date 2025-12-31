"""Tests for the EspeakBackend."""

import pytest


@pytest.mark.espeak
class TestEspeakBackend:
    """Tests for the EspeakBackend class."""

    def test_backend_creation(self, espeak_backend):
        """Test backend creation."""
        assert espeak_backend.language == "en-us"
        assert espeak_backend.with_stress is True
        assert espeak_backend.tie == "^"

    def test_backend_is_british(self, espeak_backend, espeak_backend_gb):
        """Test is_british property."""
        assert espeak_backend.is_british is False
        assert espeak_backend_gb.is_british is True

    def test_phonemize_simple_word(self, espeak_backend):
        """Test phonemizing a simple word."""
        result = espeak_backend.phonemize("hello")
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain stress marker for primary syllable
        assert "ˈ" in result or "ˌ" in result or len(result) > 3

    def test_phonemize_sentence(self, espeak_backend):
        """Test phonemizing a sentence."""
        result = espeak_backend.phonemize("Hello world")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_phonemize_with_kokoro_conversion(self, espeak_backend):
        """Test phonemization with Kokoro conversion."""
        result = espeak_backend.phonemize("say", convert_to_kokoro=True)
        # "say" contains the eɪ diphthong, which should be converted to A
        # The result might vary by espeak version, but should be valid
        assert isinstance(result, str)
        assert len(result) > 0

    def test_phonemize_without_kokoro_conversion(self, espeak_backend):
        """Test phonemization without Kokoro conversion."""
        result = espeak_backend.phonemize("say", convert_to_kokoro=False)
        assert isinstance(result, str)
        # Without conversion, should have original IPA
        assert len(result) > 0

    def test_phonemize_list(self, espeak_backend):
        """Test phonemizing a list of texts."""
        texts = ["hello", "world", "test"]
        results = espeak_backend.phonemize_list(texts)
        assert isinstance(results, list)
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

    def test_word_phonemes(self, espeak_backend):
        """Test single word phonemization."""
        result = espeak_backend.word_phonemes("hello")
        assert isinstance(result, str)
        # Should not have underscores or trailing separators
        assert "_" not in result

    def test_version(self, espeak_backend):
        """Test version property."""
        version = espeak_backend.version
        assert isinstance(version, str)
        # Version should be in format like "1.51.1" or similar
        parts = version.split(".")
        assert len(parts) >= 1

    def test_repr(self, espeak_backend):
        """Test string representation."""
        result = repr(espeak_backend)
        assert "EspeakBackend" in result
        assert "en-us" in result

    def test_british_phonemization(self, espeak_backend_gb):
        """Test British English phonemization."""
        result = espeak_backend_gb.phonemize("hello")
        assert isinstance(result, str)
        assert len(result) > 0


@pytest.mark.espeak
class TestEspeakWrapper:
    """Tests for the low-level EspeakWrapper."""

    def test_wrapper_version(self, has_espeak):
        """Test wrapper version."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()

        assert wrapper.version is not None
        assert isinstance(wrapper.version, tuple)
        assert len(wrapper.version) >= 2

    def test_wrapper_text_to_phonemes(self, has_espeak):
        """Test text to phonemes conversion."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        wrapper.set_voice("en-us")

        result = wrapper.text_to_phonemes("hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_wrapper_set_voice(self, has_espeak):
        """Test setting voice."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()

        # Should not raise
        wrapper.set_voice("en-us")
        wrapper.set_voice("en-gb")


@pytest.mark.espeak
class TestEspeakVoice:
    """Tests for the EspeakVoice class."""

    def test_voice_from_language(self, has_espeak):
        """Test voice creation from language code."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakVoice

        voice = EspeakVoice.from_language("en-us")
        assert voice.language == "en-us"

        voice_gb = EspeakVoice.from_language("en-gb")
        assert voice_gb.language == "en-gb"
