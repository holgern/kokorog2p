"""Espeak-ng backend for phonemization."""

from kokorog2p.backends.espeak.wrapper import EspeakWrapper
from kokorog2p.backends.espeak.backend import EspeakBackend
from kokorog2p.backends.espeak.voice import EspeakVoice

__all__ = ["EspeakWrapper", "EspeakBackend", "EspeakVoice"]
