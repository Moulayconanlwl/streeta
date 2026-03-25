# -*- coding: utf-8 -*-
"""
InternationalBuildingNumberExtractor
─────────────────────────────────────
Multi-pass, language-aware extractor of building / house numbers
from free-form international address strings.

Extraction pipeline (in order of priority):
  1. Inline  "No." / "nº" / "nr." pattern anywhere in string      → very reliable
  2. After-comma pattern  "… , 123"                               → reliable
  3. Russian dom-indicator  "д. 15" / "дом 15"                   → script-specific
  4. CJK hierarchical pattern                                      → script-specific
  5. Language-aware: starts-with-digit → NUMBER-FIRST             → high confidence
  6. Language-aware: known prefix detected → NUMBER-LAST          → good confidence
  7. Trailing-number heuristic                                     → moderate
  8. Fallback: first isolated number found                         → low confidence
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


@dataclass
class ExtractionResult:
    raw_address:      str
    building_number:  Optional[str]
    confidence:       float           # 0.0 – 1.0
    lang_code:        Optional[str]
    number_position:  str             # 'first' | 'last' | 'complex' | 'unknown'
    method:           str
    notes:            list = field(default_factory=list)


def _clean(text: str) -> str:
    """Normalize whitespace and remove zero-width chars."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\u200b\u200c\u200d\ufeff]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _normalize_number(raw: str) -> str:
    """Normalize extracted number string: trim spaces around separators."""
    raw = raw.strip()
    raw = re.sub(r"\s*-\s*", "-", raw)
    raw = re.sub(r"\s*/\s*", "/", raw)
    raw = re.sub(r"\s+", " ", raw)
    return raw


class InternationalBuildingNumberExtractor:
    """
    Thread-safe, stateless extractor.  Instantiate once and reuse.
    """

    def extract(self, addr_ln3: str, addr_ln4: str = "") -> ExtractionResult:
        """
        Concatenate CLIADDLN3_LA + CLIADDLN4_LA and extract the building number.

        Parameters
        ----------
        addr_ln3 : str   Content of CLIADDLN3_LA column
        addr_ln4 : str   Content of CLIADDLN4_LA column (optional)

        Returns
        -------
        ExtractionResult dataclass
        """
        # ── 0. Build combined address ──────────────────────────────────────
        parts = [_clean(str(addr_ln3 or "")), _clean(str(addr_ln4 or ""))]
        parts = [p for p in parts if p]
        full_address = " ".join(parts)

        if not full_address:
            return ExtractionResult(
                raw_address="", building_number=None,
                confidence=0.0, lang_code=None,
                number_position="unknown", method="empty input",
            )

        # ── 1. Inline No. / nº / nr. / # anywhere ─────────────────────────
        m = RE_INLINE_NO.search(full_address)
        if m:
            num = _normalize_number(m.group(1))
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.97, lang_code=None,
                number_position="inline", method="inline No./nº/nr. pattern",
            )

        # ── 2. After-comma pattern ─────────────────────────────────────────
        m = RE_AFTER_COMMA.search(full_address)
        if m:
            num = _normalize_number(m.group(1))
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.93, lang_code=None,
                number_position="after_comma", method="after-comma number pattern",
            )

        # ── 3. Russian dom indicator ───────────────────────────────────────
        m = RE_RU_DOM.search(full_address)
        if m:
            num = _normalize_number(m.group(1))
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.96, lang_code="RU",
                number_position="last", method="Russian dom (д./дом) indicator",
            )

        # ── 4. Japanese chome-ban-go ───────────────────────────────────────
        m = RE_JP_CHOME.search(full_address)
        if m:
            num = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.95, lang_code="JP",
                number_position="complex", method="Japanese chome-ban-go",
            )
        m = RE_JP_SIMPLE.search(full_address)
        if m:
            num = f"{m.group(1)}-{m.group(2)}"
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.93, lang_code="JP",
                number_position="complex", method="Japanese ban-go",
            )

        # ── 4b. Chinese 号 ─────────────────────────────────────────────────
        m = RE_ZH_NUMBER.search(full_address)
        if m:
            return ExtractionResult(
                raw_address=full_address, building_number=m.group(1),
                confidence=0.90, lang_code="ZH",
                number_position="complex", method="Chinese 号 indicator",
            )

        # ── 4c. Korean 번지/호 ─────────────────────────────────────────────
        m = RE_KO_NUMBER.search(full_address)
        if m:
            return ExtractionResult(
                raw_address=full_address, building_number=m.group(1),
                confidence=0.90, lang_code="KO",
                number_position="complex", method="Korean address indicator",
            )

        # ── 5. Language detection ──────────────────────────────────────────
        detection = detect_number_position(full_address)
        position  = detection["position"]
        lang_code = detection["lang_code"]

        # ── 5a. NUMBER-FIRST ───────────────────────────────────────────────
        if position == "first":
            m = RE_NUMBER_FIRST.match(full_address)
            if m:
                num = _normalize_number(m.group(1))
                return ExtractionResult(
                    raw_address=full_address, building_number=num,
                    confidence=0.95, lang_code=lang_code,
                    number_position="first",
                    method=f"number-first ({detection['method']})",
                )

        # ── 5b. NUMBER-LAST ────────────────────────────────────────────────
        if position in ("last", "unknown"):
            m = RE_NUMBER_LAST.search(full_address)
            if m:
                num = _normalize_number(m.group(1))
                conf = 0.90 if position == "last" else 0.72
                return ExtractionResult(
                    raw_address=full_address, building_number=num,
                    confidence=conf, lang_code=lang_code,
                    number_position="last",
                    method=f"number-last ({detection['method']})",
                )

        # ── 6. Trailing number heuristic (catches DE compound words) ───────
        m = re.search(r"[\s,]+(\d+[a-zA-Z]?(?:/[a-zA-Z])?)[\s,]*$", full_address)
        if m:
            num = _normalize_number(m.group(1))
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.75, lang_code=lang_code,
                number_position="last",
                method="trailing number heuristic",
            )

        # ── 7. number-first fallback when detection was uncertain ──────────
        m = RE_NUMBER_FIRST.match(full_address)
        if m:
            num = _normalize_number(m.group(1))
            return ExtractionResult(
                raw_address=full_address, building_number=num,
                confidence=0.65, lang_code=lang_code,
                number_position="first",
                method="number-first fallback",
            )

        # ── 8. Last resort: first isolated number ─────────────────────────
        candidates = RE_FALLBACK.findall(full_address)
        if candidates:
            # Filter out obvious postal codes or year-like 4+ digit numbers if
            # there are shorter alternatives
            short = [c for c in candidates if len(re.sub(r"\D", "", c)) <= 5]
            pick = short[0] if short else candidates[0]
            return ExtractionResult(
                raw_address=full_address, building_number=pick,
                confidence=0.45, lang_code=lang_code,
                number_position="fallback",
                method="last-resort isolated number",
                notes=["Low confidence — multiple numbers found; first selected"]
                      if len(candidates) > 1 else [],
            )

        # ── 9. Not found ───────────────────────────────────────────────────
        return ExtractionResult(
            raw_address=full_address, building_number=None,
            confidence=0.0, lang_code=lang_code,
            number_position="unknown", method="no number found",
        )
