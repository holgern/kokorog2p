#!/usr/bin/env python3
"""Regenerate phonemes in synthetic data using actual G2P output.

This ensures phonemes match what the G2P system actually produces,
including punctuation marks and context-dependent pronunciations.
"""

import json
from pathlib import Path
from kokorog2p.en import EnglishG2P


def regenerate_phonemes(input_file: Path, output_file: Path | None = None) -> None:
    """Regenerate phonemes using G2P output.

    Args:
        input_file: Path to input synthetic JSON file
        output_file: Path to output file (default: overwrite input)
    """
    if output_file is None:
        output_file = input_file

    # Load existing data
    with open(input_file) as f:
        data = json.load(f)

    # Create G2P with gold+silver (reference configuration)
    g2p = EnglishG2P(
        language="en-us",
        use_espeak_fallback=False,
        use_spacy=False,
        load_gold=True,
        load_silver=True,
    )

    updated_count = 0
    unchanged_count = 0

    print(f"Regenerating phonemes for {len(data['sentences'])} sentences...")
    print()

    for sentence in data["sentences"]:
        sent_id = sentence["id"]
        text = sentence["text"]
        old_phonemes = sentence["phonemes"]

        # Phonemize
        tokens = g2p(text)

        # Extract ALL phonemes (including punctuation)
        new_phonemes = " ".join(t.phonemes for t in tokens if t.phonemes)

        # Update if different
        if old_phonemes != new_phonemes:
            print(f"Sentence {sent_id}:")
            print(f"  Old: {old_phonemes}")
            print(f"  New: {new_phonemes}")
            print()
            sentence["phonemes"] = new_phonemes
            updated_count += 1
        else:
            unchanged_count += 1

    # Save updated data
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Complete!")
    print(f"  Updated: {updated_count} sentences")
    print(f"  Unchanged: {unchanged_count} sentences")
    print(f"  Output: {output_file}")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Regenerate phonemes in synthetic data"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input synthetic JSON file",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file (default: overwrite input)",
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: File not found: {args.input}")
        return 1

    regenerate_phonemes(args.input, args.output)
    return 0


if __name__ == "__main__":
    exit(main())
