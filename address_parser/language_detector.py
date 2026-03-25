# -*- coding: utf-8 -*-
"""Language / address-format detector."""

import re
import unicodedata
from .abbrevs.multilingual import MASTER_LOOKUP

RE_CYRILLIC  = re.compile(r"[\u0400-\u04FF]")
RE_ARABIC_SC = re.compile(r"[\u0600-\u06FF\u0750-\u077F]")
RE_HEBREW_SC = re.compile(r"[\u0590-\u05FF]")
RE_CJK       = re.compile(r"[\u4E00-\u9FFF\u3400-\u4DBF\uF900-\uFAFF]")
RE_KOREAN    = re.compile(r"[\uAC00-\uD7AF\u1100-\u11FF]")
RE_JAPANESE  = re.compile(r"[\u3040-\u30FF]")


def _tokenize(address):
    tokens = re.split(r"[\s,./;:]+", address.lower().strip())
    return [t for t in tokens if t]


def detect_number_position(address):
    """Return dict with keys: position, lang_code, confidence, method."""
    if not address or not address.strip():
        return {"position": "unknown", "lang_code": None, "confidence": 0.0, "method": "empty"}

    addr = address.strip()

    if RE_JAPANESE.search(addr):
        return {"position": "complex", "lang_code": "JP", "confidence": 0.95, "method": "Japanese script"}
    if RE_KOREAN.search(addr):
        return {"position": "complex", "lang_code": "KO", "confidence": 0.95, "method": "Korean script"}
    if RE_CJK.search(addr):
        return {"position": "complex", "lang_code": "ZH", "confidence": 0.90, "method": "CJK script"}
    if RE_ARABIC_SC.search(addr):
        return {"position": "first",   "lang_code": "AR", "confidence": 0.85, "method": "Arabic script"}
    if RE_HEBREW_SC.search(addr):
        return {"position": "first",   "lang_code": "HE", "confidence": 0.85, "method": "Hebrew script"}
    if RE_CYRILLIC.search(addr):
        return {"position": "last",    "lang_code": "RU", "confidence": 0.85, "method": "Cyrillic script"}

    if addr[0].isdigit():
        return {"position": "first", "lang_code": None, "confidence": 0.95, "method": "starts with digit"}

    tokens = _tokenize(addr)
    lang_votes = {}
    for token in tokens[:6]:
        if token in MASTER_LOOKUP:
            lang_code, position = MASTER_LOOKUP[token]
            if lang_code not in lang_votes:
                lang_votes[lang_code] = {"votes": 0, "position": position}
            lang_votes[lang_code]["votes"] += 1

    if lang_votes:
        best = max(lang_votes, key=lambda k: lang_votes[k]["votes"])
        votes = lang_votes[best]["votes"]
        confidence = min(0.95, 0.60 + 0.10 * votes)
        return {
            "position":   lang_votes[best]["position"],
            "lang_code":  best,
            "confidence": confidence,
            "method":     f"keyword match ({votes} tokens)",
        }

    if re.search(r"\s+\d+[a-zA-Z]?\s*$", addr):
        return {"position": "last", "lang_code": None, "confidence": 0.70, "method": "trailing number"}

    return {"position": "unknown", "lang_code": None, "confidence": 0.30, "method": "no signal"}
