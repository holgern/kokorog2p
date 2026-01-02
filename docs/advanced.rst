Advanced Usage
==============

This guide covers advanced features and usage patterns for kokorog2p.

Custom G2P Configuration
------------------------

Memory-Efficient Loading
~~~~~~~~~~~~~~~~~~~~~~~~

Control dictionary loading to optimize memory and initialization time:

.. code-block:: python

   from kokorog2p import get_g2p

   # Default: Gold + Silver dictionaries (~365k entries, ~57 MB)
   # Provides maximum vocabulary coverage
   g2p = get_g2p("en-us")
   
   # Memory-optimized: Gold dictionary only (~179k entries, ~35 MB)
   # Saves ~22-31 MB memory and ~400-470 ms initialization time
   g2p_fast = get_g2p("en-us", load_silver=False)
   
   # Ultra-fast initialization: No dictionaries (~7 MB, espeak fallback only)
   # Saves ~50+ MB memory, fastest initialization
   g2p_minimal = get_g2p("en-us", load_silver=False, load_gold=False)
   
   # Check dictionary size
   print(f"Gold entries: {len(g2p.lexicon.golds):,}")
   print(f"Silver entries: {len(g2p.lexicon.silvers):,}")

**Dictionary loading configurations:**

* ``load_gold=True, load_silver=True``: Maximum coverage (default, ~365k entries)
* ``load_gold=True, load_silver=False``: Common words only (~179k entries, -22-31 MB)
* ``load_gold=False, load_silver=True``: Extended vocabulary only (unusual, ~187k entries)
* ``load_gold=False, load_silver=False``: Ultra-fast (espeak only, -50+ MB)

**When to disable dictionaries:**

* **Disable silver** (``load_silver=False``):
  * Resource-constrained environments (limited memory)
  * Real-time applications (faster initialization)
  * You only need common vocabulary
  * Production deployments where performance is critical

* **Disable both** (``load_gold=False, load_silver=False``):
  * Ultra-fast initialization is critical
  * You're fine with espeak-only fallback
  * Minimal memory footprint required
  * Testing or prototyping

**Default (both enabled) provides:**

* Maximum vocabulary coverage (~365k total entries)
* Best phoneme quality from curated dictionaries
* Backward compatibility with existing code

Disabling Features
~~~~~~~~~~~~~~~~~~

You can disable specific features for better performance or control:

.. code-block:: python

   from kokorog2p.en import EnglishG2P

   # Disable espeak fallback
   g2p = EnglishG2P(
       language="en-us",
       use_espeak_fallback=False,  # Unknown words will have no phonemes
       use_spacy=True
   )

   # Disable spaCy (faster but no POS tagging)
   g2p = EnglishG2P(
       language="en-us",
       use_espeak_fallback=True,
       use_spacy=False  # Faster tokenization
   )

   # Minimal configuration (fastest)
   g2p = EnglishG2P(
       language="en-us",
       use_espeak_fallback=False,
       use_spacy=False,
       load_silver=False,
       load_gold=False  # No dictionaries, ultra-fast
   )

Stress Control
~~~~~~~~~~~~~~

Control stress marker output:

.. code-block:: python

   from kokorog2p.de import GermanG2P

   # Strip stress markers from output
   g2p = GermanG2P(
       language="de-de",
       strip_stress=True  # Remove ˈ and ˌ markers
   )

Token Inspection
----------------

Tokens contain detailed information:

.. code-block:: python

   from kokorog2p import get_g2p

   g2p = get_g2p("en-us", use_spacy=True)
   tokens = g2p("I can't believe it!")

   for token in tokens:
       # Basic attributes
       print(f"Text: {token.text}")
       print(f"Phonemes: {token.phonemes}")
       print(f"POS tag: {token.tag}")
       print(f"Whitespace: '{token.whitespace}'")

       # Additional metadata
       rating = token.get("rating")  # 5=dictionary, 2=espeak, 0=unknown
       print(f"Rating: {rating}")

       # Check token type
       is_punct = not any(c.isalnum() for c in token.text)
       print(f"Is punctuation: {is_punct}")

Rating System
~~~~~~~~~~~~~

Tokens have a rating indicating the source of phonemes:

* **5**: User-provided (markdown annotations) or gold dictionary (highest quality)
* **4**: Punctuation
* **3**: Silver dictionary or rule-based conversion
* **2**: From espeak-ng fallback
* **1**: From goruut backend
* **0**: Unknown/failed

