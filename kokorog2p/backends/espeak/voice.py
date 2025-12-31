"""Voice data structure for espeak-ng.

This module provides a Python representation of the espeak_VOICE structure
from the espeak-ng C API (speak_lib.h).

Copyright 2024 kokorog2p contributors
Licensed under the Apache License, Version 2.0
"""

import ctypes
from dataclasses import dataclass


@dataclass
class Voice:
    """Represents an espeak-ng voice.

    This corresponds to the espeak_VOICE struct in speak_lib.h:
    - name: a given name for this voice (UTF8 string)
    - languages: list of priority + language pairs
    - identifier: the filename for this voice within espeak-ng-data/voices
    - gender: 0=none, 1=male, 2=female
    - age: 0=not specified, or age in years
    """

    name: str = ""
    language: str = ""
    identifier: str = ""
    gender: int = 0
    age: int = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Voice):
            return NotImplemented
        return (
            self.name == other.name
            and self.language == other.language
            and self.identifier == other.identifier
        )

    def __hash__(self) -> int:
        return hash((self.name, self.language, self.identifier))

    @classmethod
    def from_language(cls, language: str) -> "Voice":
        """Create a Voice with just the language set.

        Args:
            language: Language code like 'en-us' or 'en-gb'.

        Returns:
            Voice instance with language set.
        """
        return cls(language=language)


class VoiceStruct(ctypes.Structure):
    """ctypes Structure matching espeak_VOICE from speak_lib.h.

    From the espeak-ng header:
        typedef struct {
            const char *name;
            const char *languages;
            const char *identifier;
            unsigned char gender;
            unsigned char age;
            unsigned char variant;
            unsigned char xx1;
            int score;
            void *spare;
        } espeak_VOICE;
    """

    _fields_ = [
        ("name", ctypes.c_char_p),
        ("languages", ctypes.c_char_p),
        ("identifier", ctypes.c_char_p),
        ("gender", ctypes.c_ubyte),
        ("age", ctypes.c_ubyte),
        ("variant", ctypes.c_ubyte),
        ("xx1", ctypes.c_ubyte),
        ("score", ctypes.c_int),
        ("spare", ctypes.c_void_p),
    ]


def voice_to_struct(voice: Voice) -> VoiceStruct:
    """Convert a Voice dataclass to a ctypes VoiceStruct.

    Args:
        voice: Voice dataclass instance.

    Returns:
        VoiceStruct for use with espeak C API.
    """
    struct = VoiceStruct()
    struct.name = voice.name.encode("utf-8") if voice.name else None
    struct.languages = voice.language.encode("utf-8") if voice.language else None
    struct.identifier = voice.identifier.encode("utf-8") if voice.identifier else None
    struct.gender = voice.gender
    struct.age = voice.age
    struct.variant = 0
    struct.xx1 = 0
    struct.score = 0
    struct.spare = None
    return struct


def struct_to_voice(struct: VoiceStruct) -> Voice:
    """Convert a ctypes VoiceStruct to a Voice dataclass.

    Args:
        struct: VoiceStruct from espeak C API.

    Returns:
        Voice dataclass instance.
    """
    name = struct.name.decode("utf-8") if struct.name else ""
    # Languages field has a priority byte prefix, skip it
    languages = struct.languages
    if languages:
        # The languages field starts with a priority byte, then the language string
        lang_bytes = languages[1:] if len(languages) > 1 else b""
        language = lang_bytes.decode("utf-8").split("\x00")[0] if lang_bytes else ""
    else:
        language = ""
    identifier = struct.identifier.decode("utf-8") if struct.identifier else ""

    return Voice(
        name=name.replace("_", " "),
        language=language,
        identifier=identifier,
        gender=struct.gender,
        age=struct.age,
    )


# Backwards compatibility aliases
EspeakVoice = Voice
