"""Tests for plotline.reports.review module."""

from __future__ import annotations

import json
from pathlib import Path

from plotline.reports.review import _build_theme_name_lookup, generate_review


class TestBuildThemeNameLookup:
    def test_no_synthesis_file(self, tmp_project: Path) -> None:
        """Returns empty dict when synthesis.json is absent."""
        assert _build_theme_name_lookup(tmp_project) == {}

    def test_empty_unified_themes(self, tmp_project: Path) -> None:
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(json.dumps({"unified_themes": []}))
        assert _build_theme_name_lookup(tmp_project) == {}

    def test_builds_lookup_from_synthesis(self, tmp_project: Path) -> None:
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {"unified_theme_id": "utheme_001", "name": "Theme One"},
                        {"unified_theme_id": "utheme_002", "name": "Theme Two"},
                    ]
                }
            )
        )
        lookup = _build_theme_name_lookup(tmp_project)
        assert lookup == {"utheme_001": "Theme One", "utheme_002": "Theme Two"}


class TestGenerateReview:
    def test_generates_report(self, tmp_project: Path) -> None:
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.parent.mkdir(parents=True, exist_ok=True)
        selections_path.write_text(
            json.dumps(
                {"segments": [{"segment_id": "seg_001", "start": 0, "end": 10, "text": "Hello"}]}
            )
        )

        manifest = {"project_name": "review-test", "interviews": []}
        output = generate_review(tmp_project, manifest, open_browser=False)

        assert output.exists()
        assert output.name == "review.html"
        content = output.read_text()
        assert "review-test" in content

    def test_resolves_theme_ids(self, tmp_project: Path) -> None:
        """Theme IDs (utheme_001) are replaced with their real names."""
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.parent.mkdir(parents=True, exist_ok=True)
        selections_path.write_text(
            json.dumps({"segments": [{"segment_id": "s1", "themes": ["utheme_001"]}]})
        )

        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.write_text(
            json.dumps(
                {"unified_themes": [{"unified_theme_id": "utheme_001", "name": "The Great Filter"}]}
            )
        )

        manifest = {"project_name": "themes-test", "interviews": []}
        output = generate_review(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        assert "The Great Filter" in content
        assert "utheme_001" not in content

    def test_displays_cultural_flags(self, tmp_project: Path) -> None:
        """Segments with culturally_flagged=True show a warning in the UI."""
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.parent.mkdir(parents=True, exist_ok=True)
        selections_path.write_text(
            json.dumps(
                {
                    "segments": [
                        {
                            "segment_id": "s1",
                            "text": "Flagged text",
                            "flagged": True,
                            "flag_reason": "Contains sensitive ritual details",
                        }
                    ]
                }
            )
        )

        manifest = {"project_name": "flags-test", "interviews": []}
        output = generate_review(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        # Check for the top-level banner alert
        assert "1 segment flagged by AI" in content
        # Check for the segment-level warning
        assert "Contains sensitive ritual details" in content

    def test_displays_pacing_and_alternates(self, tmp_project: Path) -> None:
        """Pacing guidance and alternate candidates from arc are surfaced."""
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.parent.mkdir(parents=True, exist_ok=True)
        selections_path.write_text(
            json.dumps(
                {
                    "segments": [
                        {
                            "segment_id": "s1",
                            "position": 2,
                            "pacing": "Hold on the smile before cutting.",
                        }
                    ]
                }
            )
        )

        arc_path = tmp_project / "data" / "arc.json"
        arc_path.write_text(
            json.dumps(
                {
                    "alternate_candidates": [
                        {
                            "for_position": 2,
                            "segment_id": "alt_001",
                            "reasoning": "A stronger alternate take.",
                        }
                    ]
                }
            )
        )

        manifest = {"project_name": "pacing-test", "interviews": []}
        output = generate_review(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        # Pacing
        assert "Hold on the smile before cutting." in content
        assert "Pacing guidance:" in content
        # Alternate
        assert "alt_001" in content
        assert "A stronger alternate take." in content
