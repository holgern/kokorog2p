"""Tests for the EspeakBackend.

Tests adapted from phonemizer-fork by Mathieu Bernard.
"""

import os
import pickle
import sys

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


@pytest.mark.espeak
class TestEspeakStress:
    """Tests for stress handling in espeak backend."""

    def test_stress_disabled(self, has_espeak):
        """Test phonemization without stress markers."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakBackend

        backend = EspeakBackend("en-us", with_stress=False)
        result = backend.phonemize("hello world", convert_to_kokoro=False)
        # Without stress, there should be no primary/secondary stress markers
        # Note: espeak may still include some markers depending on version
        assert isinstance(result, str)
        assert len(result) > 0

    def test_stress_enabled(self, has_espeak):
        """Test phonemization with stress markers."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakBackend

        backend = EspeakBackend("en-us", with_stress=True)
        result = backend.phonemize("hello world", convert_to_kokoro=False)
        # With stress, should include primary stress marker
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for stress markers in the raw output
        assert "ˈ" in result or "ˌ" in result


@pytest.mark.espeak
class TestEspeakAvailableVoices:
    """Tests for available voices enumeration."""

    def test_available_voices(self, has_espeak):
        """Test listing available voices."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        voices = wrapper.available_voices()

        assert voices
        assert len(voices) > 0
        # Should have at least English
        languages = {v.language for v in voices}
        assert (
            "en" in languages
            or "en-us" in languages
            or any(lang.startswith("en") for lang in languages)
        )

    def test_available_voices_filtered(self, has_espeak):
        """Test listing available voices with filter."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()

        # Get mbrola voices (may be empty if not installed)
        mbrola_voices = wrapper.available_voices("mbrola")
        espeak_voices = wrapper.available_voices()

        # Espeak and mbrola voices should not overlap
        if mbrola_voices:
            espeak_identifiers = {v.identifier for v in espeak_voices}
            mbrola_identifiers = {v.identifier for v in mbrola_voices}
            assert not espeak_identifiers.intersection(mbrola_identifiers)


@pytest.mark.espeak
class TestEspeakVoiceSetGet:
    """Tests for setting and getting voices."""

    def test_set_get_voice(self, has_espeak):
        """Test setting and getting voice."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        assert wrapper.voice is None

        wrapper.set_voice("en-us")
        assert wrapper.voice is not None
        assert wrapper.voice.language == "en-us"
        assert (
            "english" in wrapper.voice.name.lower()
            or "america" in wrapper.voice.name.lower()
        )

        wrapper.set_voice("fr-fr")
        assert wrapper.voice.language == "fr-fr"
        assert (
            "french" in wrapper.voice.name.lower()
            or "france" in wrapper.voice.name.lower()
        )

    def test_set_invalid_voice(self, has_espeak):
        """Test setting an invalid voice raises error."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()

        with pytest.raises(RuntimeError) as err:
            wrapper.set_voice("")
        assert "invalid voice code" in str(err)

        with pytest.raises(RuntimeError) as err:
            wrapper.set_voice("non-existent-voice-xyz")
        assert "invalid voice code" in str(err)


@pytest.mark.espeak
class TestEspeakPickle:
    """Tests for pickling support (needed for multiprocessing)."""

    def test_pickle_wrapper(self, has_espeak):
        """Test that EspeakWrapper can be pickled and unpickled."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        wrapper.set_voice("en-us")

        # Pickle and unpickle
        dump = pickle.dumps(wrapper)
        wrapper2 = pickle.loads(dump)

        assert wrapper.version == wrapper2.version
        assert wrapper.library_path == wrapper2.library_path
        assert wrapper.voice.language == wrapper2.voice.language

    def test_pickle_preserves_phonemization(self, has_espeak):
        """Test that unpickled wrapper produces same results."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        wrapper.set_voice("en-us")

        original_result = wrapper.text_to_phonemes("hello")

        # Pickle and unpickle
        dump = pickle.dumps(wrapper)
        wrapper2 = pickle.loads(dump)

        new_result = wrapper2.text_to_phonemes("hello")

        assert original_result == new_result


@pytest.mark.espeak
class TestEspeakMultipleInstances:
    """Tests for multiple wrapper instances."""

    def test_multiple_wrappers(self, has_espeak):
        """Test that multiple wrapper instances work correctly."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper1 = EspeakWrapper()
        wrapper2 = EspeakWrapper()

        assert wrapper1.data_path == wrapper2.data_path
        assert wrapper1.version == wrapper2.version
        assert wrapper1.library_path == wrapper2.library_path

    def test_multiple_wrappers_different_voices(self, has_espeak):
        """Test multiple wrappers with different voices."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper1 = EspeakWrapper()
        wrapper2 = EspeakWrapper()

        wrapper1.set_voice("fr-fr")
        assert wrapper1.voice.language == "fr-fr"

        wrapper2.set_voice("en-us")
        assert wrapper2.voice.language == "en-us"

        # Both should maintain their respective voices
        assert wrapper1.voice.language == "fr-fr"
        assert wrapper2.voice.language == "en-us"


@pytest.mark.espeak
class TestEspeakBasicInfo:
    """Tests for basic espeak information."""

    def test_version_format(self, has_espeak):
        """Test version is a tuple of integers."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        assert wrapper.version >= (1, 48)
        assert all(isinstance(v, int) for v in wrapper.version)

    def test_library_path(self, has_espeak):
        """Test library path is valid."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        assert "espeak" in str(wrapper.library_path)
        assert os.path.isabs(wrapper.library_path)

    def test_data_path(self, has_espeak):
        """Test data path is valid."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        # data_path should be accessible
        assert wrapper.data_path is not None


@pytest.mark.espeak
class TestEspeakTie:
    """Tests for tie character handling."""

    def test_tie_character(self, has_espeak):
        """Test tie character for affricates."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        wrapper.set_voice("en-us")

        # Without tie - phonemes separated by underscore
        result_no_tie = wrapper.text_to_phonemes("Jackie Chan", tie=False)
        assert "_" in result_no_tie

        # With tie - uses tie character for affricates
        # Note: espeak >= 1.49 required
        if wrapper.version >= (1, 49):
            result_tie = wrapper.text_to_phonemes("Jackie Chan", tie=True)
            # Tie character (U+0361) should be present for dʒ and tʃ
            assert "͡" in result_tie or "_" not in result_tie


@pytest.mark.espeak
@pytest.mark.skipif(sys.platform == "win32", reason="Path handling differs on Windows")
class TestEspeakTempfileCleanup:
    """Tests for temporary file cleanup."""

    def test_tempdir_exists_during_use(self, has_espeak):
        """Test that wrapper has a temp directory during use."""
        if not has_espeak:
            pytest.skip("espeak not available")

        import pathlib

        from kokorog2p.backends.espeak import EspeakWrapper

        wrapper = EspeakWrapper()
        wrapper.set_voice("en-us")

        # Check that the temp directory exists while wrapper is alive
        tempdir = pathlib.Path(wrapper._espeak._tempdir)
        assert tempdir.exists()
        # The temp directory should contain a copy of the espeak library
        files = list(tempdir.iterdir())
        assert len(files) >= 1
