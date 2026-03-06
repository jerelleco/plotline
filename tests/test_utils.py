"""Tests for plotline.utils module."""

from __future__ import annotations

from plotline.utils import (
    THEME_COLORS,
    format_duration,
    format_duration_friendly,
    get_delivery_class,
    get_theme_color,
)


class TestFormatDuration:
    def test_seconds_only(self) -> None:
        assert format_duration(45.0) == "0:45"

    def test_minutes_and_seconds(self) -> None:
        assert format_duration(125.0) == "2:05"

    def test_hours_minutes_seconds(self) -> None:
        assert format_duration(3725.0) == "1:02:05"

    def test_exact_hour(self) -> None:
        assert format_duration(3600.0) == "1:00:00"

    def test_zero(self) -> None:
        assert format_duration(0.0) == "0:00"

    def test_large_duration(self) -> None:
        assert format_duration(7384.0) == "2:03:04"

    def test_float_seconds(self) -> None:
        assert format_duration(90.7) == "1:30"


class TestGetDeliveryClass:
    def test_high_score(self) -> None:
        assert get_delivery_class(0.85) == "filled"
        assert get_delivery_class(0.7) == "filled"
        assert get_delivery_class(1.0) == "filled"

    def test_medium_score(self) -> None:
        assert get_delivery_class(0.5) == "medium"
        assert get_delivery_class(0.4) == "medium"
        assert get_delivery_class(0.69) == "medium"

    def test_low_score(self) -> None:
        assert get_delivery_class(0.1) == "low"
        assert get_delivery_class(0.0) == "low"
        assert get_delivery_class(0.39) == "low"

    def test_boundary_at_07(self) -> None:
        assert get_delivery_class(0.7) == "filled"
        assert get_delivery_class(0.699) == "medium"

    def test_boundary_at_04(self) -> None:
        assert get_delivery_class(0.4) == "medium"
        assert get_delivery_class(0.399) == "low"


class TestFormatDurationFriendly:
    def test_hours_and_minutes(self) -> None:
        assert format_duration_friendly(3725.0) == "1h 2m"

    def test_exact_hour(self) -> None:
        assert format_duration_friendly(3600.0) == "1h 0m"

    def test_multiple_hours(self) -> None:
        assert format_duration_friendly(8100.0) == "2h 15m"

    def test_minutes_only(self) -> None:
        assert format_duration_friendly(180.0) == "3m"

    def test_one_minute(self) -> None:
        assert format_duration_friendly(60.0) == "1m"

    def test_seconds_only(self) -> None:
        assert format_duration_friendly(45.0) == "45s"

    def test_zero(self) -> None:
        assert format_duration_friendly(0.0) == "0s"

    def test_fractional_seconds_truncated(self) -> None:
        assert format_duration_friendly(90.7) == "1m"

    def test_large_duration(self) -> None:
        assert format_duration_friendly(7384.0) == "2h 3m"


class TestThemeColors:
    def test_palette_has_twelve_colors(self) -> None:
        assert len(THEME_COLORS) == 12

    def test_all_colors_are_hex(self) -> None:
        for color in THEME_COLORS:
            assert color.startswith("#")
            assert len(color) == 7

    def test_no_duplicate_colors(self) -> None:
        assert len(set(THEME_COLORS)) == len(THEME_COLORS)


class TestGetThemeColor:
    def test_first_color(self) -> None:
        assert get_theme_color(0) == "#3b82f6"

    def test_last_color(self) -> None:
        assert get_theme_color(11) == "#84cc16"

    def test_wraps_around(self) -> None:
        assert get_theme_color(12) == get_theme_color(0)
        assert get_theme_color(13) == get_theme_color(1)

    def test_large_index(self) -> None:
        assert get_theme_color(120) == get_theme_color(0)

    def test_each_index_returns_from_palette(self) -> None:
        for i in range(12):
            assert get_theme_color(i) == THEME_COLORS[i]
