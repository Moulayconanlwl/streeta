# -*- coding: utf-8 -*-
"""Regex patterns for international building/house number extraction."""

import re

# ── PATTERN 1: Optional No./nº prefix normalizer ─────────────────────────
RE_NO_PREFIX = re.compile(
    r"^(?:n[°º\.:]?\s*|no\.?\s*|num\.?\s*|nr\.?\s*|n\xfam\.?\s*|n\xba\.?\s*|#\s*)",
    re.IGNORECASE | re.UNICODE,
)

# ── PATTERN 2: Number-first (EN/FR/NL/AR/GR/HE/IN) ───────────────────────
# Handles: "12", "12A", "12bis", "12-14", "12 1/2", "No.5", "N°12"
RE_NUMBER_FIRST = re.compile(
    r"^(?:n[°º\.:]?\s*|no\.?\s*|num\.?\s*|nr\.?\s*|n\xfam\.?\s*|n\xba\.?\s*|#\s*)?"
    r"(\d+(?:\s*[-/]\s*\d+)?(?:\s*(?:bis|ter|quater|quinquies|tris))?(?:\s*[a-zA-Z](?!\w))?(?:\s+1/2)?)"
    r"(?=[\s,\-/]|$)",
    re.IGNORECASE | re.UNICODE,
)

# ── PATTERN 3: Number-last (DE/IT/ES/PT/Nordic/RU/PL/HU/RO) ─────────────
# Handles: "Via Roma 10", "Hauptstr. 12A", "Calle Mayor, 5", "utca 5/A"
RE_NUMBER_LAST = re.compile(
    r"(?:^|[\s,]+)"
    r"(?:no\.?\s*|n[°º\.:]?\s*|nr\.?\s*|n\xfam\.?\s*|n\xba\.?\s*|#\s*)?"
    r"(\d+(?:\s*[-/]\s*\d+[a-zA-Z]?)?(?:\s*[a-zA-Z](?!\w))?(?:\s*[-/]\s*[a-zA-Z])?)"
    r"\s*$",
    re.IGNORECASE | re.UNICODE,
)

# ── PATTERN 4: Inline No./nº/nr./#  anywhere in string ───────────────────
# Handles: "Atatürk Cad. No:5", "Park Lane, nr. 23", "Beyoğlu No.12A"
RE_INLINE_NO = re.compile(
    r"(?:no\.?\s*|n[°º\.:]?\s*|nr\.?\s*|n\xfam\.?\s*|n\xba\.?\s*|num\.?\s*|#\s*)"
    r"(\d+(?:\s*[-/]\s*\d+[a-zA-Z]?)?(?:\s*[a-zA-Z](?!\w))?)",
    re.IGNORECASE | re.UNICODE,
)

# ── PATTERN 5: After-comma  (PT/BR/IT mixed formats) ─────────────────────
# Handles: "Rua das Flores, 123", "Via Roma, 10 int. 5"
RE_AFTER_COMMA = re.compile(
    r",\s*(?:no\.?\s*|n[°º\.:]?\s*|nr\.?\s*|n\xfam\.?\s*|n\xba\.?\s*|#\s*)?"
    r"(\d+(?:\s*[-/]\s*\d+[a-zA-Z]?)?(?:\s*[a-zA-Z](?!\w))?)",
    re.IGNORECASE | re.UNICODE,
)

# ── PATTERN 6: Japanese chome-ban-go ─────────────────────────────────────
RE_JP_CHOME = re.compile(r"(\d+)\u4e01\u76ee(\d+)\u756a(?:\u5730)?(\d+)\u53f7?", re.UNICODE)
RE_JP_SIMPLE = re.compile(r"(\d+)\u756a(?:\u5730)?(\d+)\u53f7?", re.UNICODE)

# ── PATTERN 7: Chinese 号 ─────────────────────────────────────────────────
RE_ZH_NUMBER = re.compile(r"(\d+)\u53f7", re.UNICODE)

# ── PATTERN 8: Korean 번지/호/로/길 ─────────────────────────────────────────
RE_KO_NUMBER = re.compile(r"(\d+)(?:\ub2f8\uc9c0|\ud638|\ub85c|\uae38)", re.UNICODE)

# ── PATTERN 9: Russian dom indicator  д./дом ─────────────────────────────
RE_RU_DOM = re.compile(
    r"(?:\u0434(?:\u043e\u043c)?\.?\s*)(\d+[\u0430-\u044f\u0410-\u042fA-Za-z]?(?:\s*[-/]\s*\d+[\u0430-\u044f\u0410-\u042fA-Za-z]?)?)",
    re.IGNORECASE | re.UNICODE,
)

# ── PATTERN 10: Fallback — any isolated number ───────────────────────────
RE_FALLBACK = re.compile(r"(?<![a-zA-Z\d])(\d+[a-zA-Z]?)(?!\d)", re.IGNORECASE | re.UNICODE)
