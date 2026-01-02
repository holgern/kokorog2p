Mixed-Language API
==================

The mixed-language module provides automatic language detection for texts mixing multiple languages.

Main Class
----------

.. autoclass:: kokorog2p.mixed_language_g2p.MixedLanguageG2P
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   .. automethod:: __call__

   .. automethod:: phonemize

   .. automethod:: lookup

   .. automethod:: get_cache_size

   .. automethod:: clear_detection_cache

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from kokorog2p import get_g2p

   # German text with English words
   g2p = get_g2p(
       language="de",
       multilingual_mode=True,
       allowed_languages=["de", "en-us"]
   )

   tokens = g2p("Das Meeting war great!")

   for token in tokens:
       if token.is_word:
           detected = token.get("detected_language")
           print(f"{token.text} ({detected}) -> {token.phonemes}")

Output:

.. code-block:: text

   Das (de) -> das
   Meeting (en-us) -> mˈiɾɪŋ
   war (de) -> vaːɐ̯
   great (en-us) -> ɡɹˈeɪt

Direct API Usage
~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p.mixed_language_g2p import MixedLanguageG2P

   # More control over detection
   g2p = MixedLanguageG2P(
       primary_language="de",
       allowed_languages=["de", "en-us", "fr"],
       confidence_threshold=0.6,  # Lower threshold = more aggressive detection
       enable_detection=True
   )

   tokens = g2p("Ich gehe zum Meeting mit Marie.")

   # Access detection metadata
   for token in tokens:
       if token.is_word:
           detected = token.get("detected_language")
           confidence = token.get("language_confidence")
           print(f"{token.text}: {detected} (confidence: {confidence:.2f})")

Configuring Confidence
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p import get_g2p

   # Conservative detection (higher confidence required)
   g2p_conservative = get_g2p(
       language="de",
       multilingual_mode=True,
       allowed_languages=["de", "en-us"],
       language_confidence_threshold=0.9  # Very high confidence
   )

   # Aggressive detection (lower confidence required)
   g2p_aggressive = get_g2p(
       language="de",
       multilingual_mode=True,
       allowed_languages=["de", "en-us"],
       language_confidence_threshold=0.5  # Lower confidence
   )

Cache Management
~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p import get_g2p

   g2p = get_g2p(
       language="de",
       multilingual_mode=True,
       allowed_languages=["de", "en-us"]
   )

   # Process some text (builds cache)
   g2p("Hello World Hallo Welt")

   # Check cache size
   cache_size = g2p.get_cache_size()
   print(f"Cached {cache_size} words")

   # Clear cache if needed
   g2p.clear_detection_cache()

Handling Graceful Degradation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p import get_g2p

   # If lingua-py is not installed, this still works
   # but uses only the primary language
   g2p = get_g2p(
       language="de",
       multilingual_mode=True,  # Ignored if lingua not available
       allowed_languages=["de", "en-us"]
   )

   # You can check if detection is actually enabled
   if hasattr(g2p, 'detector') and g2p.detector is not None:
       print("Language detection is active")
   else:
       print("Fallback to primary language only")

Technical Details
-----------------

Supported Languages
~~~~~~~~~~~~~~~~~~~

The mixed-language module supports automatic detection between:

* English (en-us, en-gb)
* German (de)
* French (fr)
* Spanish (es)
* Italian (it)
* Portuguese (pt)
* Japanese (ja)
* Chinese (zh)
* Korean (ko)
* Hebrew (he)
* Czech (cs)
* Dutch (nl)
* Polish (pl)
* Russian (ru)
* Arabic (ar)
* Hindi (hi)
* Turkish (tr)

Language Mapping
~~~~~~~~~~~~~~~~

The module automatically maps between kokorog2p language codes and lingua-py language codes:

.. code-block:: python

   # kokorog2p code -> lingua-py code
   "en-us" -> Language.ENGLISH
   "en-gb" -> Language.ENGLISH
   "de" -> Language.GERMAN
   "fr" -> Language.FRENCH
   # ... and more

Detection Behavior
~~~~~~~~~~~~~~~~~~

Words are detected based on:

1. **Word length**: Words < 3 characters use primary language (too short to detect)
2. **Confidence**: Words below threshold use primary language
3. **Allowed languages**: Only languages in allowed_languages are considered
4. **Caching**: Each word's detection is cached for performance

Performance Characteristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **Memory**: ~100 MB for lingua language models (loaded once)
* **Speed**: ~0.1-0.5 ms per word detection (first time)
* **Speed**: ~0.001 ms per word (cached)
* **Accuracy**: >90% for words with 5+ characters
* **Cache**: Unlimited size (clear manually if needed)

Limitations
~~~~~~~~~~~

* Short words (<3 chars) are always assigned to primary language
* Detection quality depends on word length and distinctiveness
* Proper nouns may be misdetected
* Mixed-script texts (e.g., Japanese with Latin) need special handling
* lingua-py required for detection (otherwise falls back to primary language only)
