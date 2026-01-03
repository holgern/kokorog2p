# Italian Synthetic Benchmark Dataset

## Overview

The Italian benchmark script is located at:

- **benchmarks/benchmark_it_comparison.py**

This script tests all Italian G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_it_comparison.py

# Verbose output
python benchmarks/benchmark_it_comparison.py --verbose

# Export results
python benchmarks/benchmark_it_comparison.py --output results.json
```

## Benchmark Results (100 sentences)

| Configuration              | Accuracy | Speed         | Phonemes | Recommendation      |
| -------------------------- | -------- | ------------- | -------- | ------------------- |
| Full (stress + gemination) | 100.0%   | 9,347 sent/s  | 29       | ✅ **Best**         |
| No Stress                  | 91.0%    | 13,453 sent/s | 28       | For fast processing |
| No Gemination              | 70.0%    | 15,242 sent/s | 29       | Not recommended     |
| Minimal (no markers)       | 65.0%    | 13,306 sent/s | 28       | Not recommended     |

**Recommendation**: Use **Full configuration** (default) for Italian. It provides 100%
accuracy with proper stress and gemination marking, essential for accurate Italian
pronunciation.

## Dataset Composition

The dataset consists of 100 hand-crafted Italian sentences covering:

- **Greetings** (8 sentences): Ciao, Buongiorno, Buonasera, etc.
- **Common words** (12 sentences): Per favore, Grazie, Scusa, Sì, No, etc.
- **Numbers** (8 sentences): Uno, Due, Tre, Quattro, Cinque, etc.
- **Food** (10 sentences): Pizza, Pasta, Gelato, Caffè, Vino, etc.
- **Palatals** (8 sentences): Testing gn → ɲ, gli → ʎ
- **Affricates** (10 sentences): Testing c/ci → ʧ, g/gi → ʤ, z → ʦ
- **Gemination** (12 sentences): Double consonants with ː marker
- **Vowels** (10 sentences): Testing all 5 vowels and stress patterns
- **Conversation** (12 sentences): Natural conversational Italian
- **Complex** (10 sentences): Long sentences with multiple phonological features

**Total**: 100 sentences with complete coverage of Italian phonology

## Phoneme Coverage

The dataset achieves **96.7% coverage** (29/30 phonemes) of the Italian vocabulary:

```
a b d e f i j k l m n o p r s t u v w ɡ ɲ ʃ ʎ ʣ ʤ ʦ ʧ ˈ ː
```

**Missing phonemes** (2):

- `z` - Basic z consonant (rare in standard Italian)

**Note**: The missing phoneme is extremely rare and doesn't affect practical usage.

### Italian Vowels

Italian has 5 pure vowels that are always pronounced clearly (no reduction):

- **a** - open central (casa, amore)
- **e** - mid front (bene, mele)
- **i** - close front (vino, piccolo)
- **o** - mid back (sole, pomodoro)
- **u** - close back (uno, scusa)

**Stressed vowels** can be marked with accents in spelling:

- **à è é ì ò ó ù** - indicate irregular stress (caffè, città, perché)
- In phonemes: stress is marked AFTER the vowel with **ˈ** (eˈ for è)

### Italian Consonants

**Special Italian Sounds:**

- **ɲ** - palatal nasal (gn: gnocchi, bagno, Spagna)
- **ʎ** - palatal lateral (gli: famiglia, figlio, aglio)
- **ʃ** - voiceless postalveolar (sc+e/i: pesce, scienza)

**Affricates:**

- **ʧ** - voiceless palatal affricate (c+e/i: ciao, cento; ch+i)
- **ʤ** - voiced palatal affricate (g+e/i: giorno, gelato)
- **ʦ** - voiceless alveolar affricate (z: pizza, grazie, zio)
- **ʣ** - voiced alveolar affricate (z in some contexts: zero)

**Standard Consonants:**

- **b d f l m n p r t v** - similar to English
- **s** - voiceless alveolar fricative (casa, sole)
- **k** - voiceless velar (c+a/o/u: casa, cosa; ch+e/i: che, chi)
- **ɡ** - voiced velar (g+a/o/u: gatto, gusto; gh+e/i: ghetto)

**Semivowels:**

- **j** - palatal approximant (piano, ieri)
- **w** - labial-velar approximant (qu: quando, acqua; uo: uomo)

### Special Markers

- **ˈ** - primary stress marker (placed AFTER the stressed vowel)
  - Used for words with irregular stress: caffèˈ, citàˈ
  - Penultimate stress (default) usually not marked
- **ː** - length/gemination marker (placed AFTER the consonant)
  - Indicates double consonants: pizza → piʦːa
  - Phonemically distinctive: pala (shovel) vs palla (ball) → pal a vs palːa

## Italian Phonology Features

### 1. Gemination (Double Consonants)

Gemination is phonemically distinctive in Italian. Double consonants are marked with
**ː**:

- **casa** /kasa/ (house) vs **cassa** /kasːa/ (cash register)
- **pala** /pala/ (shovel) vs **palla** /palːa/ (ball)
- **sete** /sete/ (thirst) vs **sette** /setːe/ (seven)

**Special gemination rules:**

- **cc** before e/i → ʧː (cappuccino → kapːuʧːino)
- **gg** before e/i → ʤː (oggi → oʤːi)
- **cqu** → kːw (acqua → akːwa)

### 2. Soft vs Hard C and G

Context-sensitive pronunciation:

**C consonant:**

- c + e, i → **ʧ** (ciao, cento)
- c + a, o, u → **k** (casa, cosa, cucina)
- ch + e, i → **k** (che, chi)

**G consonant:**

- g + e, i → **ʤ** (giorno, gelato)
- g + a, o, u → **ɡ** (gatto, gondola, gusto)
- gh + e, i → **ɡ** (ghetto, ghiaccio)

**Silent 'i' rule:**

- After soft g/c, 'i' before another vowel is often silent:
  - **formaggio** → formaʤːo (not formaʤːio)
  - **mangia** → manʤa (not manʤia)
- Exception: when 'i' precedes certain consonants:
  - **giorno** → ʤiorno (keep 'i' before 'r', 'n')

### 3. SC Combinations

- sc + e, i → **ʃ** (pesce, scienza)
- sc + a, o, u → **sk** (scatola, scuola)

### 4. Palatals

- **gn** → **ɲ** (gnocchi, bagno, agnello)
- **gli** → **ʎ** before vowels (famiglia, figlio, aglio)
- **gl** + consonant → **ɡl** (inglese)

### 5. Stress Patterns

Default stress is on the **penultimate** syllable:

- **casa** → kasa (stress on 'a')
- **parlare** → parlare (stress on 'a')

Irregular stress marked with accents:

- **caffè** → kafːeˈ (final stress)
- **città** → ʧitːaˈ (final stress)
- **telefono** → telefono (third-to-last stress, no accent needed in phonemes)

### 6. Contractions and Apostrophes

Italian uses apostrophes for elision:

- **l'uomo** → luomo (article + noun)
- **c'è** → ʧeˈ (ci + è)
- **po'** (poco) → poˈ (stress on final vowel)

## Implementation Notes

### Rule-Based G2P

The Italian G2P uses a pure rule-based approach with a small exception lexicon:

**Why rule-based works well:**

- Italian orthography is highly regular and phonemic
- Clear, predictable rules for c/g softening
- Consistent stress patterns
- Few exceptions to phonological rules

**Exception lexicon** (5 words):

- `scusa` → skuʦa (intervocalic s → ʦ)
- `scusi` → skuʦi
- `poˈ` → poˈ (preprocessed from po')
- `gli` → ʎi (article keeps 'i')
- `olio` → oljo ('i' as semivowel)

### Phoneme Notation

The Italian G2P follows IPA conventions with TTS-friendly adaptations:

1. **Stress**: Marked AFTER vowel (eˈ not ˈe) for easier TTS processing
2. **Gemination**: Uses ː (length marker) rather than doubling (ʦː not ʦʦ)
3. **Affricates**: Single symbols (ʧ, ʤ, ʦ, ʣ) rather than digraphs
4. **IPA g**: Uses ɡ (U+0261) not g (U+0067) for voiced velar

## Usage Examples

```python
from kokorog2p.it import ItalianG2P

