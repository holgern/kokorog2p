Language Support
================

kokorog2p supports multiple languages with varying levels of functionality.

.. list-table:: Language Support Overview
   :header-rows: 1
   :widths: 15 15 20 20 30

   * - Language
     - Code
     - Dictionary
     - Fallback
     - Special Features
   * - English (US)
     - en-us
     - 100k+ entries
     - espeak-ng
     - POS tagging, stress, numbers
   * - English (GB)
     - en-gb
     - 100k+ entries
     - espeak-ng
     - POS tagging, stress, numbers
   * - German
     - de
     - 738k+ entries
     - espeak-ng
     - Phonological rules, numbers
   * - French
     - fr
     - Gold dictionary
     - espeak-ng
     - Numbers, liaison rules
   * - Czech
     - cs
     - Rule-based
     - —
     - Phonological rules
   * - Chinese
     - zh
     - —
     - pypinyin
     - Tone sandhi, pinyin
   * - Japanese
     - ja
     - —
     - pyopenjtalk
     - Mora-based, pitch accent

English (en-us, en-gb)
----------------------

English G2P uses a two-tier dictionary system with spaCy for POS tagging.

Features
~~~~~~~~

* **Gold dictionary**: 50k+ high-confidence entries
* **Silver dictionary**: Additional 50k+ entries
* **POS-aware pronunciation**: Different pronunciations based on part of speech
* **Stress assignment**: Primary and secondary stress markers
* **Number handling**: Cardinals, ordinals, currency
* **Contraction support**: Proper handling of "can't", "won't", etc.

Usage
~~~~~

.. code-block:: python

   from kokorog2p.en import EnglishG2P

   # US English
   g2p_us = EnglishG2P(
       language="en-us",
       use_espeak_fallback=True,
       use_spacy=True
   )

   # British English
   g2p_gb = EnglishG2P(
       language="en-gb",
       use_espeak_fallback=True,
       use_spacy=True
   )

Examples
~~~~~~~~

.. code-block:: python

   from kokorog2p import phonemize

   # Context-dependent pronunciation
   print(phonemize("I read a book.", language="en-us"))
   # → ˈaɪ ɹˈɛd ə bˈʊk.

   print(phonemize("I will read tomorrow.", language="en-us"))
   # → ˈaɪ wɪl ɹˈid təmˈɑɹO.

   # Numbers and currency
   print(phonemize("I paid $1,234.56 for it.", language="en-us"))
   # → aɪ pˈeɪd wʌn θˈaʊzənd tˈu hˈʌndɹəd...

German (de)
-----------

German G2P uses a large dictionary (738k+ entries from Olaph) with rule-based fallback.

Features
~~~~~~~~

* **Large dictionary**: 738k+ entries with stress markers
* **Phonological rules**:

  - Final obstruent devoicing (Auslautverhärtung)
  - ich-Laut [ç] vs ach-Laut [x] alternation
  - Word-initial sp/st → [ʃp]/[ʃt]
  - Vowel length rules
  - Schwa in unstressed syllables

* **Number handling**: Cardinals, ordinals, years, currency
* **Regional variants**: de-de, de-at, de-ch

Usage
~~~~~

.. code-block:: python

   from kokorog2p.de import GermanG2P

   g2p = GermanG2P(
       language="de-de",
       use_espeak_fallback=True,
       strip_stress=True
   )

Examples
~~~~~~~~

.. code-block:: python

   from kokorog2p import phonemize

   # Basic phonemization
   print(phonemize("Guten Tag", language="de"))
   # → ɡuːtn̩ taːk

   # Phonological rules
   print(phonemize("ich", language="de"))      # → ɪç (ich-Laut)
   print(phonemize("ach", language="de"))      # → ax (ach-Laut)
   print(phonemize("Tag", language="de"))      # → taːk (final devoicing)

   # Numbers
   print(phonemize("Ich habe 42 Euro.", language="de"))
   # → ɪç haːbə t͡svaɪ̯ʊntfɪɐ̯t͡sɪç ɔɪ̯ʁo.

French (fr)
-----------

French G2P uses a gold dictionary with espeak-ng fallback.

Features
~~~~~~~~

* **Gold dictionary**: High-quality French pronunciations
* **Number handling**: Cardinals, ordinals, currency
* **espeak-ng fallback**: For out-of-vocabulary words

Usage
~~~~~

.. code-block:: python

   from kokorog2p.fr import FrenchG2P

   g2p = FrenchG2P(
       language="fr-fr",
       use_espeak_fallback=True
   )

