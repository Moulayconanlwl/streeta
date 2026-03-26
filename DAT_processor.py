#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dat_processor.py
──────────────────────────────────────────────────────────────────────────────
Process .DAT flat files (tilde '~' separated) and extract building numbers
using InternationalBuildingNumberExtractor.

Behavior:
- Reads .DAT file line by line
- Splits by '~'
- Uses column index 3 (LN3) and 4 (LN4) for address extraction
- Adds a new final column containing the building number (or empty)
- Writes the output as .DAT with identical formatting but +1 column
"""

import sys
from pathlib import Path
from address_parser import InternationalBuildingNumberExtractor


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def read_dat_file(path, sep="~"):
    """Read a .DAT file and return list of rows (each row = list of fields)."""
    rows = []
    with open(path, "r", encoding="latin-1") as f:
        for line in f:
            line = line.rstrip("\n")
            fields = line.split(sep)
            rows.append(fields)
    return rows


def write_dat_file(rows, path, sep="~"):
    """Write rows (list of lists) into a .DAT file with same separator."""
    with open(path, "w", encoding="utf-8") as f:
        for fields in rows:
            line = sep.join("" if v is None else str(v) for v in fields)
            f.write(line + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# Core DAT processing
# ─────────────────────────────────────────────────────────────────────────────

def process_dat(
    input_path: str,
    output_path: str = None,
    ln3_index: int = 3,
    ln4_index: int = 4,
):
    """
    Process a .DAT file, extract building numbers, and output a new .DAT.

    Parameters:
        input_path  : str  → path to input DAT file
        output_path : str  → path to output DAT file (optional)
        ln3_index   : int  → index of LN3 column
        ln4_index   : int  → index of LN4 column
    """

    inp = Path(input_path)
    if not inp.exists():
        raise FileNotFoundError(f"Input file does not exist: {inp}")

    if output_path is None:
        output_path = inp.parent / (inp.stem + "_with_numbers.DAT")

    # Load extractor
    extractor = InternationalBuildingNumberExtractor()

    # Read DAT
    rows = read_dat_file(inp)
    out_rows = []

    for fields in rows:
        # Ensure the row has enough columns
        # If shorter than expected, pad with empty fields
        max_index = max(ln3_index, ln4_index)
        while len(fields) <= max_index:
            fields.append("")

        ln3 = fields[ln3_index]
        ln4 = fields[ln4_index]

        result = extractor.extract(ln3, ln4)

        # Append a final column with the building number or empty string
        bn_value = result.building_number if result.building_number else ""
        fields_out = fields + [bn_value]

        out_rows.append(fields_out)

    # Write output
    write_dat_file(out_rows, output_path)

    print(f"Done → {output_path}")
    return output_path


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dat_processor.py input.DAT [output.DAT]")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) >= 3 else None
    process_dat(inp, out)