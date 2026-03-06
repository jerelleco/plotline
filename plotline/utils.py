"""
plotline.utils - Shared utility functions.

Contains common functions used across multiple modules to avoid duplication.
"""

from __future__ import annotations


def format_duration(seconds: float) -> str:
    """Format seconds as HH:MM:SS or MM:SS.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (HH:MM:SS if >= 1 hour, otherwise MM:SS)
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_duration_friendly(seconds: float) -> str:
    """Format seconds as human-friendly duration string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g. "2h 15m", "3m", "45s")
    """
    if seconds >= 3600:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
    if seconds >= 60:
        minutes = int(seconds // 60)
        return f"{minutes}m"
    return f"{int(seconds)}s"


def get_delivery_class(score: float) -> str:
    """Get CSS class for delivery score badge.

    Args:
        score: Delivery score (0.0 to 1.0)

    Returns:
        CSS class name: "filled" (high), "medium", or "low"
    """
    if score >= 0.7:
        return "filled"
    elif score >= 0.4:
        return "medium"
    return "low"


# Shared theme color palette (12 colors) used across all report templates.
THEME_COLORS = [
    "#3b82f6",
    "#8b5cf6",
    "#06b6d4",
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#ec4899",
    "#14b8a6",
    "#6366f1",
    "#d946ef",
    "#0ea5e9",
    "#84cc16",
]


def get_theme_color(index: int) -> str:
    """Get a consistent color for a theme by index.

    Args:
        index: Theme index (wraps around the palette)

    Returns:
        Hex color string
    """
    return THEME_COLORS[index % len(THEME_COLORS)]
