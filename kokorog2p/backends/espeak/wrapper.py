"""Wrapper on espeak-ng library.

Based on phonemizer by Mathieu Bernard, licensed under GPL-3.0.
"""

import ctypes
import ctypes.util
import functools
import os
import pathlib
import sys
import tempfile
import weakref
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from kokorog2p.backends.espeak.api import EspeakAPI
from kokorog2p.backends.espeak.voice import EspeakVoice


class EspeakWrapper:
    """Wrapper on espeak shared library.

    The aim of this wrapper is not to be exhaustive but to encapsulate the
    espeak functions required for phonemization. It relies on a espeak shared
    library (*.so on Linux, *.dylib on Mac and *.dll on Windows) that must be
    installed on the system.

    Use the function `EspeakWrapper.set_library()` before instantiation to
    customize the library to use.

    Raises:
        RuntimeError: If the espeak shared library cannot be loaded.
    """

    # a static variable used to overload the default espeak library installed
    # on the system. The user can choose an alternative espeak library with
    # the method EspeakWrapper.set_library().
    _ESPEAK_LIBRARY: Optional[str] = None
    _ESPEAK_DATA_PATH: Optional[str] = None

    def __init__(self) -> None:
        # the following attributes are accessed through properties and are
        # lazily initialized
        self._version: Optional[Tuple[int, ...]] = None
        self._data_path: Optional[Path] = None
        self._voice: Optional[EspeakVoice] = None

        # load the espeak API
        self._espeak = EspeakAPI(self.library(), self.data_path)

        # lazy loading of attributes only required for the synthetize method
        self._libc_: Optional[Any] = None
        self._tempfile_: Optional[Any] = None

    @property
    def _libc(self) -> Any:
        if self._libc_ is None:
            self._libc_ = (
                ctypes.windll.msvcrt
                if sys.platform == "win32"
                else ctypes.cdll.LoadLibrary(ctypes.util.find_library("c"))
            )
        return self._libc_

    @property
    def _tempfile(self) -> Any:
        if self._tempfile_ is None:
            # this will automatically removed at exit
            # pylint: disable=consider-using-with
            self._tempfile_ = tempfile.NamedTemporaryFile()
            weakref.finalize(self._tempfile_, self._tempfile_.close)
        return self._tempfile_

    def __getstate__(self) -> Dict[str, Any]:
        """For pickling, when phonemizing on multiple jobs."""
        return {
            "version": self._version,
            "data_path": self._data_path,
            "voice": self._voice,
        }

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """For unpickling, when phonemizing on multiple jobs."""
        self.__init__()
        self._version = state["version"]
        self._data_path = state["data_path"]
        self._voice = state["voice"]
        if self._voice:
            if "mb" in self._voice.identifier:  # mbrola voice
                self.set_voice(self._voice.identifier[3:])
            else:
                self.set_voice(self._voice.language)

    @classmethod
    def set_library(cls, library: Optional[str]) -> None:
        """Sets the espeak backend to use `library`.

        If this is not set, the backend uses the default espeak shared library
        from the system installation.

        Args:
            library: The path to the espeak shared library to use as backend.
                Set to None to restore the default.
        """
        cls._ESPEAK_LIBRARY = library

    @classmethod
    def set_data_path(cls, data_path: Optional[str]) -> None:
        """Sets the path for the data to be used by the espeak backend.

        If this is not set, the backend uses the default data path from the
        system installation.

        Args:
            data_path: The path to the data to be used by the espeak backend.
                Set to None to restore the default.
        """
        cls._ESPEAK_DATA_PATH = data_path

    @classmethod
    def library(cls) -> str:
        """Returns the espeak library used as backend.

        The following precedence rule applies for library lookup:
        1. As specified by EspeakWrapper.set_library()
        2. Or as specified by the environment variable PHONEMIZER_ESPEAK_LIBRARY
        3. Or from espeakng-loader package if installed
        4. Or the default espeak library found on the system

        Raises:
            RuntimeError: If the espeak library cannot be found or if the
                environment variable PHONEMIZER_ESPEAK_LIBRARY is set to a
                non-readable file.
        """
        if cls._ESPEAK_LIBRARY:
            return cls._ESPEAK_LIBRARY

        if "PHONEMIZER_ESPEAK_LIBRARY" in os.environ:
            library = pathlib.Path(os.environ["PHONEMIZER_ESPEAK_LIBRARY"])
            if not (library.is_file() and os.access(library, os.R_OK)):
                raise RuntimeError(  # pragma: nocover
                    f"PHONEMIZER_ESPEAK_LIBRARY={library} is not a readable file"
                )
            return str(library.resolve())

        # Try espeakng-loader package
        try:
            import espeakng_loader

            loader_path = espeakng_loader.get_library_path()
            if loader_path and os.path.isfile(loader_path):
                return loader_path
        except ImportError:
            pass

        library_name = ctypes.util.find_library(
            "espeak-ng"
        ) or ctypes.util.find_library("espeak")
        if not library_name:  # pragma: nocover
            raise RuntimeError("failed to find espeak library")
        return library_name

    def _fetch_version_and_path(self) -> None:
        """Initializes version and data path from the espeak library."""
        version_bytes, data_path_bytes = self._espeak.info()

        # pylint: disable=no-member
        self._data_path = pathlib.Path(data_path_bytes.decode())
        if not self._data_path.is_dir():  # pragma: nocover
            raise RuntimeError("failed to retrieve espeak data directory")

        # espeak-1.48 appends the release date to version number, here we
        # simply ignore it
        version = version_bytes.decode().strip().split(" ")[0].replace("-dev", "")
        self._version = tuple(int(v) for v in version.split("."))

    @property
    def version(self) -> Tuple[int, ...]:
        """The espeak version as a tuple of integers (major, minor, patch)."""
        if self._version is None:
            self._fetch_version_and_path()
        return self._version  # type: ignore

    @property
    def library_path(self) -> Path:
        """The espeak library as a pathlib.Path instance."""
        return self._espeak.library_path

    @property
    def data_path(self) -> Optional[Path]:
        """Returns the espeak data path.

        The following precedence rule applies for data path lookup:
        1. As specified by EspeakWrapper.set_data_path()
        2. Or as specified by the environment variable PHONEMIZER_ESPEAK_DATA_PATH
        3. Or from espeakng-loader package if installed
        4. Or the default espeak data path found by espeak itself
        """
        if self._ESPEAK_DATA_PATH:
            data_path = pathlib.Path(self._ESPEAK_DATA_PATH)
            if not (data_path.is_dir() and os.access(self._ESPEAK_DATA_PATH, os.R_OK)):
                raise RuntimeError(
                    f"{self._ESPEAK_DATA_PATH} is not a readable directory"
                )
            self._data_path = data_path.resolve()
        elif "PHONEMIZER_ESPEAK_DATA_PATH" in os.environ:
            data_path = pathlib.Path(os.environ["PHONEMIZER_ESPEAK_DATA_PATH"])
            if not (data_path.is_dir() and os.access(data_path, os.R_OK)):
                raise RuntimeError(  # pragma: nocover
                    f"PHONEMIZER_ESPEAK_DATA_PATH={data_path} is not a readable directory"
                )
            self._data_path = data_path.resolve()
        elif self._data_path is None:
            # Try espeakng-loader package
            try:
                import espeakng_loader

                loader_data = espeakng_loader.get_data_path()
                if loader_data and os.path.isdir(loader_data):
                    self._data_path = pathlib.Path(loader_data).resolve()
            except ImportError:
                pass

        # Fetch path dynamically after initialize
        if self._data_path is None and hasattr(self, "_espeak"):
            self._fetch_version_and_path()
        return self._data_path

    @property
    def voice(self) -> Optional[EspeakVoice]:
        """The configured voice as an EspeakVoice instance.

        If `set_voice` has not been called, returns None.
        """
        return self._voice

    @functools.lru_cache(maxsize=None)
    def available_voices(self, name: Optional[str] = None) -> List[EspeakVoice]:
        """Voices available for phonemization, as a list of `EspeakVoice`."""
        voice_filter = None
        if name:
            voice_filter = EspeakVoice(language=name).to_ctypes()
        voices = self._espeak.list_voices(voice_filter)

        index = 0
        available_voices: List[EspeakVoice] = []
        # voices is an array to pointers, terminated by None
        while voices[index]:
            voice = voices[index].contents
            available_voices.append(
                EspeakVoice(
                    name=os.fsdecode(voice.name).replace("_", " "),
                    language=os.fsdecode(voice.languages)[1:],
                    identifier=os.fsdecode(voice.identifier),
                )
            )
            index += 1
        return available_voices

    def set_voice(self, voice_code: str) -> None:
        """Setup the voice to use for phonemization.

        Args:
            voice_code: Must be a valid language code that is actually
                supported by espeak.

        Raises:
            RuntimeError: If the required voice cannot be initialized.
        """
        if "mb" in voice_code:
            # this is an mbrola voice code. Select the voice by using
            # identifier in the format 'mb/{voice_code}'
            available = {
                voice.identifier[3:]: voice.identifier
                for voice in self.available_voices("mbrola")
            }
        else:
            # these are espeak voices. Select the voice using it's attached
            # language code. Consider only the first voice of a given code as
            # they are sorted by relevancy
            available: Dict[str, str] = {}
            for voice in self.available_voices():
                if voice.language not in available:
                    available[voice.language] = voice.identifier

        try:
            voice_name = available[voice_code]
        except KeyError:
            raise RuntimeError(f'invalid voice code "{voice_code}"') from None

        if self._espeak.set_voice_by_name(voice_name.encode("utf8")) != 0:
            raise RuntimeError(  # pragma: nocover
                f'failed to load voice "{voice_code}"'
            )

        voice = self._get_voice()
        if not voice:  # pragma: nocover
            raise RuntimeError(f'failed to load voice "{voice_code}"')
        self._voice = voice

    def _get_voice(self) -> Optional[EspeakVoice]:
        """Returns the current voice used for phonemization.

        If no voice has been set up, returns None.
        """
        voice = self._espeak.get_current_voice()
        if voice.name:
            return EspeakVoice.from_ctypes(voice)
        return None  # pragma: nocover

    def text_to_phonemes(self, text: str, tie: bool = False) -> str:
        """Translates a text into phonemes, must call set_voice() first.

        This method is used by the Espeak backend. Wrapper on the
        espeak_TextToPhonemes function.

        Args:
            text: The text to phonemize.
            tie: When True use a '͡' character between consecutive characters
                of a single phoneme. Else separate phoneme with '_'.
                This option requires espeak>=1.49. Default to False.

        Returns:
            The phonemes for the text encoded in IPA, with '_' as phonemes
            separator (excepted if ``tie`` is True) and ' ' as word separator.
        """
        if self.voice is None:  # pragma: nocover
            raise RuntimeError("no voice specified")

        if tie and self.version <= (1, 48, 3):
            raise RuntimeError(  # pragma: nocover
                "tie option only compatible with espeak>=1.49"
            )

        # from Python string to C void** (a pointer to a pointer to chars)
        text_ptr = ctypes.pointer(ctypes.c_char_p(text.encode("utf8")))

        # input text is encoded as UTF8
        text_mode = 1

        # output phonemes in IPA and separated by _, or with a tie character if
        # required. See comments for the function espeak_TextToPhonemes in
        # speak_lib.h of the espeak sources for details.
        if self.version <= (1, 48, 3):  # pragma: nocover
            phonemes_mode = 0x03 | 0x01 << 4
        elif tie:
            phonemes_mode = 0x02 | 0x01 << 7 | ord("͡") << 8
        else:
            phonemes_mode = ord("_") << 8 | 0x02

        result: List[str] = []
        while text_ptr.contents.value is not None:
            phonemes = self._espeak.text_to_phonemes(text_ptr, text_mode, phonemes_mode)
            if phonemes:
                result.append(phonemes.decode())
        return " ".join(result)

    def synthetize(self, text: str) -> str:
        """Translates a text into phonemes, must call set_voice() first.

        Only compatible with espeak>=1.49. This method is used by the
        EspeakMbrola backend. Wrapper on the espeak_Synthesize function.

        Args:
            text: The text to phonemize.

        Returns:
            The phonemes for the text encoded in SAMPA, with '_' as phonemes
            separator and no word separation.
        """
        if self.version < (1, 49):  # pragma: nocover
            raise RuntimeError("not compatible with espeak<=1.48")
        if self.voice is None:  # pragma: nocover
            raise RuntimeError("no voice specified")

        # init libc fopen and fclose functions
        self._libc.fopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self._libc.fopen.restype = ctypes.c_void_p
        self._libc.fclose.argtypes = [ctypes.c_void_p]
        self._libc.fclose.restype = ctypes.c_int

        # output phonemes in SAMPA and separated by _. Write the result to a
        # tempfile which is read back after phonemization (seems not possible
        # to redirect to stdout). See comments for the function
        # espeak_SetPhonemeTrace in speak_lib.h of the espeak sources for
        # details.
        self._tempfile.truncate(0)
        file_p = self._libc.fopen(
            self._tempfile.name.encode(),
            self._tempfile.mode.encode(),
        )

        self._espeak.set_phoneme_trace(0x01 << 4 | ord("_") << 8, file_p)
        status = self._espeak.synthetize(
            ctypes.c_char_p(text.encode("utf8")),
            ctypes.c_size_t(len(text) + 1),
            ctypes.c_uint(0x01),
        )
        self._libc.fclose(file_p)  # because flush does not work...

        if status != 0:  # pragma: nocover
            raise RuntimeError("failed to synthetize")

        self._tempfile.seek(0)
        phonemized = self._tempfile.read().decode().strip()
        return phonemized
