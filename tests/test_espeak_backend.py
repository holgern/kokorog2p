"""Tests for the espeak-ng backend.

Copyright 2024 kokorog2p contributors
Licensed under the Apache License, Version 2.0
"""

import os
import pickle
import sys

import pytest


@pytest.mark.espeak
class TestEspeakBackend:
    """Tests for the EspeakBackend class."""

    def test_creation(self, espeak_backend):
        """Test backend creation with default parameters."""
        assert espeak_backend.language == "en-us"
        assert espeak_backend.with_stress is True
        assert espeak_backend.tie == "^"

    def test_is_british(self, espeak_backend, espeak_backend_gb):
        """Test British English detection."""
        assert espeak_backend.is_british is False
        assert espeak_backend_gb.is_british is True

    def test_phonemize_word(self, espeak_backend):
        """Test converting a single word to phonemes."""
        result = espeak_backend.phonemize("hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_phonemize_sentence(self, espeak_backend):
        """Test converting a sentence to phonemes."""
        result = espeak_backend.phonemize("Hello world")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_phonemize_with_kokoro(self, espeak_backend):
        """Test phonemization with Kokoro format conversion."""
        result = espeak_backend.phonemize("say", convert_to_kokoro=True)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_phonemize_raw_ipa(self, espeak_backend):
        """Test phonemization without Kokoro conversion."""
        result = espeak_backend.phonemize("say", convert_to_kokoro=False)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_phonemize_list(self, espeak_backend):
        """Test batch phonemization."""
        texts = ["hello", "world", "test"]
        results = espeak_backend.phonemize_list(texts)
        assert isinstance(results, list)
        assert len(results) == 3
        assert all(isinstance(r, str) for r in results)

    def test_word_phonemes(self, espeak_backend):
        """Test single word phonemization without separators."""
        result = espeak_backend.word_phonemes("hello")
        assert isinstance(result, str)
        assert "_" not in result

    def test_version_string(self, espeak_backend):
        """Test version string format."""
        version = espeak_backend.version
        assert isinstance(version, str)
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
class TestPhonemizer:
    """Tests for the Phonemizer (wrapper) class."""

    def test_version(self, has_espeak):
        """Test version is available."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        assert p.version is not None
        assert isinstance(p.version, tuple)
        assert len(p.version) >= 2

    def test_phonemize(self, has_espeak):
        """Test basic phonemization."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        p.set_voice("en-us")

        result = p.phonemize("hello")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_set_voice(self, has_espeak):
        """Test voice selection."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        p.set_voice("en-us")
        p.set_voice("en-gb")


@pytest.mark.espeak
class TestVoice:
    """Tests for the Voice class."""

    def test_from_language(self, has_espeak):
        """Test creating voice from language code."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Voice

        voice = Voice.from_language("en-us")
        assert voice.language == "en-us"

        voice_gb = Voice.from_language("en-gb")
        assert voice_gb.language == "en-gb"


@pytest.mark.espeak
class TestVoiceListing:
    """Tests for listing available voices."""

    def test_list_voices(self, has_espeak):
        """Test listing all voices."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        voices = p.list_voices()

        assert voices
        assert len(voices) > 0
        languages = {v.language for v in voices}
        assert any(lang.startswith("en") for lang in languages if lang)

    def test_list_voices_filtered(self, has_espeak):
        """Test listing voices with filter."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        mbrola = p.list_voices("mbrola")
        espeak = p.list_voices()

        if mbrola:
            espeak_ids = {v.identifier for v in espeak}
            mbrola_ids = {v.identifier for v in mbrola}
            assert not espeak_ids.intersection(mbrola_ids)


@pytest.mark.espeak
class TestVoiceSelection:
    """Tests for voice selection."""

    def test_set_and_get_voice(self, has_espeak):
        """Test setting and retrieving voice."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        assert p.voice is None

        p.set_voice("en-us")
        assert p.voice is not None
        assert p.voice.language == "en-us"

        p.set_voice("fr-fr")
        assert p.voice.language == "fr-fr"

    def test_invalid_voice(self, has_espeak):
        """Test error on invalid voice."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()

        with pytest.raises(RuntimeError):
            p.set_voice("")

        with pytest.raises(RuntimeError):
            p.set_voice("nonexistent-xyz")


@pytest.mark.espeak
class TestPickling:
    """Tests for pickle support."""

    def test_pickle_phonemizer(self, has_espeak):
        """Test pickling and unpickling."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p1 = Phonemizer()
        p1.set_voice("en-us")

        data = pickle.dumps(p1)
        p2 = pickle.loads(data)

        assert p1.version == p2.version
        assert p1.library_path == p2.library_path
        assert p1.voice.language == p2.voice.language

    def test_pickle_preserves_results(self, has_espeak):
        """Test pickled instance produces same output."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p1 = Phonemizer()
        p1.set_voice("en-us")
        result1 = p1.phonemize("hello")

        data = pickle.dumps(p1)
        p2 = pickle.loads(data)
        result2 = p2.phonemize("hello")

        assert result1 == result2


@pytest.mark.espeak
class TestMultipleInstances:
    """Tests for multiple phonemizer instances."""

    def test_shared_properties(self, has_espeak):
        """Test instances share some properties."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p1 = Phonemizer()
        p2 = Phonemizer()

        assert p1.version == p2.version
        assert p1.library_path == p2.library_path

    def test_independent_voices(self, has_espeak):
        """Test instances have independent voice selection."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p1 = Phonemizer()
        p2 = Phonemizer()

        p1.set_voice("fr-fr")
        p2.set_voice("en-us")

        assert p1.voice.language == "fr-fr"
        assert p2.voice.language == "en-us"


@pytest.mark.espeak
class TestLibraryInfo:
    """Tests for library information."""

    def test_version_tuple(self, has_espeak):
        """Test version format."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        assert p.version >= (1, 48)
        assert all(isinstance(v, int) for v in p.version)

    def test_library_path(self, has_espeak):
        """Test library path."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        assert "espeak" in str(p.library_path)
        assert os.path.isabs(p.library_path)

    def test_data_path(self, has_espeak):
        """Test data path."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        assert p.data_path is not None


@pytest.mark.espeak
class TestTieCharacter:
    """Tests for tie character handling."""

    def test_with_separator(self, has_espeak):
        """Test output with separator."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        p.set_voice("en-us")

        result = p.phonemize("Jackie", use_tie=False)
        assert "_" in result

    def test_with_tie(self, has_espeak):
        """Test output with tie character."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        p.set_voice("en-us")

        if p.version >= (1, 49):
            result = p.phonemize("Jackie", use_tie=True)
            assert "͡" in result or "_" not in result


@pytest.mark.espeak
@pytest.mark.skipif(sys.platform == "win32", reason="Different on Windows")
class TestTempDirectory:
    """Tests for temporary directory handling."""

    def test_temp_dir_exists(self, has_espeak):
        """Test temp directory exists during use."""
        if not has_espeak:
            pytest.skip("espeak not available")

        import pathlib

        from kokorog2p.backends.espeak import Phonemizer

        p = Phonemizer()
        p.set_voice("en-us")

        temp_dir = pathlib.Path(p._api.temp_dir)
        assert temp_dir.exists()
        files = list(temp_dir.iterdir())
        assert len(files) >= 1


# Backwards compatibility tests
@pytest.mark.espeak
class TestBackwardsCompatibility:
    """Tests for backwards compatible aliases."""

    def test_espeak_wrapper_alias(self, has_espeak):
        """Test EspeakWrapper alias works."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakWrapper

        w = EspeakWrapper()
        assert w.version is not None

    def test_espeak_voice_alias(self, has_espeak):
        """Test EspeakVoice alias works."""
        if not has_espeak:
            pytest.skip("espeak not available")

        from kokorog2p.backends.espeak import EspeakVoice

        v = EspeakVoice.from_language("en-us")
        assert v.language == "en-us"
