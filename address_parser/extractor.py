# -*- coding: utf-8 -*-
"""
InternationalBuildingNumberExtractor
─────────────────────────────────────
Multi-pass, language-aware extractor of building / house numbers
from free-form international address strings.

ADDITION:
- number_index → index (0-based) of first character of the building number
                 in the concatenation LN3 + LN4
"""

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Optional

from .patterns import (
    RE_NO_PREFIX, RE_NUMBER_FIRST, RE_NUMBER_LAST, RE_INLINE_NO,
    RE_AFTER_COMMA, RE_JP_CHOME, RE_JP_SIMPLE, RE_ZH_NUMBER,
    RE_KO_NUMBER, RE_RU_DOM, RE_FALLBACK,
)
from .language_detector import detect_number_position


# ─────────────────────────────────────────────────────────────────────────────
# Result object
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExtractionResult:
    raw_address:      str
    building_number:  Optional[str]
    number_index:     Optional[int]   # 0-based index in raw_address
    confidence:       float
    lang_code:        Optional[str]
    number_position:  str
    method:           str
    notes:            list = field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _clean(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _normalize_number(raw: str) -> str:
    raw = raw.strip()
    raw = re.sub(r"\s*-\s*", "-", raw)
    raw = re.sub(r"\s*/\s*", "/", raw)
    raw = re.sub(r"\s+", " ", raw)
    return raw


def _mask_blocked_patterns(text: str) -> str:
    """
    Mask (do not remove) floor numbers / PO Box / ordinals with spaces.

    This keeps character positions aligned with the original LN3+LN4 string.
    """
    from .patterns import RE_FLOOR, RE_POBOX, RE_ORDINAL

    def _mask(regex, s):
        return regex.sub(lambda m: " " * len(m.group(0)), s)

    text = _mask(RE_FLOOR, text)
    text = _mask(RE_POBOX, text)
    text = _mask(RE_ORDINAL, text)
    return text


# ─────────────────────────────────────────────────────────────────────────────
# Extractor
# ─────────────────────────────────────────────────────────────────────────────

class InternationalBuildingNumberExtractor:
    """
    Thread-safe, stateless extractor.
    """

    def extract(self, addr_ln3: str, addr_ln4: str = "") -> ExtractionResult:

        # ── 0. Build concatenated Omega address ───────────────────────────
        parts = [_clean(addr_ln3 or ""), _clean(addr_ln4 or "")]
        parts = [p for p in parts if p]
        raw_concat = " ".join(parts)

        if not raw_concat:
            return ExtractionResult(
                raw_address="",
                building_number=None,
                number_index=None,
                confidence=0.0,
                lang_code=None,
                number_position="unknown",
                method="empty input",
            )

        # Mask patterns but keep indices
        masked = _mask_blocked_patterns(raw_concat)

        # Allow regex matching from first meaningful char
        stripped = masked.lstrip()
        lead_offset = len(masked) - len(stripped)
        work = stripped

        # Helper to build result safely
        def _result(num, m, confidence, lang, pos, method, notes=None):
            return ExtractionResult(
                raw_address=raw_concat,
                building_number=num,
                number_index=lead_offset + m.start(1),
                confidence=confidence,
                lang_code=lang,
                number_position=pos,
                method=method,
                notes=notes or [],
            )

        # ── 1. Inline No / nº / nr / # ────────────────────────────────────
        m = RE_INLINE_NO.search(work)
        if m:
            return _result(
                _normalize_number(m.group(1)), m,
                0.97, None, "inline",
                "inline No./nº/nr. pattern"
            )

        # ── 2. After-comma ────────────────────────────────────────────────
        m = RE_AFTER_COMMA.search(work)
        if m:
            return _result(
                _normalize_number(m.group(1)), m,
                0.93, None, "after_comma",
                "after-comma number pattern"
            )

        # ── 3. Russian дом ────────────────────────────────────────────────
        m = RE_RU_DOM.search(work)
        if m:
            return _result(
                _normalize_number(m.group(1)), m,
                0.96, "RU", "last",
                "Russian dom (д./дом) indicator"
            )

        # ── 4. JP / CJK / KO ───────────────────────────────────────────────
        m = RE_JP_CHOME.search(work)
        if m:
            num = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            return _result(num, m, 0.95, "JP", "complex", "Japanese chome-ban-go")

        m = RE_JP_SIMPLE.search(work)
        if m:
            num = f"{m.group(1)}-{m.group(2)}"
            return _result(num, m, 0.93, "JP", "complex", "Japanese ban-go")

        m = RE_ZH_NUMBER.search(work)
        if m:
            return _result(m.group(1), m, 0.90, "ZH", "complex", "Chinese 号 indicator")

        m = RE_KO_NUMBER.search(work)
        if m:
            return _result(m.group(1), m, 0.90, "KO", "complex", "Korean address indicator")

        # ── 5. Language detection ──────────────────────────────────────────
        detection = detect_number_position(work)
        position = detection["position"]
        lang = detection["lang_code"]

        # ── 5a. Number-first ───────────────────────────────────────────────
        if position == "first":
            m = RE_NUMBER_FIRST.match(work)
            if m:
                return _result(
                    _normalize_number(m.group(1)), m,
                    0.95, lang, "first",
                    f"number-first ({detection['method']})"
                )

        # ── 5b. Number-last ────────────────────────────────────────────────
        if position in ("last", "unknown"):
            m = RE_NUMBER_LAST.search(work)
            if m:
                return _result(
                    _normalize_number(m.group(1)), m,
                    0.90 if position == "last" else 0.72,
                    lang, "last",
                    f"number-last ({detection['method']})"
                )

        # ── 6. Fallback ────────────────────────────────────────────────────
        iters = list(RE_FALLBACK.finditer(work))
        if iters:
            pick = iters[0]
            return _result(
                pick.group(1), pick,
                0.45, lang, "fallback",
                "last-resort isolated number",
                ["Low confidence — multiple numbers found"] if len(iters) > 1 else []
            )

        # ── 7. Not found ───────────────────────────────────────────────────
        return ExtractionResult(
            raw_address=raw_concat,
            building_number=None,
            number_index=None,
            confidence=0.0,
            lang_code=lang,
            number_position="unknown",
            method="no number found",
        )
