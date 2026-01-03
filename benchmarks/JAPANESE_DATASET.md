# Japanese Synthetic Benchmark Dataset

## Overview

The Japanese benchmark script is located at:

- **benchmarks/benchmark_ja_comparison.py**

This script tests all Japanese G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_ja_comparison.py

# Test specific configuration
python benchmarks/benchmark_ja_comparison.py --config "pyopenjtalk"

# Verbose output
python benchmarks/benchmark_ja_comparison.py --verbose

# Export results
python benchmarks/benchmark_ja_comparison.py --output results.json
```

## Benchmark Results (371 sentences)

| Configuration        | Accuracy | Speed        | Recommendation |
| -------------------- | -------- | ------------ | -------------- |
| pyopenjtalk + espeak | 100.0%   | 6,286 sent/s | ✅ **Best**    |
| pyopenjtalk          | 100.0%   | 1,716 sent/s | Good           |
| cutlet + espeak      | N/A      | -            | Requires MeCab |
| cutlet               | N/A      | -            | Requires MeCab |

**Recommendation**: Use **pyopenjtalk + espeak** configuration for Japanese for best
speed and accuracy.

## Dataset Composition

The dataset consists of:

- **31 hand-crafted sentences** covering:
  - Greetings (こんにちは, おはよう, etc.)
  - Common words and phrases
  - Questions
  - Numbers
  - Verbs and adjectives
  - Conversational phrases
- **340 natural speech samples** from CHILDES ja-JP corpus (adult speech only)

**Total**: 371 sentences with 1,432 words

## Phoneme Coverage

The dataset achieves **100% coverage** of all 29 Japanese phoneme characters:

```
a b d e f g h i j k m n o p r s t u w z ɕ ɴ ʔ ʥ ʦ ʨ ː ᶄ ᶉ
```

### Special Japanese Phonemes

- **ɕ** - palatal fricative (し shi)
- **ɴ** - moraic n (ん)
- **ʔ** - glottal stop
- **ʥ** - voiced affricate (じ ji)
- **ʦ** - voiceless affricate (つ tsu)
- **ʨ** - palatal affricate (ち chi)
- **ː** - long vowel marker (ー)
- **ᶄ ᶉ** - special pronunciation markers

## Character-Based Phoneme System

**Important**: Unlike European languages where phonemes are space-separated by word,
Japanese phonemes are **character-based**. Each character in the phoneme string
represents a single phoneme.

**Example**:

- Text: `こんにちは`
- Phonemes: `koɴniʨiwa` (9 characters = 9 phonemes)
  - k-o-ɴ-n-i-ʨ-i-w-a

## Category Breakdown

| Category        | Sentences | Description                              |
| --------------- | --------- | ---------------------------------------- |
| childes_natural | 340       | Natural adult speech from CHILDES corpus |
| greetings       | 5         | Common Japanese greetings                |
| common_words    | 4         | Frequently used vocabulary               |
| conversation    | 7         | Conversational phrases                   |
| verbs           | 5         | Common verb forms                        |
| adjectives      | 4         | Basic adjectives                         |
| questions       | 3         | Question patterns                        |
| numbers         | 3         | Number pronunciation                     |

## G2P Backend Information

### pyopenjtalk (Recommended)

The default and recommended backend for Japanese G2P. It provides:

- Accurate kana/kanji → phoneme conversion
- MeCab-based morphological analysis
- Built-in pronunciation dictionary
- No additional dependencies (MeCab included)

### cutlet (Alternative)

An alternative backend that requires:

- External MeCab installation
- Additional system setup
- May have different accuracy characteristics

**Note**: The benchmark currently shows 0% accuracy for cutlet because MeCab is not
installed in the test environment.

## Validation Results

Run the validator to check dataset integrity:

```bash
python benchmarks/validate_synthetic_data.py benchmarks/data/ja_synthetic.json
```

**Results**:

- ✅ All 371 sentences validated
- ✅ 100% phoneme coverage (29/29 unique characters)
- ✅ No invalid phonemes
- ✅ All required fields present

## CHILDES Corpus Source

The natural speech examples were extracted from:

- **Corpus**: CHILDES IPA corpus
- **Language**: ja-JP (Japanese)
- **Source size**: 246 MB (~850K sentences)
- **Selection criteria**:
  - Adult speech only (not child babbling)
  - 3-10 tokens per sentence
  - Valid Japanese characters
  - No special markers or errors
  - Deduplicated against hand-crafted sentences

**Extraction rate**: ~0.06% (340 sentences from 300K+ candidates)

- High filtering rate due to strict quality criteria
- Focus on natural, grammatical adult speech
- Removal of incomplete utterances and non-standard forms

## Usage Examples

### Basic Benchmarking

```python
from kokorog2p.ja import JapaneseG2P

# Create G2P with recommended configuration
g2p = JapaneseG2P(
    use_espeak_fallback=True,
    version="pyopenjtalk"
)

# Phonemize Japanese text
tokens = g2p("こんにちは")
for token in tokens:
    print(f"{token.text} → {token.phonemes}")
# Output: こんにちは → koɴniʨiwa
```

### Testing Different Configurations

```bash
# Test pyopenjtalk only (no fallback)
python benchmarks/benchmark_ja_comparison.py --config "pyopenjtalk"

# Test with espeak fallback (faster)
python benchmarks/benchmark_ja_comparison.py --config "pyopenjtalk + espeak"

# See detailed errors (if any)
python benchmarks/benchmark_ja_comparison.py --verbose
```

## Known Limitations

1. **Katakana romanization**: Some katakana words (especially English loanwords) may
   have non-standard phoneme outputs
2. **Kanji readings**: Multiple readings (kun/on) are context-dependent; the G2P uses
   MeCab for disambiguation
3. **Pitch accent**: Japanese pitch accent is not represented in the phoneme output
4. **Dialectal variation**: Dataset represents standard Tokyo Japanese pronunciation

## Future Improvements

Potential areas for enhancement:

- [ ] Add more katakana loanword examples
- [ ] Include compound word edge cases
- [ ] Add regional dialect variations
- [ ] Test with alternative MeCab dictionaries
- [ ] Expand conversation category with longer dialogues

## References

- CHILDES IPA Corpus: https://github.com/ErikMorton/ipa-childes
- pyopenjtalk: https://github.com/r9y9/pyopenjtalk
- cutlet: https://github.com/polm/cutlet
- Japanese IPA: https://en.wikipedia.org/wiki/Help:IPA/Japanese

## Contributing

To improve the Japanese dataset:

1. Add more diverse sentence patterns
2. Test with specialized vocabulary (technical, literary, etc.)
3. Validate pronunciation with native speakers
4. Report any phoneme mismatches or errors

## License

The Japanese synthetic dataset is released under the same license as kokorog2p.
