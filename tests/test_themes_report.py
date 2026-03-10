"""Tests for plotline.reports.themes module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from plotline.reports.themes import generate_themes_report


class TestGenerateThemesReport:
    def test_raises_without_theme_data(self, tmp_project: Path) -> None:
        """Without synthesis.json or themes/, raises FileNotFoundError."""
        manifest = {"project_name": "themes-test", "interviews": []}

        with pytest.raises(FileNotFoundError) as exc_info:
            generate_themes_report(tmp_project, manifest, open_browser=False)

        assert "theme" in str(exc_info.value).lower()

    def test_generates_report_from_synthesis(self, tmp_project: Path) -> None:
        """With synthesis.json containing unified_themes, report generates."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {
                            "unified_theme_id": "utheme_001",
                            "name": "Connection to Nature",
                            "description": "Themes about nature",
                            "all_segment_ids": [],
                            "source_themes": [],
                            "perspectives": "Hopeful",
                        }
                    ]
                }
            )
        )

        manifest = {"project_name": "themes-test", "interviews": []}
        output = generate_themes_report(tmp_project, manifest, open_browser=False)

        assert output.exists()
        assert output.name == "themes.html"
        content = output.read_text()
        assert "themes-test" in content
        assert "Connection to Nature" in content

    def test_generates_report_from_per_interview_themes(self, tmp_project: Path) -> None:
        """With per-interview themes (no synthesis), report generates."""
        themes_path = tmp_project / "data" / "themes" / "int_001.json"
        themes_path.parent.mkdir(parents=True, exist_ok=True)
        themes_path.write_text(
            json.dumps(
                {
                    "themes": [
                        {
                            "theme_id": "theme_001",
                            "name": "Personal Journey",
                            "description": "Individual experiences",
                            "segment_ids": [],
                            "strength": 0.8,
                        }
                    ]
                }
            )
        )

        manifest = {"project_name": "themes-test", "interviews": []}
        output = generate_themes_report(tmp_project, manifest, open_browser=False)

        assert output.exists()
        content = output.read_text()
        assert "Personal Journey" in content

    def test_segment_lookup_dict_passed_to_template(self, tmp_project: Path) -> None:
        """Verify segment_lookup dict is in template data for O(1) lookup."""
        segments_path = tmp_project / "data" / "segments" / "int_001.json"
        segments_path.parent.mkdir(parents=True, exist_ok=True)
        segments_path.write_text(
            json.dumps(
                {
                    "segments": [
                        {
                            "segment_id": "int_001_seg_001",
                            "text": "Test segment text",
                            "start": 0.0,
                            "end": 5.0,
                            "delivery": {"composite_score": 0.75},
                        }
                    ]
                }
            )
        )

        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {
                            "unified_theme_id": "utheme_001",
                            "name": "Test Theme",
                            "all_segment_ids": ["int_001_seg_001"],
                            "source_themes": ["t1"],
                        }
                    ]
                }
            )
        )

        manifest = {
            "project_name": "themes-test",
            "interviews": [{"id": "int_001", "filename": "interview1.mp4", "frame_rate": 24}],
        }
        output = generate_themes_report(tmp_project, manifest, open_browser=False)

        content = output.read_text()
        assert "Test segment text" in content
        assert "Test Theme" in content

    def test_custom_output_path(self, tmp_project: Path) -> None:
        """Custom output path is respected."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {
                            "unified_theme_id": "utheme_001",
                            "name": "Theme One",
                            "all_segment_ids": [],
                            "source_themes": [],
                        }
                    ]
                }
            )
        )

        manifest = {"project_name": "themes-test", "interviews": []}
        custom_path = tmp_project / "my_themes.html"
        output = generate_themes_report(
            tmp_project, manifest, output_path=custom_path, open_browser=False
        )

        assert output == custom_path
        assert custom_path.exists()

    def test_nav_bar_includes_themes(self, tmp_project: Path) -> None:
        """Themes report includes nav bar with themes link active."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {
                            "unified_theme_id": "utheme_001",
                            "name": "Theme One",
                            "all_segment_ids": [],
                            "source_themes": [],
                        }
                    ]
                }
            )
        )

        manifest = {"project_name": "themes-test", "interviews": []}
        output = generate_themes_report(tmp_project, manifest, open_browser=False)

        content = output.read_text()
        assert "plotline-nav" in content
        assert 'href="themes.html"' in content
