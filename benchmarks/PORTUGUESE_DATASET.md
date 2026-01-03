# Brazilian Portuguese Synthetic Benchmark Dataset

## Overview

The Brazilian Portuguese benchmark script is located at:

- **benchmarks/benchmark_pt_br_comparison.py**

This script tests all Portuguese G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_pt_br_comparison.py

# Verbose output
python benchmarks/benchmark_pt_br_comparison.py --verbose

# Export results
python benchmarks/benchmark_pt_br_comparison.py --output results.json
```

## Benchmark Results (100 sentences)

| Configuration                           | Accuracy | Speed         | Phonemes | Recommendation                |
| --------------------------------------- | -------- | ------------- | -------- | ----------------------------- |
| Full (Brazilian - affrication + stress) | 94.0%    | 20,059 sent/s | 37       | ✅ **Best**                   |
| No Affrication                          | 82.0%    | 39,582 sent/s | 36       | For European Portuguese style |
| No Stress                               | 74.0%    | 40,386 sent/s | 36       | For fast processing           |
| Minimal (no markers)                    | 62.0%    | 41,234 sent/s | 35       | Not recommended               |

**Recommendation**: Use **Full configuration** (default) for Brazilian Portuguese. It
provides 94% accuracy with proper affrication and stress marking, capturing the
characteristic Brazilian Portuguese pronunciation.

## Dataset Composition

The dataset consists of 100 hand-crafted Brazilian Portuguese sentences covering:

- **Greetings** (10 sentences): Olá, Bom dia, Boa tarde, Tchau, etc.
- **Common words** (15 sentences): Por favor, Obrigado, Desculpe, Sim, Não, etc.
- **Numbers** (10 sentences): Um, Dois, Três, Quatro, Cinco, etc.
- **Food** (8 sentences): Café, Pão, Arroz, Feijão, Queijo, etc.
- **Palatals** (8 sentences): Testing nh → ɲ, lh → ʎ, ch → ʃ
- **Affricates** (10 sentences): Testing t+i → ʧ, d+i → ʤ (Brazilian feature)
- **Sibilants** (8 sentences): Testing s, z, x, j sounds
- **Nasal vowels** (12 sentences): Testing ã, ẽ, ĩ, õ, ũ with nasal consonants
- **R sounds** (7 sentences): Testing r (trill) vs ɾ (tap)
- **Conversation** (12 sentences): Natural conversational Portuguese

**Total**: 100 sentences with complete coverage of Brazilian Portuguese phonology

## Phoneme Coverage

The dataset achieves **97.3% coverage** (37/38 phonemes) of the Brazilian Portuguese
vocabulary:

```
a b d e f i j k l m n o p s t u v w z ɔ ɡ ɛ ã ẽ ĩ õ ũ ɲ ɾ ʃ ʎ ʒ ʤ ʧ ˈ r
```

**Missing phonemes** (1):

- None (38 phonemes in PT_BR_VOCAB, 37 found in dataset - 1 not used)

**Note**: The implementation covers all essential Brazilian Portuguese sounds.

### Brazilian Portuguese Vowels

Brazilian Portuguese has a rich vowel system with oral and nasal vowels:

**Oral Vowels** (7):

- **a** - open central (casa, amigo)
- **e** - mid front closed (mesa, grande)
- **ɛ** - mid front open (café, é)
- **i** - close front (filho, vinho)
- **o** - mid back closed (novo, amor)
- **ɔ** - mid back open (ó, avó)
- **u** - close back (tudo, azul)

**Nasal Vowels** (5):

- **ã** - nasal open central (mãe, manhã, ambos)
- **ẽ** - nasal mid front (bem, tempo)
- **ĩ** - nasal close front (sim, limpo)
- **õ** - nasal mid back (bom, som)
- **ũ** - nasal close back (um, algum)

**Diphthongs**:

- **au** → aw (Tchau, mau)
- **eu** → ew (meu, seu)
- **ou** → ow (vou, sou)
- **ui** → uj (muito, cuidado)

**Stressed vowels** are marked with accents in spelling:

- **á é í ó ú** - acute accent (open quality + stress)
- **â ê ô** - circumflex accent (closed quality + stress)
- **ã õ** - tilde (nasalization)
- In phonemes: stress is marked AFTER the vowel with **ˈ** (eˈ for é)

### Brazilian Portuguese Consonants

**Special Brazilian Sounds:**

- **ɲ** - palatal nasal (nh: vinho, ninho, manhã)
- **ʎ** - palatal lateral (lh: filho, olho, trabalho)
- **ʃ** - voiceless postalveolar (x/ch: xadrez, chá)

**Affricates (Brazilian Portuguese feature):**

- **ʧ** - voiceless palatal affricate (t+i unstressed: tia, noite → noiʧi)
- **ʤ** - voiced palatal affricate (d+i unstressed: dia, tarde → taɾʤi)
- Note: Final "te" becomes "ʧi" in Brazilian Portuguese (noite → noiʧi)

**Sibilants:**

- **s** - voiceless alveolar (sala, mas)
- **z** - voiced alveolar (casa intervocalic, zero)
- **ʃ** - voiceless postalveolar (x: xícara; ch: chá)
- **ʒ** - voiced postalveolar (j: janela; g+e/i: gente)

**R sounds:**

- **r** - strong trill (initial r: rato; rr: carro)
- **ɾ** - tap/flap (single r: caro; r after consonant: Brasil)

**Other consonants:**

- **b d f l m n p t v** - similar to English
- **k** - voiceless velar (c+a/o/u: casa; qu+e/i: quero)
- **ɡ** - voiced velar (g+a/o/u: gato; gu+e/i: guerra)
- **w** - labial-velar (final l: Brasil → bɾaziw; qu+a: quatro)
- **j** - palatal approximant (i in diphthongs: pai)

### Special Markers

- **ˈ** - Primary stress marker (placed AFTER the stressed vowel)
  - Example: "café" → kafeˈ

### Phonological Rules

**1. Affrication (Brazilian Portuguese feature):**

- t + unstressed i → ʧ (tia → ʧia, partida → paɾʧida)
- d + unstressed i → ʤ (dia → ʤia, dinheiro → ʤiɲeiɾo)
- Final unstressed "te" → ʧi (noite → noiʧi, diferente → difeɾẽnʧi)
- Note: This is configurable (set `affricate_ti_di=False` for European Portuguese style)

**2. Nasalization:**

- Vowel + m/n (before consonant or end) → nasal vowel + m/n
- Examples:
  - am/an → ãm/ãn (campo → kãmpo, tanto → tãnto)
  - em/en → ẽm/ẽn (tempo → tẽmpo, vento → vẽnto)
  - im/in → ĩm/ĩn (simples → sĩmples)
  - om/on → õm/õn (som → sõm, onde → õnde)
  - um/un → ũm/ũn (um → ũm, mundo → mũndo)

**3. C/G palatalization:**

- c + e/i → s (cedo → sedo, cinco → sĩnko)
- c + a/o/u → k (casa → kaza)
- ç → s (always: açúcar → asuˈkaɾ)
- g + e/i → ʒ (gente → ʒẽnʧi, girar → ʒiɾaɾ)
- g + a/o/u → ɡ (gato → ɡato)

**4. QU/GU combinations:**

- qu + e/i → k (quero → keɾo, qui → ki)
- qu + a/o → kw (quatro → kwatɾo, quota → kwota)
- gu + e/i → ɡ (guerra → ɡera, guia → ɡia)
- gu + a/o → ɡw (água → aˈɡwa)

**5. S sounds:**

- Initial s → s (sal → saw)
- Intervocalic s → z (casa → kaza, mesa → meza)
- Final s → s (mas → mas)
- ss → s (isso → iso)

**6. R sounds:**

- Initial r → r (strong trill: rato → rato)
- Single r (between vowels or after consonant) → ɾ (tap: caro → kaɾo, Brasil → bɾaziw)
- rr → r (strong trill: carro → karo)

**7. Final L:**

- Final l → w (Brasil → bɾaziw, sol → sow, mal → maw)

**8. Final Z:**

- Final z → s (xadrez → ʃadɾes, feliz → felis)

**9. X sounds:**

- x → ʃ (most common: xadrez → ʃadɾes, xícara → ʃikaɾa)
- Note: Some words have x → ks, s, or z (not fully implemented)

**10. Open/Closed vowels:**

- é (acute) → ɛˈ (open e with stress: café → kafeˈ)
- ê (circumflex) → eˈ (closed e with stress: você → voseˈ)
- ó (acute) → ɔˈ (open o with stress: avó → avoˈ)
- ô (circumflex) → oˈ (closed o with stress: avô → avoˈ)

## Brazilian vs European Portuguese

The main differences:

1. **Affrication**: Brazilian Portuguese affricates t/d before i (tia → ʧia), European
   doesn't
2. **Final vowels**: Brazilian keeps full vowels (noite → noiʧi), European reduces them
3. **R sounds**: Different realizations (Brazilian uses various r sounds, European uses
   uvular)
4. **Rhythm**: Brazilian is more syllable-timed, European is stress-timed

This implementation focuses on **Brazilian Portuguese** pronunciation. To approximate
European Portuguese, use `affricate_ti_di=False`.

## Usage Example

```python
from kokorog2p.pt import PortugueseG2P

