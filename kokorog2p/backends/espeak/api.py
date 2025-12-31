"""Low-level bindings to the espeak API.

Based on phonemizer by Mathieu Bernard, licensed under GPL-3.0.
"""

import atexit
import ctypes
import pathlib
import shutil
import sys
import tempfile
import weakref
from ctypes import CDLL
from pathlib import Path
from typing import Optional, Tuple, Union

from kokorog2p.backends.espeak.voice import EspeakVoice

if sys.platform != "win32":
    # cause a crash on Windows
    import dlinfo


class EspeakAPI:
    """Exposes the espeak API to the EspeakWrapper.

    This class exposes only low-level bindings to the API and should not be
    used directly.
    """

    def __init__(
        self,
        library: Union[str, Path],
        data_path: Optional[Union[str, Path]],
    ) -> None:
        # set to None to avoid an AttributeError in _delete if the __init__
        # method raises, will be properly initialized below
        self._library: Optional[CDLL] = None

        data_path_bytes: Optional[bytes] = None
        if data_path is not None:
            data_path_bytes = str(data_path).encode("utf-8")

        # Because the library is not designed to be wrapped nor to be used in
        # multithreaded/multiprocess contexts (massive use of global variables)
        # we need a copy of the original library for each instance of the
        # wrapper... (see "man dlopen" on Linux/MacOS: we cannot load two times
        # the same library because a reference is then returned by dlopen). The
        # tweak is therefore to make a copy of the original library in a
        # different (temporary) directory.
        try:
            # load the original library in order to retrieve its full path
            # Forced as str as it is required on Windows.
            espeak: CDLL = ctypes.cdll.LoadLibrary(str(library))
            library_path = self._shared_library_path(espeak)
            del espeak
        except OSError as error:
            raise RuntimeError(f"failed to load espeak library: {error!s}") from None

        # will be automatically destroyed after use
        self._tempdir = tempfile.mkdtemp()

        # properly exit when the wrapper object is destroyed (see
        # https://docs.python.org/3/library/weakref.html#comparing-finalizers-with-del-methods).
        # But... weakref implementation does not work on windows so we register
        # the cleanup with atexit. This means that, on Windows, all the
        # temporary directories created by EspeakAPI instances will remain on
        # disk until the Python process exit.
        if sys.platform == "win32":  # pragma: nocover
            atexit.register(self._delete_win32)
        else:
            weakref.finalize(self, self._delete, self._library, self._tempdir)

        espeak_copy = pathlib.Path(self._tempdir) / library_path.name
        shutil.copy(library_path, espeak_copy, follow_symlinks=False)

        # finally load the library copy and initialize it. 0x02 is
        # AUDIO_OUTPUT_SYNCHRONOUS in the espeak API
        self._library = ctypes.cdll.LoadLibrary(str(espeak_copy))
        try:
            if self._library.espeak_Initialize(0x02, 0, data_path_bytes, 0) <= 0:
                raise RuntimeError(  # pragma: nocover
                    "failed to initialize espeak shared library"
                )
        except AttributeError:  # pragma: nocover
            raise RuntimeError("failed to load espeak library") from None

        # the path to the original one (the copy is considered an
        # implementation detail and is not exposed)
        self._library_path = library_path

    def _delete_win32(self) -> None:  # pragma: nocover
        # Windows does not support static methods with ctypes libraries
        # (library == None) so we use a proxy method...
        self._delete(self._library, self._tempdir)

    @staticmethod
    def _delete(library: Optional[CDLL], tempdir: str) -> None:
        try:
            # clean up the espeak library allocated memory
            if library is not None:
                library.espeak_Terminate()
        except AttributeError:  # library not loaded
            pass

        # on Windows it is required to unload the library or the .dll file
        # cannot be erased from the temporary directory
        if sys.platform == "win32" and library is not None:  # pragma: nocover
            # pylint: disable=import-outside-toplevel
            # pylint: disable=protected-access
            # pylint: disable=no-member
            import _ctypes

            _ctypes.FreeLibrary(library._handle)  # type: ignore

        # clean up the tempdir containing the copy of the library
        shutil.rmtree(tempdir)

    @property
    def library_path(self) -> Path:
        """Absolute path to the espeak library being in use."""
        return self._library_path

    @staticmethod
    def _shared_library_path(library: CDLL) -> Path:
        """Returns the absolute path to `library`.

        This function is cross-platform and works for Linux, MacOS and Windows.
        Raises a RuntimeError if the library path cannot be retrieved.
        """
        # pylint: disable=protected-access
        path = pathlib.Path(library._name).resolve()
        if path.is_file():
            return path

        try:
            # Linux or MacOS only, ImportError on Windows
            return pathlib.Path(dlinfo.DLInfo(library).path).resolve()
        except (Exception, ImportError):  # pragma: nocover
            raise RuntimeError(
                f"failed to retrieve the path to {library} library"
            ) from None

    def info(self) -> Tuple[bytes, bytes]:
        """Bindings to espeak_Info.

        Returns:
            Tuple of (version, data_path) as encoded strings.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_info = self._library.espeak_Info
        f_info.restype = ctypes.c_char_p
        data_path = ctypes.c_char_p()
        version = f_info(ctypes.byref(data_path))
        return version, data_path.value or b""

    def list_voices(
        self,
        name: Optional[EspeakVoice.VoiceStruct],
    ) -> ctypes.Array:  # type: ignore
        """Bindings to espeak_ListVoices.

        Args:
            name: If specified, a filter on voices to be listed.

        Returns:
            A pointer to EspeakVoice.Struct instances.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_list_voices = self._library.espeak_ListVoices
        f_list_voices.argtypes = [ctypes.POINTER(EspeakVoice.VoiceStruct)]
        f_list_voices.restype = ctypes.POINTER(ctypes.POINTER(EspeakVoice.VoiceStruct))
        return f_list_voices(name)

    def set_voice_by_name(self, name: bytes) -> int:
        """Bindings to espeak_SetVoiceByName.

        Args:
            name: The voice name to setup.

        Returns:
            0 on success, non-zero integer on failure.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_set_voice_by_name = self._library.espeak_SetVoiceByName
        f_set_voice_by_name.argtypes = [ctypes.c_char_p]
        return f_set_voice_by_name(name)

    def get_current_voice(self) -> EspeakVoice.VoiceStruct:
        """Bindings to espeak_GetCurrentVoice.

        Returns:
            An EspeakVoice.Struct instance or None if no voice has been setup.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_get_current_voice = self._library.espeak_GetCurrentVoice
        f_get_current_voice.restype = ctypes.POINTER(EspeakVoice.VoiceStruct)
        return f_get_current_voice().contents

    def text_to_phonemes(
        self,
        text_ptr: ctypes.POINTER,  # type: ignore
        text_mode: int,
        phonemes_mode: int,
    ) -> bytes:
        """Bindings to espeak_TextToPhonemes.

        Args:
            text_ptr: The text to be phonemized, as a pointer to a pointer of chars.
            text_mode: Bits field (see espeak sources for details).
            phonemes_mode: Bits field (see espeak sources for details).

        Returns:
            An encoded string containing the computed phonemes.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_text_to_phonemes = self._library.espeak_TextToPhonemes
        f_text_to_phonemes.restype = ctypes.c_char_p
        f_text_to_phonemes.argtypes = [
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_int,
            ctypes.c_int,
        ]
        return f_text_to_phonemes(text_ptr, text_mode, phonemes_mode)

    def set_phoneme_trace(self, mode: int, file_pointer: ctypes.c_void_p) -> None:
        """Bindings on espeak_SetPhonemeTrace.

        This method must be called before any call to synthetize().

        Args:
            mode: Bits field (see espeak sources for details).
            file_pointer: A pointer to an opened file in which to output
                the phoneme trace.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_set_phoneme_trace = self._library.espeak_SetPhonemeTrace
        f_set_phoneme_trace.argtypes = [ctypes.c_int, ctypes.c_void_p]
        f_set_phoneme_trace(mode, file_pointer)

    def synthetize(
        self,
        text_ptr: ctypes.c_char_p,
        size: ctypes.c_size_t,
        mode: ctypes.c_uint,
    ) -> int:
        """Bindings on espeak_Synth.

        The output phonemes are sent to the file specified by a call to
        set_phoneme_trace().

        Args:
            text_ptr: A pointer to chars.
            size: Number of chars in text.
            mode: Bits field (see espeak sources for details).

        Returns:
            0 on success, non-zero integer on failure.
        """
        if self._library is None:
            raise RuntimeError("espeak library not loaded")

        f_synthetize = self._library.espeak_Synth
        f_synthetize.argtypes = [
            ctypes.c_void_p,
            ctypes.c_size_t,
            ctypes.c_uint,
            ctypes.c_int,  # position_type
            ctypes.c_uint,
            ctypes.POINTER(ctypes.c_uint),
            ctypes.c_void_p,
        ]
        return f_synthetize(text_ptr, size, 0, 1, 0, mode, None, None)