.. code-block:: python

   from kokorog2p import get_g2p

   g2p = get_g2p("en-us")
   tokens = g2p("Hello xyznotaword!")

   for token in tokens:
       rating = token.get("rating", 0)
       if rating == 5:
           print(f"{token.text}: High quality (gold dictionary)")
       elif rating == 3:
           print(f"{token.text}: Silver dictionary")
       elif rating == 2:
           print(f"{token.text}: Fallback (espeak)")
       elif rating == 0:
           print(f"{token.text}: Unknown")

Dictionary Lookup
-----------------

Direct dictionary access:

.. code-block:: python

   from kokorog2p.en import EnglishG2P

   # Load with or without silver dataset
   g2p_gold = EnglishG2P(language="en-us", load_silver=False)
   g2p_full = EnglishG2P(language="en-us", load_silver=True)

   # Simple lookup
   phonemes = g2p_gold.lexicon.lookup("hello")
   print(phonemes)  # həlˈO

   # Check if word is in dictionary
   if g2p_gold.lexicon.is_known("hello"):
       print("Word is in gold dictionary")

   # Get dictionary sizes
   print(f"Gold: {len(g2p_gold.lexicon.golds):,} entries")
   print(f"Silver: {len(g2p_full.lexicon.silvers):,} entries")

   # POS-aware lookup
   phonemes_verb = g2p_gold.lexicon.lookup("read", tag="VB")   # ɹˈid (present)
   phonemes_past = g2p_gold.lexicon.lookup("read", tag="VBD")  # ɹˈɛd (past)

German Lexicon
~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p.de import GermanLexicon

   lexicon = GermanLexicon(strip_stress=False)

   phonemes = lexicon.lookup("Haus")
   print(phonemes)  # haʊ̯s

   print(f"Dictionary has {len(lexicon):,} entries")  # 738,427

Phoneme Utilities
-----------------

Validation
~~~~~~~~~~

Validate phonemes against Kokoro vocabulary:

.. code-block:: python

   from kokorog2p import validate_phonemes, get_vocab

   # Check if phonemes are valid
   valid = validate_phonemes("hˈɛlO")
   print(valid)  # True

   invalid = validate_phonemes("xyz123")
   print(invalid)  # False

   # Get the full vocabulary
   vocab = get_vocab("us")
   print(f"US vocabulary: {len(vocab)} phonemes")

Conversion
~~~~~~~~~~

Convert between different phoneme formats:

.. code-block:: python

   from kokorog2p import from_espeak, to_espeak

   # Convert espeak IPA to Kokoro
   espeak_ipa = "həlˈəʊ"
   kokoro_phonemes = from_espeak(espeak_ipa, variant="us")
   print(kokoro_phonemes)  # hˈɛlO

   # Convert Kokoro to espeak IPA
   kokoro = "hˈɛlO"
   espeak = to_espeak(kokoro, variant="us")
   print(espeak)

Vocabulary Encoding
-------------------

Convert phonemes to IDs for model input:

.. code-block:: python

   from kokorog2p import phonemes_to_ids, ids_to_phonemes

   # Encode phonemes
   phonemes = "hˈɛlO wˈɜɹld"
   ids = phonemes_to_ids(phonemes)
   print(ids)  # [12, 45, 23, ...]

   # Decode back
   decoded = ids_to_phonemes(ids)
   print(decoded)  # hˈɛlO wˈɜɹld

   # Get Kokoro vocabulary
   from kokorog2p import get_kokoro_vocab
   vocab = get_kokoro_vocab()
   print(f"Kokoro has {len(vocab)} tokens")

Punctuation Handling
--------------------

Control punctuation normalization:

.. code-block:: python

   from kokorog2p import normalize_punctuation, filter_punctuation

   # Normalize to Kokoro punctuation
   text = "Hello... world!!!"
   normalized = normalize_punctuation(text)
   print(normalized)  # Hello. world!

   # Filter out non-Kokoro punctuation
   phonemes = "hˈɛlO… wˈɜɹld‼"
   filtered = filter_punctuation(phonemes)
   print(filtered)  # hˈɛlO. wˈɜɹld!

   # Check if punctuation is valid
   from kokorog2p import is_kokoro_punctuation
   print(is_kokoro_punctuation("!"))   # True
   print(is_kokoro_punctuation("…"))   # False

Word Mismatch Detection
-----------------------

Detect mismatches between input text and phoneme output:

.. code-block:: python

   from kokorog2p import detect_mismatches

   text = "Hello world!"
   phonemes = "hɛlO wɜɹld !"

   mismatches = detect_mismatches(text, phonemes)

   for mismatch in mismatches:
       print(f"Position {mismatch.position}:")
       print(f"  Input word: {mismatch.input_word}")
       print(f"  Output word: {mismatch.output_word}")
       print(f"  Type: {mismatch.type}")

