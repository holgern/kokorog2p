Changelog
=========

All notable changes to kokorog2p will be documented in this file.

Unreleased
----------

Added
~~~~~

* German G2P module with 738k+ entry dictionary
* Czech G2P module with rule-based phonology
* French G2P module with gold dictionary
* Comprehensive test suite (469 tests including 37 new contraction tests)
* Benchmarking framework for performance testing
* Contraction merging for spaCy tokenizer in English G2P
* Test coverage for single and double contractions (don't, could've, I'd've, etc.)

Changed
~~~~~~~

* Improved English contraction handling with intelligent token merging
* Enhanced number conversion for all languages
* Better error handling for missing dependencies
* Updated documentation with multi-language support examples
* Improved type annotations and mypy configuration

Fixed
~~~~~

* Fixed contraction tokenization in English (don't was incorrectly split as "Do" + "n't")
* Fixed Chinese tone_sandhi import type annotation
* Fixed GToken __post_init__ to handle None values for extension dict
* Fixed stress marker handling in German
* Improved phonological rules for Czech
* Fixed documentation API references for English and French modules

Version 0.1.0 (Initial Release)
-------------------------------

Added
~~~~~

* Core G2P framework
* English G2P (US and GB variants)
* Chinese G2P with jieba and pypinyin
* Japanese G2P with pyopenjtalk
* espeak-ng backend support
* goruut backend support (experimental)
* Number and currency handling
* Phoneme vocabulary encoding/decoding
* Punctuation normalization
* Word mismatch detection
* Comprehensive API documentation
* Test suite with 300+ tests

Features
~~~~~~~~

* Dictionary-based lookup with gold/silver tiers
* POS-aware pronunciation for English
* Automatic stress assignment
* Multi-backend support
* Caching for performance
* Type hints throughout
* Full IPA support
