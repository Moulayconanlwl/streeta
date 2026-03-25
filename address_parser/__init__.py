# -*- coding: utf-8 -*-
"""
international_address_parser
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Multi-language building number extractor.
Processes CLIADDLN3_LA + CLIADDLN4_LA columns from Excel input.

Quick start:
    from address_parser import InternationalBuildingNumberExtractor
    ext = InternationalBuildingNumberExtractor()
    result = ext.extract("12 rue de la Paix", "")
    print(result.building_number)   # → "12"
"""

from .extractor import InternationalBuildingNumberExtractor, ExtractionResult

__title__   = "international_address_parser"
__version__ = "1.0.0"
__all__     = ["InternationalBuildingNumberExtractor", "ExtractionResult"]
