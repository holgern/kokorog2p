# Synthetic Benchmark Data

This directory contains synthetic benchmark datasets for testing kokorog2p
configurations across all supported languages.

## Overview

The synthetic benchmarks enable comprehensive testing of all G2P configurations:

- **Lexicon-only** (gold/silver/both)
- **Espeak fallback** (with gold/silver/none)
- **Goruut fallback** (with gold/silver/none)

Each benchmark file contains carefully curated sentences designed to:

- Cover all Kokoro phonemes (100% coverage)
- Test specific phonological features (diphthongs, contractions, stress patterns)
- Include OOV words to test fallback mechanisms
- Represent realistic usage patterns

## Available Datasets

| File                   | Language     | Sentences | Phonemes     | Status      |
| ---------------------- | ------------ | --------- | ------------ | ----------- |
| `en_us_synthetic.json` | English (US) | 205       | 46/46 (100%) | ✅ Complete |
| `en_gb_synthetic.json` | English (GB) | 201       | 45/45 (100%) | ✅ Complete |
| `de_synthetic.json`    | German       | 189       | 307 unique   | ✅ Complete |
| `ja_synthetic.json`    | Japanese     | 371       | 29/29 (100%) | ✅ Complete |
| `fr_synthetic.json`    | French       | 154       | 35/35 (100%) | ✅ Complete |
| `ko_synthetic.json`    | Korean       | 100       | 23/23 (100%) | ✅ Complete |
| `cs_synthetic.json`    | Czech        | -         | -            | 🚧 Planned  |

## File Format

Each synthetic dataset follows this JSON schema:

```json
{
  "metadata": {
    "version": "1.0.0",
    "language": "en-us",
    "created_date": "2026-01-03",
    "description": "Human-readable description",
    "phoneme_set": "kokoro",
    "total_sentences": 95,
    "categories": {
      "phoneme_coverage": 18,
      "stress_patterns": 10,
      ...
    }
  },
  "sentences": [
    {
      "id": 1,
      "text": "The quick brown fox jumps over the lazy dog.",
      "phonemes": "ðə kwˈɪk bɹˈWn fˈɑks ʤˈʌmps ˈOvəɹ ðə lˈAzi dˈɔɡ",
      "category": "phoneme_coverage",
      "difficulty": "basic",
      "word_count": 9,
      "contains_oov": false,
      "notes": "Classic pangram - basic phoneme coverage"
    }
  ]
}
```

### Field Descriptions

**Metadata:**

- `version`: Semantic version of the dataset
- `language`: Language code (ISO 639-1 + country code)
- `created_date`: Date created (YYYY-MM-DD)
- `description`: Human-readable description
- `phoneme_set`: Always "kokoro"
- `total_sentences`: Number of sentences
- `categories`: Breakdown by category

**Sentence:**

- `id`: Unique integer ID (1-indexed)
- `text`: The sentence text to phonemize
- `phonemes`: Ground truth phonemes (space-separated by word)
- `category`: Test category (see below)
- `difficulty`: `basic` | `intermediate` | `advanced`
- `word_count`: Number of words
- `contains_oov`: Whether sentence contains OOV words
- `notes`: Optional description

### Sentence Categories

1. **phoneme_coverage** - Cover all Kokoro phonemes
2. **stress_patterns** - Primary (ˈ) and secondary (ˌ) stress
3. **contractions** - don't, won't, I'm, etc.
4. **common_words** - High-frequency vocabulary
5. **diphthongs** - A, I, O/Q, W, Y sounds
6. **oov_words** - Out-of-vocabulary words (tests fallback)
7. **numbers_punctuation** - Numbers and punctuation handling
8. **compounds** - Hyphenated and compound words
9. **minimal_pairs** - Words differing by one phoneme
10. **mixed_difficulty** - Complex real-world sentences
11. **gb_specific** - GB-specific phoneme features (for en-gb only)

## Usage

### Validate Synthetic Data

```bash
# Validate a specific file
python benchmarks/validate_synthetic_data.py benchmarks/data/en_us_synthetic.json

# Validate all synthetic files
python benchmarks/validate_synthetic_data.py --all
```

The validator checks:

