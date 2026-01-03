# Korean Synthetic Benchmark Dataset

## Overview

The Korean benchmark script is located at:

- **benchmarks/benchmark_ko_comparison.py**

This script tests Korean G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_ko_comparison.py

# Test specific configuration
python benchmarks/benchmark_ko_comparison.py --config "Korean G2P"

# Verbose output
python benchmarks/benchmark_ko_comparison.py --verbose

# Export results
python benchmarks/benchmark_ko_comparison.py --output results.json
```

## Benchmark Results (100 sentences, 301 words)

| Configuration       | Accuracy | Speed     | Recommendation        |
| ------------------- | -------- | --------- | --------------------- |
| Korean G2P + Espeak | 100.0%   | 37 sent/s | ✅ **Best** (fastest) |
| Korean G2P          | 100.0%   | 22 sent/s | Good default          |

**Recommendation**: Use **Korean G2P + Espeak** configuration for best speed while
maintaining 100% accuracy. The espeak fallback improves performance without sacrificing
accuracy.

## Dataset Composition

The dataset consists of:

- **40 hand-crafted sentences** covering:
  - Greetings (안녕하세요, 감사합니다, etc.)
  - Common words (사랑, 행복, 가족, etc.)
  - Numbers (하나 둘 셋, 일 이 삼, etc.)
  - Food vocabulary (김치, 밥, 물, etc.)
  - Phoneme coverage (특수 발음 테스트)
  - Questions and conversation
- **60 natural speech samples** from CHILDES ko-KR corpus (adult speech only)

**Total**: 100 sentences with 301 words

## Phoneme Coverage

The dataset achieves **100% coverage** of all 23 Korean phoneme characters:

```
a e h i j k l m n o p s t u w ø ɛ ɯ ɰ ʌ ʨ ʰ ͈
```

### Character-Based Phoneme System

**Important**: Like Japanese, Korean phonemes are **character-based**. Each character in
the phoneme string represents a single phoneme (not space-separated by word).

**Example**:

- Text: `안녕하세요`
- Phonemes: `annjʌhasejo` (11 characters = 11 phonemes)
  - a-n-n-j-ʌ-h-a-s-e-j-o

### Korean Vowels

**Basic vowels:**

- **a** - 아 (PALM vowel)
- **e** - 에 (mid front vowel)
- **i** - 이 (FLEECE vowel)
- **o** - 오 (mid back rounded vowel)
- **u** - 우 (GOOSE vowel)

**Special vowels:**

- **ø** - 외 (front rounded vowel, like German ö)
- **ɛ** - 애 (open-mid front vowel)
- **ɯ** - 으 (close back unrounded vowel, unique to Korean)
- **ɰ** - 의 onset (velar approximant)
- **ʌ** - 어 (mid-central vowel, like English "uh")

### Korean Consonants

**Plain consonants:**

- **k** - ㄱ (velar stop)
- **t** - ㄷ (alveolar stop)
- **p** - ㅂ (bilabial stop)
- **s** - ㅅ (alveolar fricative)
- **ʨ** - ㅈ (alveolo-palatal affricate)

**Sonorants:**

- **n** - ㄴ (alveolar nasal)
- **m** - ㅁ (bilabial nasal)
- **l** - ㄹ (lateral approximant)
- **h** - ㅎ (glottal fricative)

**Approximants:**

- **j** - ㅣ onset, y-sound (palatal approximant)
- **w** - ㅜ onset, w-sound (labio-velar approximant)

### Phonological Features

**Aspiration (ʰ):**

- **kʰ** - ㅋ (aspirated k)
- **tʰ** - ㅌ (aspirated t)
- **pʰ** - ㅍ (aspirated p)
- **ʨʰ** - ㅊ (aspirated affricate)

**Tenseness (͈):**

- **k͈** - ㄲ (tensed k, double consonant)
- **t͈** - ㄸ (tensed t)
- **p͈** - ㅃ (tensed p)
- **s͈** - ㅆ (tensed s)
- **ʨ͈** - ㅉ (tensed affricate)

### Note on Simplified Phonology

**Without MeCab**: The current implementation uses g2pK without MeCab morphological
analysis, which produces simplified phonology:

- **No ŋ (velar nasal)** - Final ㅇ is simplified
- **No ̚ (unreleased stops)** - Final consonants are not marked as unreleased
- Still achieves **100% accuracy** on benchmark

**With MeCab** (optional): Installing `mecab-python3` enables:

- More accurate morphological analysis
- Proper handling of ŋ (받침 ㅇ)
- Unreleased stop notation (̚)
- Better context-dependent pronunciation

## Category Breakdown

| Category         | Sentences | Description                              |
| ---------------- | --------- | ---------------------------------------- |
| childes_natural  | 60        | Natural adult speech from CHILDES corpus |
| common_words     | 8         | Frequently used vocabulary               |
| greetings        | 5         | Common Korean greetings                  |
| conversation     | 5         | Conversational phrases                   |
| phoneme_coverage | 10        | Sentences ensuring all phonemes present  |
| questions        | 4         | Question patterns                        |
| numbers          | 4         | Number pronunciation                     |
| food             | 4         | Food and drink vocabulary                |

## G2P Backend Information

### Korean G2P (g2pK-based)

The Korean G2P uses the g2pK library, which provides:

- Hangul decomposition into jamo (consonants and vowels)
- Application of Korean phonological rules
- Jamo to IPA conversion
- Support for:
  - Idiom/abbreviation replacement
  - English to Hangul conversion
  - Number spelling (both native and Sino-Korean)
  - Optional MeCab POS tagging

**Performance**: 100% accuracy on benchmark, 22 sent/s (without espeak)

### Espeak Fallback (Optional)

Adding espeak fallback provides:

- ~68% speed improvement (22 → 37 sent/s)
- Maintains 100% accuracy
- Handles edge cases with espeak phonemization

## Korean Phonological Features

### Three-Way Consonant Contrast

Korean distinguishes consonants in three ways:

1. **Plain** (ㄱ ㄷ ㅂ ㅅ ㅈ) - k t p s ʨ
2. **Aspirated** (ㅋ ㅌ ㅍ ㅊ) - kʰ tʰ pʰ ʨʰ (with ʰ marker)
3. **Tensed** (ㄲ ㄸ ㅃ ㅆ ㅉ) - k͈ t͈ p͈ s͈ ʨ͈ (with ͈ marker)

### Unique Vowels

Korean has vowels not found in English:

- **ɯ (으)** - Close back unrounded (unique to Korean/Turkic languages)
- **ʌ (어)** - Mid-central vowel
- **ø (외)** - Front rounded (like German/French)

### Hangul Romanization

The phoneme output uses IPA, not standard Romanization:

- 한글 → hankɯl (IPA) vs. hangul (Romanization)
- 김치 → kimʨʰi (IPA) vs. kimchi (Romanization)

## CHILDES Corpus Source

The natural speech examples were extracted from:

- **Corpus**: CHILDES IPA corpus
- **Language**: ko-KR (Korean)
- **Source size**: 23.2 MB (~94,754 sentences)
- **Selection criteria**:
  - Adult speech only (not child babbling)
  - 3-10 tokens per sentence
  - Valid Korean characters (Hangul)
  - No errors or special markers
  - Deduplicated against hand-crafted sentences

**Extraction rate**: ~4.1% (60 sentences from ~1,450 candidates)

- High filtering rate due to quality criteria
- Focus on grammatical, complete adult utterances
- All sentences validated with KoreanG2P

## Usage Examples

### Basic Benchmarking

```python
from kokorog2p.ko import KoreanG2P

