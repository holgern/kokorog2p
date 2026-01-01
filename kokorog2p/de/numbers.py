"""Number-to-words conversion for German G2P.

This module provides functions to convert numbers (digits, decimals, ordinals,
years, currency) into their German word representations for text-to-speech.

Based on the English numbers module, adapted for German language rules.
"""

import re
from collections.abc import Callable

# Ordinal suffixes in German
ORDINALS = frozenset([".", "te", "ter", "tes", "ten", "tem"])

# Currency symbols and their German word forms
CURRENCIES = {
    "€": ("Euro", "Cent"),
    "$": ("Dollar", "Cent"),
    "£": ("Pfund", "Pence"),
    "CHF": ("Franken", "Rappen"),
}


def is_digit(text: str) -> bool:
    """Check if text consists only of digits."""
    return bool(re.match(r"^[0-9]+$", text))


def is_currency_amount(word: str) -> bool:
    """Check if word looks like a currency amount (e.g., '12,99' or '12.99')."""
    # German uses comma as decimal separator
    parts = word.replace(".", "").split(",")
    if len(parts) > 2:
        return False
    return all(is_digit(p) for p in parts if p)


def number_to_german(n: int) -> str:
    """Convert an integer to German words.

    This is a fallback when num2words is not available.

    Args:
        n: Integer to convert.

    Returns:
        German word representation.
    """
    if n < 0:
        return "minus " + number_to_german(-n)

    if n == 0:
        return "null"

    ones = [
        "",
        "eins",
        "zwei",
        "drei",
        "vier",
        "fünf",
        "sechs",
        "sieben",
        "acht",
        "neun",
        "zehn",
        "elf",
        "zwölf",
        "dreizehn",
        "vierzehn",
        "fünfzehn",
        "sechzehn",
        "siebzehn",
        "achtzehn",
        "neunzehn",
    ]

    tens = [
        "",
        "",
        "zwanzig",
        "dreißig",
        "vierzig",
        "fünfzig",
        "sechzig",
        "siebzig",
        "achtzig",
        "neunzig",
    ]

    if n < 20:
        return ones[n]
    elif n < 100:
        if n % 10 == 0:
            return tens[n // 10]
        elif n % 10 == 1:
            return "einund" + tens[n // 10]
        else:
            return ones[n % 10] + "und" + tens[n // 10]
    elif n < 1000:
        if n % 100 == 0:
            return ones[n // 100] + "hundert" if n // 100 > 1 else "hundert"
        else:
            prefix = ones[n // 100] + "hundert" if n // 100 > 1 else "hundert"
            return prefix + number_to_german(n % 100)
    elif n < 1000000:
        thousands = n // 1000
        remainder = n % 1000
        if thousands == 1:
            prefix = "eintausend"
        else:
            prefix = number_to_german(thousands) + "tausend"
        if remainder == 0:
            return prefix
        return prefix + number_to_german(remainder)
    elif n < 1000000000:
        millions = n // 1000000
        remainder = n % 1000000
        if millions == 1:
            prefix = "eine Million"
        else:
            prefix = number_to_german(millions) + " Millionen"
        if remainder == 0:
            return prefix
        return prefix + " " + number_to_german(remainder)
    elif n < 1000000000000:
        billions = n // 1000000000
        remainder = n % 1000000000
        if billions == 1:
            prefix = "eine Milliarde"
        else:
            prefix = number_to_german(billions) + " Milliarden"
        if remainder == 0:
            return prefix
        return prefix + " " + number_to_german(remainder)
    else:
        return str(n)


def ordinal_to_german(n: int) -> str:
    """Convert an integer to German ordinal words.

    Args:
        n: Integer to convert.

    Returns:
        German ordinal word representation.
    """
    if n <= 0:
        return str(n) + "."

    # Special cases
    special = {
        1: "erste",
        3: "dritte",
        7: "siebte",
        8: "achte",
    }

    if n in special:
        return special[n]
    elif n < 20:
        return number_to_german(n) + "te"
    else:
        return number_to_german(n) + "ste"


class GermanNumberConverter:
    """Convert numbers to their German word representations.

    This class handles various number formats including:
    - Cardinal numbers (1, 2, 3 -> eins, zwei, drei)
    - Ordinal numbers (1., 2. -> erste, zweite)
    - Years (1984 -> neunzehnhundertvierundachtzig)
    - Decimals (3,14 -> drei Komma eins vier)
    - Currency (12,50€ -> zwölf Euro fünfzig)
    """

    def __init__(
        self,
        lookup_fn: Callable[[str, str | None], str | None] | None = None,
    ) -> None:
        """Initialize the German number converter.

        Args:
            lookup_fn: Optional function to look up words in the lexicon.
        """
        self.lookup = lookup_fn
        self._num2words: Callable | None = None

    @property
    def num2words(self) -> Callable:
        """Lazily import num2words with German language."""
        if self._num2words is None:
            try:
                from num2words import num2words

                def german_num2words(n, to="cardinal"):
                    return num2words(n, lang="de", to=to)

                self._num2words = german_num2words
            except ImportError:
                # Fallback to built-in converter
                def fallback(n, to="cardinal"):
                    if to == "ordinal":
                        return ordinal_to_german(int(n))
                    return number_to_german(int(n))

                self._num2words = fallback
        return self._num2words

    def convert_cardinal(self, word: str) -> str:
        """Convert cardinal number to German words.

        Args:
            word: Number string (e.g., "42", "1.000").

        Returns:
            German word representation.
        """
        # Remove thousand separators (German uses . for thousands)
        word = word.replace(".", "")
        try:
            return self.num2words(int(word), to="cardinal")
        except (ValueError, OverflowError):
            return word

    def convert_ordinal(self, word: str) -> str:
        """Convert ordinal number to German words.

        Args:
            word: Number string (e.g., "1", "42").

        Returns:
            German ordinal word representation.
        """
        word = word.replace(".", "")
        try:
            return self.num2words(int(word), to="ordinal")
        except (ValueError, OverflowError):
            return word

    def convert_year(self, word: str) -> str:
        """Convert year to German words.

        Args:
            word: Year string (e.g., "1984", "2024").

        Returns:
            German year word representation.
        """
        try:
            year = int(word)
            if 1100 <= year <= 1999:
                # Traditional German year reading: 1984 -> neunzehnhundertvierundachtzig
                century = year // 100
                remainder = year % 100
                century_word = self.num2words(century, to="cardinal")
                if remainder == 0:
                    return century_word + "hundert"
                remainder_word = self.num2words(remainder, to="cardinal")
                return century_word + "hundert" + remainder_word
            else:
                # Modern years: 2024 -> zweitausendvierundzwanzig
                return self.num2words(year, to="cardinal")
        except (ValueError, OverflowError):
            return word

    def convert_decimal(self, word: str) -> str:
        """Convert decimal number to German words.

        German uses comma as decimal separator.

        Args:
            word: Decimal string (e.g., "3,14" or "3.14").

        Returns:
            German word representation.
        """
        # Normalize to comma (German style)
        word = word.replace(".", ",")
        parts = word.split(",")

        if len(parts) == 1:
            return self.convert_cardinal(parts[0])

        integer_part = self.convert_cardinal(parts[0]) if parts[0] else "null"
        # Read decimal digits individually
        decimal_digits = " ".join(
            self.num2words(int(d), to="cardinal") for d in parts[1]
        )

        return f"{integer_part} Komma {decimal_digits}"

    def convert_currency(self, word: str, currency: str) -> str:
        """Convert currency amount to German words.

        Args:
            word: Amount string (e.g., "12,50").
            currency: Currency symbol (e.g., "€").

        Returns:
            German currency word representation.
        """
        currency_names = CURRENCIES.get(currency, ("", ""))

        # Normalize decimal separator
        word = word.replace(".", ",")
        parts = word.split(",")

        result_parts = []

        # Integer part (euros/dollars/etc.)
        if parts[0]:
            int_val = int(parts[0])
            int_word = self.num2words(int_val, to="cardinal")
            unit = currency_names[0]
            result_parts.append(f"{int_word} {unit}")

        # Decimal part (cents/etc.)
        if len(parts) > 1 and parts[1] and int(parts[1]) > 0:
            dec_val = int(parts[1])
            # Ensure two-digit cents
            if len(parts[1]) == 1:
                dec_val *= 10
            dec_word = self.num2words(dec_val, to="cardinal")
            unit = currency_names[1] if len(currency_names) > 1 else ""
            if result_parts:
                result_parts.append(f"{dec_word} {unit}")
            else:
                result_parts.append(f"{dec_word} {unit}")

        return " ".join(result_parts).strip()

    def convert(
        self,
        word: str,
        currency: str | None = None,
        is_ordinal: bool = False,
        is_year: bool = False,
    ) -> str:
        """Convert a number to its German word representation.

        Args:
            word: The number string to convert.
            currency: Optional currency symbol (e.g., '€').
            is_ordinal: Whether to convert as ordinal.
            is_year: Whether to convert as year.

        Returns:
            German word representation.
        """
        # Handle negative numbers
        negative = False
        if word.startswith("-"):
            negative = True
            word = word[1:]

        result = ""

        if is_ordinal or word.endswith("."):
            # Ordinal number
            word = word.rstrip(".")
            result = self.convert_ordinal(word)
        elif is_year and len(word) == 4 and is_digit(word):
            # Year
            result = self.convert_year(word)
        elif currency and currency in CURRENCIES:
            # Currency amount
            result = self.convert_currency(word, currency)
        elif "," in word or ("." in word and word.count(".") == 1):
            # Decimal number
            result = self.convert_decimal(word)
        else:
            # Cardinal number
            result = self.convert_cardinal(word)

        if negative:
            result = "minus " + result

        return result


def expand_number(text: str) -> str:
    """Expand numbers in text to German words.

    This is a convenience function for simple number expansion.

    Args:
        text: Text potentially containing numbers.

    Returns:
        Text with numbers expanded to German words.
    """
    converter = GermanNumberConverter()

    def replace_number(match: re.Match) -> str:
        word = match.group(0)

        # Check for currency
        currency = None
        if word.endswith("€"):
            currency = "€"
            word = word[:-1]
        elif word.startswith("€"):
            currency = "€"
            word = word[1:]

        # Check for ordinal (ends with .)
        is_ordinal = word.endswith(".") and is_digit(word.rstrip("."))

        # Check for year (4-digit standalone number)
        is_year = len(word) == 4 and is_digit(word)

        return converter.convert(
            word, currency=currency, is_ordinal=is_ordinal, is_year=is_year
        )

    # Match numbers with optional currency symbols
    pattern = r"€?\-?[\d.,]+€?\.?"

    return re.sub(pattern, replace_number, text)
