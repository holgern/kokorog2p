"""Voice struct from Espeak API exposed to Python.

Based on phonemizer by Mathieu Bernard, licensed under GPL-3.0.
"""

import ctypes


class EspeakVoice:
    """A helper class to expose voice structures within C and Python."""

    def __init__(
        self,
        name: str = "",
        language: str = "",
        identifier: str = "",
    ) -> None:
        self._name = name
        self._language = language
        self._identifier = identifier

    @property
    def name(self) -> str:
        """Voice name."""
        return self._name

    @property
    def language(self) -> str:
        """Language code."""
        return self._language

    @property
    def identifier(self) -> str:
        """Path to the voice file wrt espeak data path."""
        return self._identifier

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EspeakVoice):
            return NotImplemented
        return (
            self.name == other.name
            and self.language == other.language
            and self.identifier == other.identifier
        )

    def __hash__(self) -> int:
        return hash((self.name, self.language, self.identifier))

    def __repr__(self) -> str:
        return f"EspeakVoice(name={self.name!r}, language={self.language!r})"

    class VoiceStruct(ctypes.Structure):
        """A helper class to fetch voices information from the espeak library.

        The espeak_VOICE struct is defined in speak_lib.h from the espeak code.
        Here we use only name (voice name), languages (language code) and
        identifier (voice file) information.
        """

        _fields_ = [
            ("name", ctypes.c_char_p),
            ("languages", ctypes.c_char_p),
            ("identifier", ctypes.c_char_p),
        ]

    def to_ctypes(self) -> "EspeakVoice.VoiceStruct":
        """Converts the Voice instance to an espeak ctypes structure."""
        return self.VoiceStruct(
            self.name.encode("utf8") if self.name else None,
            self.language.encode("utf8") if self.language else None,
            self.identifier.encode("utf8") if self.identifier else None,
        )

    @classmethod
    def from_ctypes(cls, struct: "EspeakVoice.VoiceStruct") -> "EspeakVoice":
        """Returns a Voice instance built from an espeak ctypes structure."""
        return cls(
            name=(struct.name or b"").decode(),
            # discard a useless char prepended by espeak
            language=(struct.languages or b"0").decode()[1:],
            identifier=(struct.identifier or b"").decode(),
        )

    @classmethod
    def from_language(cls, language: str) -> "EspeakVoice":
        """Create a Voice instance from a language code.

        Args:
            language: Language code like "en-us" or "en-gb".

        Returns:
            EspeakVoice instance with the specified language.
        """
        return cls(language=language)
