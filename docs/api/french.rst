French API
==========

French G2P provides phoneme conversion using a gold dictionary with espeak-ng fallback.

Main Class
----------

.. autoclass:: kokorog2p.fr.FrenchG2P
   :members:
   :undoc-members:
   :show-inheritance:

Lexicon
-------

.. autoclass:: kokorog2p.fr.FrenchLexicon
   :members:
   :undoc-members:
   :show-inheritance:

Number Conversion
-----------------

Helper Functions
~~~~~~~~~~~~~~~~

.. autofunction:: kokorog2p.fr.numbers.number_to_french

.. autofunction:: kokorog2p.fr.numbers.expand_numbers

.. autofunction:: kokorog2p.fr.numbers.expand_time

.. autofunction:: kokorog2p.fr.numbers.expand_currency

.. autofunction:: kokorog2p.fr.numbers.expand_ordinal

.. autofunction:: kokorog2p.fr.numbers.is_available

Examples
--------

.. code-block:: python

   from kokorog2p.fr import FrenchG2P

   g2p = FrenchG2P(language="fr-fr")
   tokens = g2p("Bonjour le monde!")

   for token in tokens:
       print(f"{token.text} -> {token.phonemes}")
