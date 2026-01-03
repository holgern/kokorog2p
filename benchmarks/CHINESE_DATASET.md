# Chinese (Mandarin) Synthetic Benchmark Dataset

## Overview

The Chinese benchmark script is located at:

- **benchmarks/benchmark_zh_comparison.py**

This script tests Chinese (Mandarin) G2P configurations and measures accuracy and speed.

## Quick Start

```bash
# Run all configurations
python benchmarks/benchmark_zh_comparison.py

# Test specific configuration
python benchmarks/benchmark_zh_comparison.py --config "Chinese G2P + Espeak"

# Verbose output
python benchmarks/benchmark_zh_comparison.py --verbose

# Export results
python benchmarks/benchmark_zh_comparison.py --output results.json
```

## Benchmark Results (110 sentences, 164 characters)

| Configuration            | Accuracy | Speed      | Recommendation        |
| ------------------------ | -------- | ---------- | --------------------- |
| Chinese G2P + Espeak     | 100.0%   | 108 sent/s | ✅ **Best** (fastest) |
| Chinese G2P (ZHFrontend) | 100.0%   | 29 sent/s  | Good default          |

**Recommendation**: Use **Chinese G2P + Espeak** configuration for best speed while
maintaining 100% accuracy. The espeak fallback improves performance significantly
without sacrificing accuracy.

## Dataset Composition

The dataset consists of **110 hand-crafted sentences** covering:

### Greetings & Polite Phrases (8 sentences)