Number Expansion
----------------

Customize number handling:

English
~~~~~~~

.. code-block:: python

   from kokorog2p.en.numbers import EnglishNumberConverter

   converter = EnglishNumberConverter()

   # Cardinals
   print(converter.convert_cardinal("42"))
   # → forty-two

   # Ordinals
   print(converter.convert_ordinal("42"))
   # → forty-second

   # Years
   print(converter.convert_year("1984"))
   # → nineteen eighty-four

   # Currency
   print(converter.convert_currency("12.50", "$"))
   # → twelve dollars and fifty cents

   # Decimals
   print(converter.convert_decimal("3.14"))
   # → three point one four

German
~~~~~~

.. code-block:: python

   from kokorog2p.de.numbers import GermanNumberConverter

   converter = GermanNumberConverter()

   # Cardinals
   print(converter.convert_cardinal("42"))
   # → zweiundvierzig

   # Ordinals
   print(converter.convert_ordinal("42"))
   # → zweiundvierzigste

   # Years
   print(converter.convert_year("1984"))
   # → neunzehnhundertvierundachtzig

   # Currency
   print(converter.convert_currency("12,50", "€"))
   # → zwölf Euro fünfzig

Custom Backend Selection
-------------------------

Choose specific backends:

.. code-block:: python

   from kokorog2p import get_g2p

   # Use espeak backend
   g2p_espeak = get_g2p("en-us", backend="espeak")

   # Use goruut backend (if installed)
   g2p_goruut = get_g2p("en-us", backend="goruut")

Direct Backend Access
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p.backends.espeak import EspeakBackend

   # Create espeak backend
   backend = EspeakBackend(language="en-us")

   # Phonemize a word
   phonemes = backend.phonemize("hello")
   print(phonemes)

Caching and Performance
-----------------------

Managing Cache
~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p import get_g2p, clear_cache

   # G2P instances are cached by language and settings
   g2p1 = get_g2p("en-us", use_spacy=True)
   g2p2 = get_g2p("en-us", use_spacy=True)
   assert g2p1 is g2p2  # Same instance

   # Different settings = different cache entry
   g2p3 = get_g2p("en-us", use_spacy=False)
   assert g2p1 is not g2p3  # Different instance
   
   # load_silver and load_gold also affect caching
   g2p4 = get_g2p("en-us", load_silver=False)
   assert g2p1 is not g2p4  # Different instance (different silver setting)
   
   g2p5 = get_g2p("en-us", load_gold=False)
   assert g2p1 is not g2p5  # Different instance (different gold setting)

   # Clear cache when needed
   clear_cache()

Batch Processing
~~~~~~~~~~~~~~~~

For best performance when processing many texts:

.. code-block:: python

   from kokorog2p import get_g2p

   # Create instance once
   g2p = get_g2p("en-us")

   texts = ["Hello", "World", "This", "Is", "Fast"]

   # Process many texts with same instance
   all_tokens = []
   for text in texts:
       tokens = g2p(text)
       all_tokens.append(tokens)

Custom Phoneme Filtering
-------------------------

Filter phonemes for specific use cases:

.. code-block:: python

   from kokorog2p import get_g2p, validate_for_kokoro, filter_for_kokoro

   g2p = get_g2p("en-us")
   tokens = g2p("Hello world!")

   phoneme_str = " ".join(t.phonemes for t in tokens if t.phonemes)

   # Validate for Kokoro
   is_valid = validate_for_kokoro(phoneme_str)

   # Filter to keep only valid Kokoro phonemes
   filtered = filter_for_kokoro(phoneme_str)
   print(filtered)

Error Handling
--------------

Handle missing dependencies gracefully:

.. code-block:: python

   from kokorog2p import get_g2p

   try:
       # This might fail if Chinese dependencies not installed
       g2p = get_g2p("zh")
       tokens = g2p("你好")
   except ImportError as e:
       print(f"Missing dependency: {e}")
       print("Install with: pip install kokorog2p[zh]")

   try:
       # This might fail if spaCy model not downloaded
       g2p = get_g2p("en-us", use_spacy=True)
   except OSError as e:
       print("spaCy model not found")
       print("Download with: python -m spacy download en_core_web_sm")

Next Steps
----------

* See :doc:`api/core` for detailed API reference
* Check :doc:`languages` for language-specific features
* Read :doc:`phonemes` to understand the phoneme inventory