Examples
~~~~~~~~

.. code-block:: python

   from kokorog2p import phonemize

   print(phonemize("Bonjour le monde", language="fr"))
   # → bɔ̃ʒuʁ lə mɔ̃d

   print(phonemize("J'ai vingt et un ans.", language="fr"))
   # → ʒɛ vɛ̃t e œ̃ ɑ̃.

Czech (cs)
----------

Czech G2P is entirely rule-based with comprehensive phonological rules.

Features
~~~~~~~~

* **Rule-based phonology**:

  - Palatalization (d+i → ɟ, t+i → c, n+i → ɲ)
  - Long vowels (á → aː, í → iː, etc.)
  - ř phoneme [r̝]
  - ch digraph → [x]
  - Final devoicing
  - Voicing assimilation

* **No dictionary required**: Works with any Czech text

Usage
~~~~~

.. code-block:: python

   from kokorog2p.cs import CzechG2P

   g2p = CzechG2P(language="cs-cz")

Examples
~~~~~~~~

.. code-block:: python

   from kokorog2p import phonemize

   print(phonemize("Dobrý den", language="cs"))
   # → dobriː dɛn

   print(phonemize("Praha", language="cs"))
   # → praɦa

   # Palatalization
   print(phonemize("děti", language="cs"))
   # → ɟɛcɪ

   # ř phoneme
   print(phonemize("řeka", language="cs"))
   # → r̝ɛka

Chinese (zh)
------------

Chinese G2P uses jieba for tokenization and pypinyin for phoneme conversion.

Features
~~~~~~~~

* **Jieba tokenization**: Chinese word segmentation
* **Pypinyin conversion**: Pinyin to IPA
* **Tone sandhi**: Automatic tone changes
* **cn2an**: Number to Chinese conversion
* **Punctuation mapping**: Chinese to Western punctuation

Usage
~~~~~

.. code-block:: python

   from kokorog2p.zh import ChineseG2P

   g2p = ChineseG2P(
       language="zh",
       version="1.1"
   )

Examples
~~~~~~~~

.. code-block:: python

   from kokorog2p import phonemize

   print(phonemize("你好世界", language="zh"))
   # → nǐ hǎo shì jiè (with tone markers)

Japanese (ja)
-------------

Japanese G2P uses pyopenjtalk for text analysis and mora-based phoneme generation.

Features
~~~~~~~~

* **pyopenjtalk**: Full Japanese text analysis
* **Mora-based**: Phonemes aligned with mora structure
* **Pitch accent**: Automatic pitch accent assignment
* **Number handling**: Japanese numerals

Usage
~~~~~

.. code-block:: python

   from kokorog2p.ja import JapaneseG2P

   g2p = JapaneseG2P(
       language="ja",
       version="pyopenjtalk"
   )

Examples
~~~~~~~~

.. code-block:: python

   from kokorog2p import phonemize

   print(phonemize("こんにちは", language="ja"))
   # → koɴɲit͡ɕiha

   print(phonemize("世界", language="ja"))
   # → sekai

Language-Specific Number Handling
----------------------------------

English
~~~~~~~

.. code-block:: python

   from kokorog2p.en.numbers import expand_number

   print(expand_number("I have $42.50"))
   # → I have forty-two dollars and fifty cents

German
~~~~~~

.. code-block:: python

   from kokorog2p.de.numbers import expand_number

   print(expand_number("Ich habe 42 Euro."))
   # → Ich habe zweiundvierzig Euro.

French
~~~~~~

.. code-block:: python

   from kokorog2p.fr.numbers import expand_number

   print(expand_number("J'ai 42 euros."))
   # → J'ai quarante-deux euros.

Fallback Languages
------------------

For languages not explicitly supported, kokorog2p falls back to espeak-ng:

.. code-block:: python

   from kokorog2p import get_g2p

   # Spanish (uses espeak-ng)
   g2p_es = get_g2p("es-es")

   # Italian (uses espeak-ng)
   g2p_it = get_g2p("it-it")

   # Portuguese (uses espeak-ng)
   g2p_pt = get_g2p("pt-br")

This provides basic support for 100+ languages via espeak-ng.

Next Steps
----------

* See :doc:`advanced` for advanced usage patterns
* Check language-specific API docs:

  - :doc:`api/english`
  - :doc:`api/german`
  - :doc:`api/french`
  - :doc:`api/czech`
  - :doc:`api/chinese`
  - :doc:`api/japanese`