- JSON schema correctness
- Phoneme validity (all in Kokoro vocabulary)
- Phoneme coverage statistics
- Internal consistency (IDs, counts, etc.)

### Run Benchmarks

```bash
# Test all US English configurations
python benchmarks/benchmark_en_us_comparison.py

# Test all GB English configurations
python benchmarks/benchmark_en_gb_comparison.py

# Test all German configurations
python benchmarks/benchmark_de_comparison.py

# Test all Japanese configurations
python benchmarks/benchmark_ja_comparison.py

# Test all French configurations
python benchmarks/benchmark_fr_comparison.py

# Test all Korean configurations
python benchmarks/benchmark_ko_comparison.py

# Test specific language
python benchmarks/benchmark_en_us_comparison.py --language en-us
python benchmarks/benchmark_en_gb_comparison.py --language en-gb

# Test single configuration
python benchmarks/benchmark_en_us_comparison.py --config "Gold + Espeak"
python benchmarks/benchmark_ja_comparison.py --config "pyopenjtalk"
python benchmarks/benchmark_fr_comparison.py --config "Gold only"
python benchmarks/benchmark_ko_comparison.py --config "Korean G2P + Espeak"

# Verbose output with errors
python benchmarks/benchmark_en_us_comparison.py --verbose

# Export results to JSON
python benchmarks/benchmark_en_us_comparison.py --output results_en_us.json
python benchmarks/benchmark_en_gb_comparison.py --output results_en_gb.json
python benchmarks/benchmark_de_comparison.py --output results_de.json
python benchmarks/benchmark_ja_comparison.py --output results_ja.json
python benchmarks/benchmark_fr_comparison.py --output results_fr.json
python benchmarks/benchmark_ko_comparison.py --output results_ko.json
```

The benchmark tests:

- **Accuracy**: Matches against ground truth
- **Speed**: Words per second
- **Phoneme coverage**: % of Kokoro phonemes used
- **OOV success rate**: % of OOV words handled correctly
- **Fallback usage**: % of time fallback was needed

### Generate Phonemes

Helper script to generate phonemes for new sentences:

```bash
python benchmarks/generate_phonemes.py "Your sentence here."
```

This tool:

1. Checks gold dictionary first
2. Cross-validates espeak and goruut
3. Reports mismatches
4. Shows the source of each phoneme

## Creating New Benchmark Data

### Step 1: Design Sentences

Create sentences that:

- Cover target phonemes systematically
- Use natural, grammatical language
- Include various difficulty levels
- Test specific features (contractions, stress, etc.)

### Step 2: Generate Phonemes

Use the helper script to get initial phonemes:

```bash
python benchmarks/generate_phonemes.py "Your test sentence."
```

Review the output for:

- Conflicts between backends
- Missing phonemes
- Unexpected pronunciations

### Step 3: Create JSON File

Follow the schema above. Use `en_us_synthetic.json` as a template.

### Step 4: Validate

Run the validator:

```bash
python benchmarks/validate_synthetic_data.py your_file.json
```

Fix any errors until validation passes.

### Step 5: Test

Run the benchmark:

```bash
python benchmarks/benchmark_fallback_comparison.py --language your-lang
```

## Ground Truth Philosophy

**Important**: The phonemes in synthetic datasets represent the _expected output_ of the
G2P system for the given configuration, not necessarily the single "correct"
pronunciation.

### Why This Matters

- **Context-dependent**: Words like "the" can be pronounced as `ðə` (weak) or `ði`
  (strong)
- **Dialect variation**: US vs GB English have different valid pronunciations
- **Heteronyms**: Words like "read" have multiple valid pronunciations
- **Stress variation**: Function words may or may not receive stress

### Our Approach

We use a **hybrid validation strategy**:

1. **Gold dictionary first**: For words in the gold dictionary, use those phonemes
2. **Cross-validation**: For OOV words, compare espeak and goruut outputs
3. **Manual review**: Resolve conflicts based on linguistic knowledge
4. **Consistency**: Prefer consistency with existing lexicon

This ensures benchmarks test for:

- Regression detection (did output change?)
- Configuration comparison (which setup performs best?)
- Coverage validation (are all phonemes reachable?)