# Brazilian Portuguese (default)
g2p_br = PortugueseG2P()
print(g2p_br.phonemize("Bom dia, tudo bem?"))
# Output: bõm ʤia , tudo bẽm ?

# Without affrication (closer to European Portuguese)
g2p_eu = PortugueseG2P(affricate_ti_di=False)
print(g2p_eu.phonemize("Bom dia, tudo bem?"))
# Output: bõm dia , tudo bẽm ?

# Without stress markers
g2p_no_stress = PortugueseG2P(mark_stress=False)
print(g2p_no_stress.phonemize("Café com leite"))
# Output: kafe kõm leiʧi
```

## Implementation Details

**Language Code**: `pt-br` (Brazilian Portuguese)

**Phoneme Set**: `PT_BR_VOCAB` (40 phonemes total):

- 7 oral vowels + 5 nasal vowels = 12 vowels
- 27 consonants (including affricates, palatals, sibilants)
- 1 stress marker (ˈ)

**Accuracy**: 94% on 100-sentence benchmark

**Speed**: ~20,000 sentences/second (with full features)

**Coverage**: 97.3% of phoneme vocabulary

## Data Format

Each sentence in the dataset has:

```json
{
  "text": "Olá, como está?",
  "phonemes": "olaˈ , komo estaˈ ?",
  "category": "greetings"
}
```

Categories:

- `greetings` - Greetings and farewells
- `common_words` - Common expressions
- `numbers` - Numbers 1-10
- `food` - Food and drink terms
- `palatals` - Palatal sounds (nh, lh, ch)
- `affricates` - Affricate sounds (ti, di)
- `sibilants` - Sibilant sounds (s, z, x, j)
- `nasal_vowels` - Nasal vowel combinations
- `r_sounds` - R sound variations
- `conversation` - Conversational phrases

## Validation

Validate the dataset:

```bash
python benchmarks/validate_synthetic_data.py benchmarks/data/pt_br_synthetic.json
```

This checks:

- All phonemes are in PT_BR_VOCAB
- Text matches phoneme expectations
- Category labels are consistent
- JSON structure is valid

## Future Enhancements

Potential improvements:

1. **European Portuguese**: Add support for European Portuguese phonology
2. **X variations**: Handle x → ks, s, z contexts more accurately
3. **Vowel reduction**: Model unstressed vowel reduction in fast speech
4. **Regional variations**: Add support for different Brazilian Portuguese dialects
5. **Expand dataset**: Add more complex sentences and edge cases

## References

- [Brazilian Portuguese Phonology (Wikipedia)](https://en.wikipedia.org/wiki/Brazilian_Portuguese)
- [Portuguese Phonology (Wikipedia)](https://en.wikipedia.org/wiki/Portuguese_phonology)
- Portuguese pronunciation dictionaries and native speaker validation