# Create G2P with recommended configuration
g2p = KoreanG2P(use_espeak_fallback=True)

# Phonemize Korean text
tokens = g2p("안녕하세요")
for token in tokens:
    print(f"{token.text} → {token.phonemes}")
# Output: 안녕하세요 → annjʌhasejo
```

### Testing Different Configurations

```python
from kokorog2p.ko import KoreanG2P

# Default configuration (no MeCab)
g2p_default = KoreanG2P()

# With espeak fallback (faster)
g2p_fast = KoreanG2P(use_espeak_fallback=True)

# Test with various phrases
phrases = ["안녕하세요", "감사합니다", "사랑해요"]
for phrase in phrases:
    tokens = g2p_fast(phrase)
    print(f"{phrase}: {tokens[0].phonemes}")
```

### Running Benchmarks

```bash
# Test default configuration
python benchmarks/benchmark_ko_comparison.py --config "Korean G2P"

# Test with espeak fallback (recommended)
python benchmarks/benchmark_ko_comparison.py --config "Korean G2P + Espeak"

# See detailed output
python benchmarks/benchmark_ko_comparison.py --verbose
```

## Validation Results

Run the validator to check dataset integrity:

```bash
python benchmarks/validate_synthetic_data.py benchmarks/data/ko_synthetic.json
```

**Results**:

- ✅ All 100 sentences validated
- ✅ 100% phoneme coverage (23/23 unique characters)
- ✅ No invalid phonemes
- ✅ All required fields present

## Known Limitations

1. **No MeCab support in benchmark**: Current implementation uses simplified phonology
   without MeCab
2. **Missing advanced features**: ŋ (velar nasal) and ̚ (unreleased stops) not in current
   phoneme set
3. **No pitch accent**: Korean pitch accent is not represented in phoneme output
4. **Standard Seoul dialect**: Dataset represents standard Seoul Korean pronunciation
5. **Limited OOV handling**: Without MeCab, some complex words may have simplified
   pronunciation
6. **No liaison/sandhi marks**: Phonological changes are applied but not explicitly
   marked

## Korean G2P Phonological Rules

The g2pK backend applies standard Korean pronunciation rules including:

- **Nasalization** (제18항): 먹는 → [멍는]
- **Liquid nasalization** (제20항): 신라 → [실라]
- **Tensification** (제23항): 국밥 → [국빱]
- **Palatalization**: 굳이 → [구지]
- **Liaison** (제13항): 옷이 → [오시]
- **Aspiration** (제12항): 놓고 → [노코]
- **Coda neutralization** (제9항): 옷 → [옫]

## Future Improvements

Potential areas for enhancement:

- [ ] Add MeCab support for better morphological analysis
- [ ] Include ŋ and ̚ phonemes (requires MeCab)
- [ ] Expand dataset to 150+ sentences
- [ ] Add specialized vocabulary (medical, technical, etc.)
- [ ] Include regional dialect variations (Busan, Jeolla, etc.)
- [ ] Add more loanwords (English → Korean)
- [ ] Test compound words and complex morphology

## References

- CHILDES IPA Corpus: https://github.com/ErikMorton/ipa-childes
- g2pK: https://github.com/kyubyong/g2pK
- Korean IPA: https://en.wikipedia.org/wiki/Help:IPA/Korean
- Kokoro TTS Korean: https://github.com/hexgrad/kokoro-onnx
- Korean Standard Pronunciation Rules: https://korean.go.kr/

## Contributing

To improve the Korean dataset:

1. Add more diverse sentence patterns
2. Test with specialized vocabulary
3. Validate pronunciation with native Korean speakers
4. Report any phoneme mismatches or errors
5. Add examples of complex phonological rules

## License

The Korean synthetic dataset is released under the same license as kokorog2p.