## US English Phonemes (46 total)

### Shared with GB (41)

- Stress: `ˈ` `ˌ`
- Consonants: `b d f h j k l m n p s t v w z ɡ ŋ ɹ ʃ ʒ ð θ`
- Affricates: `ʤ ʧ`
- Vowels: `ə i u ɑ ɔ ɛ ɜ ɪ ʊ ʌ`
- Diphthongs: `A` (eɪ), `I` (aɪ), `W` (aʊ), `Y` (ɔɪ)
- Custom: `ᵊ` (reduced schwa)

### US-Specific (5)

- `æ` - TRAP vowel (cat, bat)
- `O` - GOAT diphthong (oʊ) (go, show)
- `ᵻ` - Reduced vowel (boxes)
- `ɾ` - Alveolar flap (butter, water)
- `ʔ` - Glottal stop (button)

## British English Phonemes (45 total)

### Shared with US (41)

Same as above

### GB-Specific (4)

- `a` - TRAP vowel (cat, bat) - replaces US `æ`
- `Q` - GOAT diphthong (əʊ) (go, show) - replaces US `O`
- `ɒ` - LOT vowel (hot, got, stop)
- `ː` - Length mark (car → kɑː, more → mɔː)

### Key GB vs US Differences

- **TRAP vowel**: GB uses `a`, US uses `æ`
- **GOAT diphthong**: GB uses `Q` (əʊ), US uses `O` (oʊ)
- **LOT vowel**: GB has distinct `ɒ`, US merges with `ɑ`
- **R-dropping**: GB uses length marks `ː` (car → kɑː), US keeps `ɹ` (car → kɑɹ)
- **No flapping**: GB keeps `t` (butter), US uses `ɾ` (butter)
- **No glottal stop**: GB uses `t` (button), US uses `ʔ` (button)

## German Phonemes

The German dataset (`de_synthetic.json`) contains 189 sentences with 307 unique phoneme
combinations.

### Key German Phonological Features

- **Umlauts**: ä ö ü (special German vowels)
- **Final obstruent devoicing** (Auslautverhärtung): `b→p`, `d→t`, `g→k` word-finally
- **CH sounds**:
  - `ç` - ich-Laut (after front vowels: ich, nicht, möchte)
  - `x` - ach-Laut (after back vowels: nach, Buch, auch)
- **Long vowels**: Marked with `ː` (e.g., `aː`, `eː`, `oː`)
- **Diphthongs**: `aɪ` (ei), `aʊ` (au), `ɔɪ` (eu/äu)
- **Affricates**: `ʦ` (z/tz), `ʧ` (tsch), `pf`
- **Consonant r**: `ʁ` (uvular fricative)

### German Dataset Composition

- **41 hand-crafted sentences** covering core German phonology
- **148 natural speech examples** from CHILDES corpus (adult speech)
- **Categories**: greetings, geography, weather, conversation, phoneme_coverage,
  numbers, family, complex
- **100% accuracy** with German G2P + espeak fallback

## Japanese Phonemes

The Japanese dataset (`ja_synthetic.json`) contains 371 sentences with 29 unique phoneme
characters achieving 100% phoneme coverage.

### Key Japanese Phonological Features

- **Character-based phonemes**: Unlike European languages, each character in the phoneme
  string is a single phoneme (not space-separated)
- **Basic vowels**: a e i o u
- **Consonants**: b d f g h j k m n p r s t w z
- **Special phonemes**:
  - `ɕ` - palatal fricative (shi sound)
  - `ɴ` - moraic n (syllabic n)
  - `ʔ` - glottal stop
- **Affricates**:
  - `ʥ` - voiced affricate (ji sound)
  - `ʦ` - voiceless affricate (tsu sound)
  - `ʨ` - palatal affricate (chi sound)
- **Length marker**: `ː` - long vowel marker
- **Special markers**: `ᶄ` `ᶉ` - special pronunciation markers

### Japanese Dataset Composition

- **31 hand-crafted sentences** covering common phrases, greetings, questions, numbers
- **340 natural speech examples** from CHILDES ja-JP corpus (adult speech)
- **Categories**: greetings, common_words, questions, numbers, verbs, adjectives,
  conversation, childes_natural
