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
* Comprehensive test suite (432+ tests)
* Benchmarking framework for performance testing

Changed
~~~~~~~

* Improved English contraction handling
* Enhanced number conversion for all languages
* Better error handling for missing dependencies

Fixed
~~~~~

* Fixed contraction tokenization in English
* Fixed stress marker handling in German
* Improved phonological rules for Czech

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
