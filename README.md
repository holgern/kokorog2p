# kokorog2p

A unified G2P (Grapheme-to-Phoneme) library for Kokoro TTS.

kokorog2p converts text to phonemes optimized for the Kokoro text-to-speech system. It
provides:

- **Dictionary-based lookup** with gold/silver tier lexicons for US and British English
- **espeak-ng integration** as a fallback for out-of-vocabulary words
- **Automatic IPA to Kokoro phoneme conversion**
- **Number and currency handling** (e.g., "$1,234.56" → "one thousand two hundred
  thirty-four dollars and fifty-six cents")
- **Stress assignment** based on linguistic rules

## Installation

```bash
# Core package (no dependencies)
pip install kokorog2p

# With English G2P support
pip install kokorog2p[en]

# With espeak-ng backend
pip install kokorog2p[espeak]

# Full installation
pip install kokorog2p[all]
```

## Quick Start

```python
from kokorog2p import phonemize

# Basic usage
phonemes = phonemize("Hello world!", language="en-us")
print(phonemes)  # həlˈoʊ wˈɜːld!

# British English
phonemes = phonemize("Hello world!", language="en-gb")
print(phonemes)
```

## Advanced Usage

```python
from kokorog2p.en import EnglishG2P

# Create a G2P instance with custom settings
g2p = EnglishG2P(
    language="en-us",
    use_espeak_fallback=True,
)

# Process text
tokens = g2p("The quick brown fox jumps over the lazy dog.")
for token in tokens:
    print(f"{token.text} → {token.phonemes}")
```

## Phoneme Inventory

kokorog2p uses Kokoro's 45-phoneme vocabulary:

### Vowels (US)

- Monophthongs: `æ ɑ ə ɚ ɛ ɪ i ʊ u ʌ ɔ`
- Diphthongs: `aɪ aʊ eɪ oʊ ɔɪ`

### Consonants

- Stops: `p b t d k ɡ`
- Fricatives: `f v θ ð s z ʃ ʒ h`
- Affricates: `tʃ dʒ`
- Nasals: `m n ŋ`
- Liquids: `l ɹ`
- Glides: `w j`

### Suprasegmentals

- Primary stress: `ˈ`
- Secondary stress: `ˌ`

## License

Apache2 License - see [LICENSE](LICENSE) for details.

## Credits

kokorog2p consolidates functionality from:

- [misaki](https://github.com/hexgrad/misaki) - G2P engine for Kokoro TTS
- [phonemizer](https://github.com/bootphon/phonemizer) - espeak-ng wrapper
