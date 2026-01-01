# kokorog2p

A unified multi-language G2P (Grapheme-to-Phoneme) library for Kokoro TTS.

kokorog2p converts text to phonemes optimized for the Kokoro text-to-speech system. It
provides:

- **Multi-language support**: English (US/GB), German, French, Czech, Chinese, Japanese
- **Dictionary-based lookup** with comprehensive lexicons
  - English: 100k+ entries (gold/silver tiers)
  - German: 738k+ entries from Olaph/IPA-Dict
  - French: Gold-tier dictionary
  - Czech, Chinese, Japanese: Rule-based and specialized engines
- **espeak-ng integration** as a fallback for out-of-vocabulary words
- **Automatic IPA to Kokoro phoneme conversion**
- **Number and currency handling** for supported languages
- **Stress assignment** based on linguistic rules

## Installation

```bash
# Core package (no dependencies)
pip install kokorog2p

# With English support
pip install kokorog2p[en]

# With German support
pip install kokorog2p[de]

# With French support
pip install kokorog2p[fr]

# With espeak-ng backend
pip install kokorog2p[espeak]

# Full installation (all languages and backends)
pip install kokorog2p[all]
```

## Quick Start

```python
from kokorog2p import phonemize

# English (US)
phonemes = phonemize("Hello world!", language="en-us")
print(phonemes)  # həlˈoʊ wˈɜːld!

# British English
phonemes = phonemize("Hello world!", language="en-gb")
print(phonemes)  # həlˈəʊ wˈɜːld!

# German
phonemes = phonemize("Guten Tag!", language="de")
print(phonemes)  # ɡuːtn̩ taːk!

# French
phonemes = phonemize("Bonjour!", language="fr")
print(phonemes)

# Chinese
phonemes = phonemize("你好", language="zh")
print(phonemes)
```

## Advanced Usage

```python
from kokorog2p import get_g2p

# English with custom settings
g2p_en = get_g2p("en-us", use_espeak_fallback=True)
tokens = g2p_en("The quick brown fox jumps over the lazy dog.")
for token in tokens:
    print(f"{token.text} → {token.phonemes}")

# German with lexicon and number handling
g2p_de = get_g2p("de")
tokens = g2p_de("Es kostet 42 Euro.")
for token in tokens:
    print(f"{token.text} → {token.phonemes}")

# French with fallback support
g2p_fr = get_g2p("fr", use_espeak_fallback=True)
tokens = g2p_fr("C'est magnifique!")
for token in tokens:
    print(f"{token.text} → {token.phonemes}")
```

## Supported Languages

| Language     | Code    | Dictionary Size | Number Support | Status     |
| ------------ | ------- | --------------- | -------------- | ---------- |
| English (US) | `en-us` | 100k+ entries   | ✓              | Production |
| English (GB) | `en-gb` | 100k+ entries   | ✓              | Production |
| German       | `de`    | 738k+ entries   | ✓              | Production |
| French       | `fr`    | Gold dictionary | ✓              | Production |
| Czech        | `cs`    | Rule-based      | -              | Production |
| Chinese      | `zh`    | pypinyin        | -              | Production |
| Japanese     | `ja`    | pyopenjtalk     | -              | Production |

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
