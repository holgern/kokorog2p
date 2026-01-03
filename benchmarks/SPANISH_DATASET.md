# Spanish Synthetic Benchmark Dataset

## Overview

The Spanish benchmark script is located at:

- **benchmarks/benchmark_es_comparison.py**

This script tests all Spanish G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_es_comparison.py

# Verbose output
python benchmarks/benchmark_es_comparison.py --verbose

# Export results
python benchmarks/benchmark_es_comparison.py --output results.json
```

## Benchmark Results (100 sentences)

| Configuration           | Accuracy | Speed         | Phonemes | Recommendation  |
| ----------------------- | -------- | ------------- | -------- | --------------- |
| Full (European Spanish) | 100.0%   | 17,863 sent/s | 27       | ✅ **Best**     |
| Latin American          | 78.0%    | 18,757 sent/s | 26       | For LA dialect  |
| No Stress (European)    | 76.0%    | 19,465 sent/s | 26       | Not recommended |
| Minimal (LA, no stress) | 60.0%    | 27,259 sent/s | 25       | Not recommended |

**Recommendation**: Use **Full configuration** (European Spanish, default) for best
accuracy. It provides 100% accuracy with proper stress marking and European Spanish
pronunciation features (including theta θ).

**Note**: The Latin American configuration has lower accuracy because the dataset uses
European Spanish phonology. Both dialects are fully supported.

## Dataset Composition

The dataset consists of 100 hand-crafted Spanish sentences covering:

- **Greetings** (8 sentences): Hola, Buenos días, Adiós, Hasta luego, etc.
- **Common words** (12 sentences): Por favor, Gracias, Sí, No, Perdón, etc.
- **Numbers** (8 sentences): Uno, Dos, Tres, Cuatro, Cinco, etc.
- **Food** (10 sentences): Pan, Vino, Café, Paella, Jamón, etc.
- **Palatals** (8 sentences): Testing ñ → ɲ, ll → ʎ, ch → ʧ
- **Jota** (8 sentences): Testing j → x, g+e/i → x
- **Theta** (8 sentences): Testing z → θ, c+e/i → θ (European Spanish)
- **R sounds** (10 sentences): Testing r (trill) vs ɾ (tap) distinction
- **Conversation** (18 sentences): Natural conversational Spanish
- **Complex** (10 sentences): Long sentences with multiple phonological features

**Total**: 100 sentences with complete coverage of Spanish phonology

## Phoneme Coverage

The dataset achieves **86.2% coverage** (25/29 phonemes) of the Spanish vocabulary:

```
a b d e f i k l m n o p r s t u x ɡ ɲ ɾ ʎ ʧ θ ˈ j
```

**Missing phonemes** (4):

- `w` - labial-velar approximant (reserved for diphthongs, handled by TTS)
- `β`, `ð`, `ɣ` - approximant variants of b/d/g (reserved for future use)

**Note**: The missing phonemes are allophonic variants or handled by the TTS system.
They don't affect practical usage.

### Spanish Vowels

Spanish has 5 pure vowels that are always pronounced clearly (no schwa reduction):

- **a** - open central (casa, agua)
- **e** - mid front (leche, mesa)
- **i** - close front (niño, vino)
- **o** - mid back (ocho, ojo)
- **u** - close back (uno, azul)

**Stressed vowels** can be marked with accents in spelling:

- **á é í ó ú** - indicate irregular stress (café, música, árbol)
- In phonemes: stress is marked AFTER the vowel with **ˈ** (eˈ for é)

### Spanish Consonants

**Special Spanish Sounds:**

- **ɲ** - palatal nasal (ñ: niño, mañana, España)
- **ʎ** - palatal lateral (ll: llamar, calle, lluvia)
- **θ** - voiceless interdental fricative (z, c+e/i: zapato, cielo) - European Spanish
  only
- **x** - voiceless velar fricative (j, g+e/i: jamón, gente)
- **ʧ** - voiceless palatal affricate (ch: chico, leche)

**R Sounds (Phonemically Distinctive):**

- **r** - alveolar trill (rr, word-initial r, r after n/l/s: perro, rosa, enredar)
- **ɾ** - alveolar tap (single r between vowels or word-final: pero, hablar)

**Standard Consonants:**

- **b d f k l m n p s t** - similar to English
- **ɡ** - voiced velar stop (g+a/o/u: gato, amigo)

**Semivowel:**

- **j** - palatal approximant (y as consonant: yo, ayer)

### Special Markers

- **ˈ** - primary stress marker (placed AFTER the stressed vowel)
  - Used for words with accented vowels: café → kafeˈ
  - Words without accents follow default stress rules (not always marked)

## Spanish Phonology Features

### 1. R Tap vs Trill Distinction

The distinction between **r** (trill) and **ɾ** (tap) is **phonemically distinctive** in
Spanish:

**Minimal pairs:**

- **pero** /peɾo/ (but) vs **perro** /pero/ (dog)
- **caro** /kaɾo/ (expensive) vs **carro** /karo/ (car)

**R trill [r] rules:**

- **rr** (double r) → r: perro, carro, tierra
- **Word-initial r** → r: rosa, río, rojo
- **r after n, l, s** → r: enredar, alrededor, israelí

**R tap [ɾ] rules:**

- **Single r between vowels** → ɾ: pero, caro, mira
- **Single r after consonant** (except n/l/s) → ɾ: gracias, tres, brazo
- **Word-final r** → ɾ: hablar, amor, mejor

### 2. Soft vs Hard C and G

Context-sensitive pronunciation:

**C consonant:**

- c + e, i → **θ** (European) or **s** (Latin American): cielo, cinco
- c + a, o, u → **k**: casa, cosa, cuatro
- z → **θ** (European) or **s** (Latin American): zapato, azul

**G consonant:**

- g + e, i → **x** (jota sound): gente, gitano
- g + a, o, u → **ɡ**: gato, amigo, gusto
- j → **x** (jota sound): jamón, joven

### 3. QU and GU Combinations

**QU combinations:**

- qu + e, i → **k** (u is silent): queso, quiero, quien

**GU combinations:**

- gu + e, i → **ɡ** (u is silent): guerra, guitarra
- gü + e, i → **ɡw** (u pronounced): pingüino, vergüenza

### 4. Palatals

**Ñ (palatal nasal):**

- ñ → **ɲ**: niño, año, mañana, español

**LL (palatal lateral):**

- ll → **ʎ**: llamar, calle, lluvia, paella
- Note: In some dialects, ll → j (yeísmo), but we use traditional ʎ

**CH (palatal affricate):**

- ch → **ʧ**: chico, leche, ocho, mucho

### 5. Silent H

The letter 'h' is always silent in Spanish:

- **hola** → ola
- **hacer** → aseɾ
- **hasta** → asta
- **ahora** → aoɾa

### 6. B/V Merger

In modern Spanish, 'b' and 'v' are pronounced identically as **b**:

- **vino** → bino
- **boca** → boka
- **cerveza** → θeɾbeθa (European) / seɾbesa (Latin American)

### 7. European vs Latin American Spanish

**Main difference: Theta (θ) vs Seseo (s)**

**European Spanish (dialect="es"):**

- z → **θ**: zapato → θapato
- c + e/i → **θ**: cielo → θielo, cinco → θinko

**Latin American Spanish (dialect="la"):**

- z → **s**: zapato → sapato
- c + e/i → **s**: cielo → sielo, cinco → sinko

**Other features (same in both):**

- R trill/tap distinction preserved
- Palatals (ñ, ll, ch) pronounced the same
- Jota sound (x) pronounced the same
- Stress patterns identical

## Stress Rules

Spanish has predictable stress patterns:

**Default stress (when no accent):**

1. Words ending in **vowel, n, or s**: stress on **penultimate** syllable

   - casa → kasa (stress on first 'a')
   - hablan → ablan (stress on 'a')
   - casas → kasas (stress on first 'a')

2. Words ending in **consonant** (except n, s): stress on **final** syllable
   - español → espaɲol (stress on 'o')
   - hablar → ablaɾ (stress on 'a')
   - ciudad → θiudad (stress on 'a')

**Irregular stress (accented vowels):**

- Accents override default rules: **á é í ó ú**
- café → kafeˈ (final stress, despite ending in vowel)
- música → muˈsika (antepenultimate stress)
- árbol → aˈɾbol (penultimate stress, despite consonant ending)

In our phoneme notation, stress is marked with **ˈ** placed AFTER the stressed vowel.

## Usage Examples

```python
from kokorog2p.es import SpanishG2P

