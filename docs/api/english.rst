English API
===========

English G2P provides high-quality phoneme conversion for US and British English.

Main Class
----------

.. autoclass:: kokorog2p.en.EnglishG2P
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   .. automethod:: __call__

   .. automethod:: phonemize

   .. automethod:: lookup

Lexicon
-------

.. autoclass:: kokorog2p.en.EnglishLexicon
   :members:
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   .. automethod:: lookup

   .. automethod:: is_known

   .. automethod:: __len__

Number Conversion
-----------------

Converter Class
~~~~~~~~~~~~~~~

.. autoclass:: kokorog2p.en.numbers.NumberConverter
   :members:
   :undoc-members:

   .. automethod:: __init__

   .. automethod:: convert

Helper Functions
~~~~~~~~~~~~~~~~

.. autofunction:: kokorog2p.en.numbers.is_digit

.. autofunction:: kokorog2p.en.numbers.is_currency_amount

Constants
~~~~~~~~~

.. autodata:: kokorog2p.en.numbers.ORDINALS
   :annotation:

.. autodata:: kokorog2p.en.numbers.CURRENCIES
   :annotation:

Examples
--------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from kokorog2p.en import EnglishG2P

   # US English
   g2p = EnglishG2P(language="en-us")
   tokens = g2p("Hello world!")

   for token in tokens:
       print(f"{token.text} -> {token.phonemes}")

   # British English
   g2p_gb = EnglishG2P(language="en-gb")
   tokens = g2p_gb("Hello world!")

Dictionary Lookup
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p.en import EnglishLexicon

   lexicon = EnglishLexicon(language="en-us")

   # Simple lookup
   phonemes = lexicon.lookup("hello")
   print(phonemes)  # həlˈO

   # POS-aware lookup
   read_present = lexicon.lookup("read", tag="VB")
   read_past = lexicon.lookup("read", tag="VBD")

Number Expansion
~~~~~~~~~~~~~~~~

.. code-block:: python

   from kokorog2p.en import EnglishG2P

   # Numbers are automatically expanded during G2P processing
   g2p = EnglishG2P(language="en-us")
   tokens = g2p("I have $42.50 and 3 cats.")

   for token in tokens:
       print(f"{token.text} -> {token.phonemes}")
   # → I -> aɪ
   # → have -> hæv
   # → forty-two dollars and fifty cents -> ...
   # → and -> ænd
   # → three -> θɹi
   # → cats -> kæts