- 你好 (Hello)
- 谢谢 (Thank you)
- 再见 (Goodbye)
- 早上好 (Good morning)
- 晚安 (Good night)
- 对不起 (Sorry)
- 没关系 (It's okay)
- 不客气 (You're welcome)

### Common Words (17 sentences)

- 爱, 家, 朋友, 工作, 学习 (Love, Home, Friend, Work, Study)
- 时间, 名字, 世界 (Time, Name, World)
- 中国, 北京, 上海 (China, Beijing, Shanghai)
- 我爱你, 很高兴 (I love you, Very happy)
- 好吃, 好看, 漂亮, 美丽 (Delicious, Pretty, Beautiful)

### Numbers (14 sentences)

- Individual digits: 一二三四五六七八九十 (1-10)
- Large numbers: 百千万 (100, 1000, 10000)
- Sequences: 一二三 (one two three)

### Food & Daily Items (9 sentences)

- 饭, 茶, 水, 面 (Rice, Tea, Water, Noodles)
- 肉, 鱼, 菜, 果 (Meat, Fish, Vegetables, Fruit)

### Questions (8 sentences)

- 什么, 为什么, 怎么 (What, Why, How)
- 哪里, 谁, 哪个 (Where, Who, Which)
- 你叫什么名字 (What is your name?)
- 这是什么 (What is this?)

### Phoneme Coverage - Initials (21 sentences)

Testing all 21 Zhuyin initials (consonants):

- ㄅㄆㄇㄈ (b p m f)
- ㄉㄊㄋㄌ (d t n l)
- ㄍㄎㄏ (g k h)
- ㄐㄑㄒ (j q x)
- ㄓㄔㄕㄖ (zh ch sh r)
- ㄗㄘㄙ (z c s)

### Phoneme Coverage - Finals (15 sentences)

Testing all 16 basic Zhuyin finals (vowels/diphthongs):

- ㄚㄛㄜㄝ (a o e ê)
- ㄞㄟㄠㄡ (ai ei ao ou)
- ㄢㄣㄤㄥ (an en ang eng)
- ㄦㄧㄨㄩ (er i u ü)

### Tone Coverage (5 sentences)

Testing all 5 Mandarin tones with the same syllable:

- 妈 (1st tone - high level)
- 麻 (2nd tone - rising)
- 马 (3rd tone - dipping)
- 骂 (4th tone - falling)
- 吗 (5th tone - neutral)

### Complex Phonemes (13 sentences)

Testing complex syllables, compound finals, and special cases:

- Complex finals: 光, 窗, 双, 想 (uang, iang)
- Erhua (儿化音): 花儿, 玩儿 (flower-r, play-r)
- Compound words: 聪明, 快乐, 幸福, 健康

**Total**: 110 sentences with 164 Chinese characters

## Phoneme Coverage

The dataset achieves **100% coverage** of all 59 Chinese phoneme characters:

```
/ 1 2 3 4 5 R ㄅ ㄆ ㄇ ㄈ ㄉ ㄊ ㄋ ㄌ ㄍ ㄎ ㄏ ㄐ ㄑ ㄒ ㄓ ㄔ ㄕ ㄖ ㄗ ㄘ ㄙ
ㄚ ㄜ ㄝ ㄞ ㄟ ㄠ ㄡ ㄢ ㄣ ㄤ ㄥ ㄦ ㄧ ㄨ ㄩ ㄭ 万 中 为 十 压 又 外 应 我 月 王 穵 要 言 阳
```

### Character-Based Phoneme System

**Important**: Like Japanese and Korean, Chinese phonemes are **character-based** using
**Zhuyin (Bopomofo) notation**. Each character in the phoneme string represents a single
phoneme component (not space-separated by word).

**Example**:

- Text: `你好`
- Phonemes: `ㄋㄧ2ㄏㄠ3` (6 characters)
  - ㄋ (initial n) + ㄧ (final i) + 2 (3rd tone, changed by tone sandhi)
  - ㄏ (initial h) + ㄠ (final ao) + 3 (3rd tone)

### What is Zhuyin (Bopomofo)?

**Zhuyin** (注音符號), also called **Bopomofo** (ㄅㄆㄇㄈ), is a traditional phonetic
notation system for Mandarin Chinese:

- Used primarily in Taiwan for education
- Pre-dates Pinyin (Wade-Giles romanization)
- Each symbol represents a sound component
- **NOT IPA** - uses unique Chinese symbols

**Why Zhuyin instead of IPA?**

- This is what Kokoro TTS uses internally
- More accurate for Chinese phonology
- Includes tone markers naturally
- Standard for Traditional Chinese education

### Zhuyin Components

#### 1. Initials (聲母) - 21 symbols

The consonant sounds at the start of syllables:

**Labials (唇音):**

- **ㄅ** (b) - 爸 bà
- **ㄆ** (p) - 怕 pà
- **ㄇ** (m) - 妈 mā
- **ㄈ** (f) - 发 fā

**Alveolars (舌尖音):**

- **ㄉ** (d) - 大 dà
- **ㄊ** (t) - 他 tā
- **ㄋ** (n) - 那 nà
- **ㄌ** (l) - 拉 lā

**Velars (舌根音):**

- **ㄍ** (g) - 个 gè
- **ㄎ** (k) - 可 kě
- **ㄏ** (h) - 河 hé

**Palatals (舌面音):**

- **ㄐ** (j) - 姐 jiě
- **ㄑ** (q) - 去 qù
- **ㄒ** (x) - 西 xī

**Retroflexes (卷舌音):**

- **ㄓ** (zh) - 知 zhī → 十 in phoneme string
- **ㄔ** (ch) - 吃 chī
- **ㄕ** (sh) - 是 shì
- **ㄖ** (r) - 日 rì

**Dentals (舌尖前音):**

- **ㄗ** (z) - 字 zì → ㄭ after z/c/s
- **ㄘ** (c) - 次 cì
- **ㄙ** (s) - 思 sī

#### 2. Finals (韻母) - 16 basic + special finals

The vowel/diphthong sounds:

**Simple Finals:**

- **ㄚ** (a) - 啊 ā
- **ㄛ** (o) - rarely used alone
- **ㄜ** (e) - 哥 gē
- **ㄝ** (ê) - 姐 jiě
- **ㄞ** (ai) - 白 bái
- **ㄟ** (ei) - 飞 fēi
- **ㄠ** (ao) - 高 gāo
- **ㄡ** (ou) - 走 zǒu

**Nasal Finals:**

- **ㄢ** (an) - 安 ān
- **ㄣ** (en) - 人 rén
- **ㄤ** (ang) - 房 fáng
- **ㄥ** (eng) - 风 fēng

**Medials/Special:**

- **ㄦ** (er) - 儿 ér
- **ㄧ** (i) - 衣 yī
- **ㄨ** (u) - 乌 wū
- **ㄩ** (ü) - 鱼 yú

#### 3. Special Finals (Compound Characters)

These appear as Chinese characters in the phoneme string and represent specific sound
combinations:

- **十** (iii) - After zh/ch/sh/r: 知 zhī, 吃 chī, 是 shì
- **ㄭ** (ii) - After z/c/s: 字 zì, 次 cì, 思 sī
- **月** (ve/üe) - After j/q/x: 学 xué
- **万** (wan) - 晚 wǎn, 玩 wán
- **中** (ong) - 中 zhōng, 工 gōng
- **为** (wei) - 为 wèi, 水 shuǐ
- **我** (uo) - 我 wǒ, 果 guǒ
- **压** (ia) - 家 jiā
- **又** (you) - 朋友 péng you
- **外** (wai) - 快 kuài
- **应** (ing) - 应 yīng, 名 míng
- **王** (uang) - 光 guāng, 窗 chuāng
- **穵** (uar) - 花儿 huār (with erhua)
- **要** (iao) - 漂亮 piào liang
- **言** (ian) - 见 jiàn, 时间 shí jiān
- **阳** (iang) - 想 xiǎng, 漂亮 piào liang
- **R** - Erhua marker: 玩儿 wánr

#### 4. Tone Markers (聲調) - 5 tones

Mandarin has 4 main tones plus a neutral tone:

- **1** - First tone (high level): 妈 mā (mother) - flat high pitch
- **2** - Second tone (rising): 麻 má (hemp) - rises like a question
- **3** - Third tone (dipping): 马 mǎ (horse) - falls then rises
- **4** - Fourth tone (falling): 骂 mà (scold) - sharp falling pitch
- **5** - Fifth tone (neutral): 吗 ma (question particle) - light/unstressed

#### 5. Special Markers

- **/** - Word boundary/pause marker (optional)
- Appears in some compound words: 很高兴 → ㄏㄣ 3/ㄍㄠ 1 ㄒ应 4

### Special Phonological Features

#### Tone Sandhi (变调)

Tones can change in context:

- **Third tone before third tone** becomes second tone:
  - 你好 nǐ hǎo → ni2 hao3 (both 3rd → first changes to 2nd)
  - Phonemes: `ㄋㄧ2ㄏㄠ3`
- **不 (bù)** and **一 (yī)** have special sandhi rules

#### Erhua (儿化音)

Adding 儿 (er) suffix merges with previous syllable:

- 花儿 huār (flower) → ㄏ穵 1 ㄦ 2
- 玩儿 wánr (play) → 万 R2
- Creates special phonetic combinations

#### Syllable Structure

Chinese syllables follow the pattern:

```
[Initial] + [Final] + [Tone]
```

Examples:

- 妈 (mā): ㄇ (m) + ㄚ (a) + 1 (high tone) = ㄇㄚ 1
- 中 (zhōng): ㄓ (zh) + 中 (ong) + 1 (high tone) = ㄓ中 1
- 学 (xué): ㄒ (x) + 月 (üe) + 2 (rising tone) = ㄒ月 2

## Data Generation

### Source

All sentences are **hand-crafted** to ensure:

1. Complete phoneme coverage
2. Common vocabulary and phrases
3. All tone combinations
4. Phonetic diversity
5. Natural language patterns

### Generation Process

```bash
# Generate Chinese synthetic data (already created)
python benchmarks/generate_zh_synthetic.py

# Add metadata
python benchmarks/add_zh_metadata.py

# Validate
python benchmarks/validate_synthetic_data.py benchmarks/data/zh_synthetic.json

# Regenerate phonemes (if needed)
python benchmarks/regenerate_phonemes.py benchmarks/data/zh_synthetic.json
```

## Validation

To validate the dataset:

```bash
python benchmarks/validate_synthetic_data.py benchmarks/data/zh_synthetic.json
```

Expected output:

- ✓ VALID - All checks passed!
- Phoneme Coverage: 100.0% (59/59)
- Total sentences: 110

## Files

### Main Files

- **benchmarks/data/zh_synthetic.json** - Complete Chinese benchmark dataset
- **benchmarks/benchmark_zh_comparison.py** - Benchmark comparison script
- **benchmarks/generate_zh_synthetic.py** - Dataset generation script
- **benchmarks/add_zh_metadata.py** - Metadata addition utility

### Supporting Files

- **kokorog2p/zh/g2p.py** - Main ChineseG2P class
- **kokorog2p/zh/frontend.py** - ZHFrontend with Zhuyin mapping
- **kokorog2p/zh/tone_sandhi.py** - Tone sandhi rules
- **kokorog2p/zh/transcription.py** - Pinyin to IPA conversion (alternative)
- **kokorog2p/phonemes.py** - ZH_VOCAB definition (59 characters)

## References

### Zhuyin (Bopomofo)

- [Wikipedia - Bopomofo](https://en.wikipedia.org/wiki/Bopomofo)
- Standard phonetic notation for Mandarin Chinese
- Used in Taiwan education system
- Pre-dates Pinyin romanization

### Mandarin Phonology

- [Wikipedia - Standard Chinese Phonology](https://en.wikipedia.org/wiki/Standard_Chinese_phonology)
- 21 initials (consonants)
- 16 basic finals (vowels/diphthongs)
- 4 tones + neutral tone
- Tone sandhi and erhua variations

### Tools Used

- **pypinyin** - Pinyin extraction and conversion
- **jieba** - Chinese word segmentation
- **ZHFrontend** - Zhuyin notation conversion (kokorog2p)

## Future Work

### Potential Enhancements

1. **CHILDES Integration** - Add natural speech samples from CHILDES zh-CN corpus
2. **Regional Variations** - Test Taiwanese vs Mainland pronunciation differences
3. **IPA Conversion** - Add alternative IPA-based phoneme representation
4. **Rare Characters** - Extend coverage to literary Chinese and rare phonemes
5. **Dialect Support** - Add Cantonese (粵語) or other Chinese dialects

### Known Limitations

1. Only covers Standard Mandarin (Putonghua/國語)
2. Does not include regional accents
3. Hand-crafted dataset (no real speech samples yet)
4. Zhuyin notation may be unfamiliar to non-Chinese speakers

## Usage Examples

### Basic Usage

```python
from kokorog2p.zh import ChineseG2P

g2p = ChineseG2P(use_espeak_fallback=True, version="1.1")

# Simple greeting
tokens = g2p("你好")
print([t.phonemes for t in tokens])  # ['ㄋㄧ2ㄏㄠ3']

# With tone sandhi
tokens = g2p("我爱你")
print([t.phonemes for t in tokens])  # ['我3ㄞ4ㄋㄧ3']

# Complex sentence
tokens = g2p("很高兴认识你")
phonemes = "".join(t.phonemes for t in tokens)
print(phonemes)  # ㄏㄣ3/ㄍㄠ1ㄒ应4ㄖㄣ4ㄕ十5ㄋㄧ3
```

### Benchmark Usage

```python
import json
from pathlib import Path

# Load dataset
with open("benchmarks/data/zh_synthetic.json") as f:
    data = json.load(f)

# Test on specific sentence
sentence = data["sentences"][0]
print(f"Text: {sentence['text']}")
print(f"Phonemes: {sentence['phonemes']}")
print(f"Category: {sentence['category']}")
```

## Conclusion

The Chinese synthetic benchmark dataset provides:

- ✅ 100% phoneme coverage (59 Zhuyin characters)
- ✅ 110 hand-crafted sentences
- ✅ 100% accuracy with kokorog2p
- ✅ All tone combinations
- ✅ Comprehensive validation
- ✅ Fast processing (108 sent/s with espeak)

This dataset serves as a robust foundation for testing and validating Chinese Mandarin
G2P systems using Zhuyin (Bopomofo) phonetic notation.