# European Spanish (default, with theta θ)
g2p_es = SpanishG2P(dialect="es", mark_stress=True)

# Basic greetings
print(g2p_es.phonemize("Hola"))           # ola
print(g2p_es.phonemize("Buenos días"))    # buenos diˈas
print(g2p_es.phonemize("¿Cómo estás?"))   # ?koˈmo estaˈs?

# R trill vs tap distinction
print(g2p_es.phonemize("perro"))  # pero (trill)
print(g2p_es.phonemize("pero"))   # peɾo (tap)

# Theta sound (European)
print(g2p_es.phonemize("zapato"))  # θapato
print(g2p_es.phonemize("cielo"))   # θielo

# Palatals
print(g2p_es.phonemize("niño"))    # niɲo
print(g2p_es.phonemize("llamar"))  # ʎamaɾ
print(g2p_es.phonemize("chico"))   # ʧiko

# Latin American Spanish (seseo, θ → s)
g2p_la = SpanishG2P(dialect="la", mark_stress=True)
print(g2p_la.phonemize("zapato"))  # sapato (not θapato)
print(g2p_la.phonemize("cielo"))   # sielo (not θielo)

# Disable stress markers
g2p_nostress = SpanishG2P(mark_stress=False)
print(g2p_nostress.phonemize("café"))  # kafe (not kafeˈ)
```

## Validation

Validate the dataset:

```bash
python benchmarks/validate_synthetic_data.py benchmarks/data/es_synthetic.json
```

Expected output:

```
✓ VALID - All checks passed!
Phoneme Coverage: 86.2% (25/29 phonemes)
100 sentences across 10 categories
```

## Dataset Files

- **benchmarks/data/es_synthetic.json** - 100 hand-crafted Spanish sentences with
  phoneme annotations
- **benchmarks/benchmark_es_comparison.py** - Benchmark script comparing configurations
- **kokorog2p/es/g2p.py** - Spanish G2P implementation
- **kokorog2p/phonemes.py** - ES_VOCAB definition (30 phonemes)

## Contributing

To extend the dataset:

1. Add new sentences to `es_synthetic.json`
2. Ensure phoneme annotations match the vocabulary
3. Run validation:
   `python benchmarks/validate_synthetic_data.py benchmarks/data/es_synthetic.json`
4. Run benchmark: `python benchmarks/benchmark_es_comparison.py`
5. Aim for 100% accuracy on European Spanish configuration

## References

- **Spanish Phonology**:
  [Wikipedia - Spanish phonology](https://en.wikipedia.org/wiki/Spanish_phonology)
- **IPA for Spanish**:
  [Wikipedia - Help:IPA/Spanish](https://en.wikipedia.org/wiki/Help:IPA/Spanish)
- **R sounds in Spanish**: Distinction between trill [r] and tap [ɾ] is phonemic
- **European vs Latin American**: Main difference is theta-distinction (θ/s) vs seseo (s
  only)
