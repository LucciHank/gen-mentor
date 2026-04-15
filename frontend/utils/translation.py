# Translation utility for mapping technical values to Vietnamese for display

LEVEL_MAP = {
    "unlearned": "Chưa học",
    "beginner": "Sơ cấp",
    "intermediate": "Trung cấp",
    "advanced": "Cao cấp"
}

CONFIDENCE_MAP = {
    "low": "Thấp",
    "medium": "Trung bình",
    "high": "Cao"
}

def translate_level(level: str) -> str:
    """Translate technical level strings to Vietnamese."""
    if not level:
        return level
    return LEVEL_MAP.get(level.lower(), level.capitalize())

def translate_confidence(confidence: str) -> str:
    """Translate confidence strings to Vietnamese."""
    if not confidence:
        return confidence
    return CONFIDENCE_MAP.get(confidence.lower(), confidence.capitalize())

def get_level_key(vietnamese_level: str) -> str:
    """Get the original English key from a Vietnamese level string."""
    for key, value in LEVEL_MAP.items():
        if value == vietnamese_level:
            return key
    return vietnamese_level
