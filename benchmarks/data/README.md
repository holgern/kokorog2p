# Synthetic Benchmark Data

This directory contains synthetic benchmark datasets for testing kokorog2p configurations across all supported languages.

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

| File | Language | Sentences | Phonemes | Status |
|------|----------|-----------|----------|--------|
| `en_us_synthetic.json` | English (US) | 205 | 46/46 (100%) | ✅ Complete |
| `en_gb_synthetic.json` | English (GB) | 201 | 45/45 (100%) | ✅ Complete |
| `de_synthetic.json` | German | 189 | 307 unique | ✅ Complete |
| `fr_synthetic.json` | French | - | - | 🚧 Planned |
| `cs_synthetic.json` | Czech | - | - | 🚧 Planned |

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

# Test specific language
python benchmarks/benchmark_en_us_comparison.py --language en-us
python benchmarks/benchmark_en_gb_comparison.py --language en-gb

# Test single configuration
python benchmarks/benchmark_en_us_comparison.py --config "Gold + Espeak"

# Verbose output with errors
python benchmarks/benchmark_en_us_comparison.py --verbose

# Export results to JSON
python benchmarks/benchmark_en_us_comparison.py --output results_en_us.json
python benchmarks/benchmark_en_gb_comparison.py --output results_en_gb.json
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

**Important**: The phonemes in synthetic datasets represent the *expected output* of the G2P system for the given configuration, not necessarily the single "correct" pronunciation.

### Why This Matters

- **Context-dependent**: Words like "the" can be pronounced as `ðə` (weak) or `ði` (strong)
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

The German dataset (`de_synthetic.json`) contains 189 sentences with 307 unique phoneme combinations.

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
- **Categories**: greetings, geography, weather, conversation, phoneme_coverage, numbers, family, complex
- **100% accuracy** with German G2P + espeak fallback

## Performance Expectations

Typical benchmark results on modern hardware:

| Configuration | Accuracy | Speed | Use Case |
|--------------|----------|-------|----------|
| Gold + Silver | ~95% | 50-80K w/s | Best accuracy for common words |
| Gold + Silver + Espeak | ~85% | 30-50K w/s | Good balance of coverage + speed |
| Gold + Silver + Goruut | ~90% | 20-40K w/s | Best for new/rare words |
| Espeak only | ~75% | 40-60K w/s | Fast, good for prototyping |
| Goruut only | ~80% | 25-45K w/s | Best OOV handling |

*Note: Accuracy depends on how closely ground truth matches the tested configuration*

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