- **100% accuracy** with pyopenjtalk backend
- **Backend**: Uses pyopenjtalk (recommended) or cutlet for kana/kanji → phoneme
  conversion

### Japanese Benchmark Results

| Configuration        | Accuracy | Speed        | Notes                            |
| -------------------- | -------- | ------------ | -------------------------------- |
| pyopenjtalk + espeak | 100%     | 6,286 sent/s | Recommended (fastest + accurate) |
| pyopenjtalk          | 100%     | 1,716 sent/s | Good default                     |
| cutlet               | N/A      | -            | Requires MeCab installation      |

## French Phonemes

The French dataset (`fr_synthetic.json`) contains 154 sentences with 35 unique phoneme
characters achieving 100% phoneme coverage.

### Key French Phonological Features

**Nasal vowels** (with combining tilde ̃):

- `ɑ̃` - nasal A (dans, enfant, temps)
- `ɛ̃` - nasal E (vin, pain, bien)
- `œ̃` - nasal EU (un, parfum)
- `ɔ̃` - nasal O (bon, monde, nom)

**Special consonants**:

- `ʁ` - uvular fricative (French R: rouge, Paris)
- `ʃ` - voiceless postalveolar fricative (ch: chat, chaud)
- `ʒ` - voiced postalveolar fricative (j: je, rouge)
- `ɥ` - labial-palatal approximant (ui: huit, nuit)

**Oral vowels**:

- `a` - open front (chat)
- `ɑ` - open back (pâte)
- `e` - close front (été)
- `ɛ` - open-mid front (père)
- `ə` - schwa (le, de)
- `i` - close front (si)
- `o` - close-mid back (beau)
- `ɔ` - open-mid back (porte)
- `ø` - close-mid front rounded (peu)
- `œ` - open-mid front rounded (peur)
- `u` - close back rounded (tout)
- `y` - close front rounded (tu)

**Standard consonants**:

- `b d f ɡ j k l m n p s t v w z` - similar to other languages

**Punctuation/markers**:

- `'` - apostrophe (l'ami)
- `,` - comma
- `-` - hyphen

### French Dataset Composition

- **35 hand-crafted sentences** covering greetings, common phrases, numbers
- **119 natural speech examples** from CHILDES fr-FR corpus (adult speech)
- **Categories**: greetings (4), common_words (8), conversation (5), numbers (3),
  phoneme_coverage (6), childes_natural (119)
- **100% accuracy** with French gold lexicon (15,011 entries)

### French Benchmark Results

| Configuration | Accuracy | Speed        | Notes                                  |
| ------------- | -------- | ------------ | -------------------------------------- |
| Gold only     | 100%     | 9,399 sent/s | ✅ Recommended (best speed + accuracy) |
| Gold + Goruut | 100%     | 7,783 sent/s | Good alternative                       |
| Gold + Espeak | 100%     | 7,669 sent/s | Good alternative                       |
| Espeak only   | 44.2%    | 1,059 sent/s | Not recommended                        |
| Goruut only   | 20.8%    | 54 sent/s    | Very slow, not recommended             |

### French CHILDES Extraction Notes

The French dataset has a smaller size (154 sentences) compared to other languages due
to:

- High OOV rate in CHILDES data (~63% of sentences had unknown phonemes)
- Strict quality filtering (only sentences with valid phonemes accepted)
- Lower retention rate (~37%) after phoneme validation
- Focus on quality over quantity

## Korean Phonemes

The Korean dataset (`ko_synthetic.json`) contains 100 sentences with 23 unique phoneme
characters achieving 100% phoneme coverage.

### Key Korean Phonological Features

**Character-based phonemes** (like Japanese):

- Each character in the phoneme string is a single phoneme
- Example: 안녕하세요 → annjʌhasejo (11 characters = 11 phonemes)

**Vowels**:

- **Basic**: a e i o u (similar to other languages)
- **Special**: ø (외), ɛ (애), ɯ (으), ɰ (의 onset), ʌ (어)

**Consonants**:

- **Basic**: h j k l m n p s t w
- **Affricate**: ʨ (ㅈ/ㅊ)

**Phonological features**:

- **ʰ** - aspiration marker (ㅋ ㅌ ㅍ ㅊ → kʰ tʰ pʰ ʨʰ)
- **͈** - tenseness marker (ㄲ ㄸ ㅃ ㅆ ㅉ → k͈ t͈ p͈ s͈ ʨ͈)

### Korean Three-Way Contrast

Korean uniquely distinguishes consonants three ways:

1. **Plain** - ㄱ ㄷ ㅂ ㅅ ㅈ (k t p s ʨ)
2. **Aspirated** - ㅋ ㅌ ㅍ ㅊ (kʰ tʰ pʰ ʨʰ)
3. **Tensed** - ㄲ ㄸ ㅃ ㅆ ㅉ (k͈ t͈ p͈ s͈ ʨ͈)

### Korean Dataset Composition

- **40 hand-crafted sentences** covering greetings, common words, numbers, food, phoneme
  coverage
- **60 natural speech examples** from CHILDES ko-KR corpus (adult speech)
- **Categories**: greetings (5), common_words (8), numbers (4), food (4),
  phoneme_coverage (10), questions (4), conversation (5), childes_natural (60)
- **100% accuracy** with Korean G2P (g2pK-based)

### Korean Benchmark Results

| Configuration       | Accuracy | Speed     | Notes                               |
| ------------------- | -------- | --------- | ----------------------------------- |
| Korean G2P + Espeak | 100%     | 37 sent/s | ✅ Recommended (fastest + accurate) |
| Korean G2P          | 100%     | 22 sent/s | Good default                        |

### Korean G2P Backend (g2pK)

The Korean G2P uses g2pK which provides:

- Hangul → jamo decomposition
- Korean phonological rules application
- Jamo → IPA conversion
- Optional MeCab support (not required for 100% accuracy)

**Without MeCab** (current implementation):

- Simplified phonology
- No ŋ (velar nasal) or ̚ (unreleased stops)
- Still achieves 100% benchmark accuracy
- Faster processing

**With MeCab** (optional):

- More accurate morphological analysis
- Proper handling of ŋ and ̚
- Better context-dependent pronunciation
- Install: `pip install mecab-python3`

### Korean CHILDES Extraction Notes

- **Source**: 23.2 MB (~94,754 sentences)
- **Extraction rate**: ~4.1% (60 from ~1,450 candidates)
- **Filtering**: Adult speech, 3-10 tokens, valid Hangul, no errors
- **Quality focus**: All sentences validated with KoreanG2P

## Performance Expectations

Typical benchmark results on modern hardware:

| Configuration          | Accuracy | Speed      | Use Case                         |
| ---------------------- | -------- | ---------- | -------------------------------- |
| Gold + Silver          | ~95%     | 50-80K w/s | Best accuracy for common words   |
| Gold + Silver + Espeak | ~85%     | 30-50K w/s | Good balance of coverage + speed |
| Gold + Silver + Goruut | ~90%     | 20-40K w/s | Best for new/rare words          |
| Espeak only            | ~75%     | 40-60K w/s | Fast, good for prototyping       |
| Goruut only            | ~80%     | 25-45K w/s | Best OOV handling                |

_Note: Accuracy depends on how closely ground truth matches the tested configuration_

## Extending to Other Languages

To create benchmarks for a new language:

1. **Study the phoneme inventory** for that language in Kokoro
2. **Identify key phonological features** (clusters, tones, stress, etc.)
3. **Create sentence categories** targeting those features
4. **Use native speaker knowledge** to ensure natural sentences
5. **Cross-validate** with available backends
6. **Document language-specific notes** in the metadata

## Contributing

When adding or improving synthetic data:

1. Ensure 100% phoneme coverage (or document why not possible)
2. Include a variety of difficulty levels
3. Test with the benchmark script before committing
4. Run the validator to ensure correctness
5. Update this README with any new categories or insights

## References

- Kokoro TTS: https://github.com/hexgrad/kokoro-onnx
- Misaki Phonemes: https://github.com/hexgrad/misaki/blob/main/EN_PHONES.md
- IPA Chart: https://www.internationalphoneticalphabet.org/

## License

Synthetic benchmark data is released under the same license as kokorog2p.