# Create G2P instance
g2p = ItalianG2P()

# Basic conversion
tokens = g2p("Ciao, come stai?")
# Result: [GToken(text="Ciao", phonemes="ʧiao"), ...]

# Get phoneme string
phonemes = g2p.phonemize("Buongiorno! Come sta?")
# Result: "buonʤiorno! kome sta?"

# Disable stress markers
g2p_no_stress = ItalianG2P(mark_stress=False)
phonemes = g2p_no_stress.phonemize("Caffè")
# Result: "kafːe" (no ˈ marker)

# Disable gemination markers
g2p_no_gem = ItalianG2P(mark_gemination=False)
phonemes = g2p_no_gem.phonemize("Pizza")
# Result: "piʦa" (no ː marker)
```

## Validation

The dataset has been validated for:

✅ **Phoneme coverage**: 96.7% (29/30 phonemes) ✅ **Accuracy**: 100% on all 100
benchmark sentences ✅ **Speed**: 9,347 sentences/second ✅ **Category coverage**: All
10 phonological categories covered ✅ **Stress marking**: Correct stress placement in
all cases ✅ **Gemination**: All double consonants properly marked

## Dataset Statistics

```json
{
  "total_sentences": 100,
  "total_words": 246,
  "total_phonemes": 30,
  "covered_phonemes": 29,
  "coverage_percentage": 96.7,
  "categories": {
    "greetings": 8,
    "common_words": 12,
    "numbers": 8,
    "food": 10,
    "palatals": 8,
    "affricates": 10,
    "gemination": 12,
    "vowels": 10,
    "conversation": 12,
    "complex": 10
  }
}
```

## Future Enhancements

Potential improvements:

1. Add CHILDES it-IT corpus samples for natural speech
2. Expand lexicon for common irregular words
3. Add regional pronunciation variants (Sicilian, Neapolitan, etc.)
4. Implement raddoppiamento sintattico (word-boundary doubling)
5. Distinguish voiced/voiceless z ([ʦ] vs [ʣ]) by context

## References

- [Italian Phonology - Wikipedia](https://en.wikipedia.org/wiki/Italian_phonology)
- [IPA for Italian - Wikipedia](https://en.wikipedia.org/wiki/Help:IPA/Italian)
- Italian dictionaries with IPA transcriptions
- CHILDES Italian corpus (planned integration)

## License

This dataset is part of the kokorog2p project and is licensed under the same terms as
the main project.
