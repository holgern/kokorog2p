Chinese API
===========

Chinese G2P uses jieba for tokenization and pypinyin for phoneme conversion.

Main Class
----------

.. autoclass:: kokorog2p.zh.ChineseG2P
   :members:
   :undoc-members:
   :show-inheritance:

Examples
--------

.. code-block:: python

   from kokorog2p.zh import ChineseG2P

   g2p = ChineseG2P(language="zh")
   tokens = g2p("你好世界")

   for token in tokens:
       print(f"{token.text} -> {token.phonemes}")

Features
--------

* Jieba tokenization for Chinese word segmentation
* Pypinyin for pinyin conversion to IPA
* Tone sandhi rules
* cn2an for number handling
* Chinese to Western punctuation mapping
