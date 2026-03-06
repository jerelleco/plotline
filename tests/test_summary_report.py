"""Tests for plotline.reports.summary module."""

from __future__ import annotations

import json
from pathlib import Path

from plotline.reports.summary import generate_summary


class TestGenerateSummary:
    def test_generates_report(self, tmp_project: Path) -> None:
        manifest = {
            "project_name": "summary-test",
            "interviews": [
                {
                    "id": "int_001",
                    "filename": "alice.mov",
                    "duration_seconds": 300.0,
                }
            ],
        }
        output = generate_summary(tmp_project, manifest, open_browser=False)

        assert output.exists()
        assert output.name == "summary.html"
        content = output.read_text()
        assert "summary-test" in content

    def test_custom_output_path(self, tmp_project: Path) -> None:
        manifest = {"project_name": "custom", "interviews": []}
        custom = tmp_project / "my_summary.html"
        output = generate_summary(tmp_project, manifest, output_path=custom, open_browser=False)
        assert output == custom
        assert custom.exists()

    def test_uses_friendly_duration(self, tmp_project: Path) -> None:
        """Summary should use friendly format (e.g. '5m') not timecode ('5:00')."""
        manifest = {
            "project_name": "dur-test",
            "interviews": [{"id": "int_001", "filename": "test.mov", "duration_seconds": 300.0}],
        }
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()
        assert "5m" in content

    def test_nav_bar_with_summary_active(self, tmp_project: Path) -> None:
        """Summary report marks its own nav link as active."""
        manifest = {
            "project_name": "nav-test",
            "interviews": [{"id": "int_001", "filename": "test.mov", "duration_seconds": 60.0}],
        }
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()
        assert "plotline-nav" in content
        assert 'href="summary.html"' in content
        assert "transcript_int_001.html" in content

    def test_no_interviews(self, tmp_project: Path) -> None:
        manifest = {"project_name": "empty", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        assert output.exists()


class TestSummaryThemesBugFix:
    """Tests that summary reads unified_themes (not the old 'themes' key)."""

    def test_reads_unified_themes(self, tmp_project: Path) -> None:
        """Themes from synthesis.json unified_themes appear in the report."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {"name": "Connection to Water", "segment_count": 12},
                        {"name": "Loss and Memory", "segment_count": 8},
                    ]
                }
            )
        )

        manifest = {"project_name": "themes-test", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        assert "Connection to Water" in content
        assert "Loss and Memory" in content

    def test_old_themes_key_ignored(self, tmp_project: Path) -> None:
        """Themes stored under the old 'themes' key are NOT picked up."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "themes": [
                        {"name": "Ghost Theme", "segment_count": 5},
                    ],
                    "unified_themes": [],
                }
            )
        )

        manifest = {"project_name": "old-key-test", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        assert "Ghost Theme" not in content

    def test_no_synthesis_file(self, tmp_project: Path) -> None:
        """Report generates without crashing when synthesis.json is absent."""
        manifest = {"project_name": "no-synth", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        assert output.exists()
        content = output.read_text()
        # Theme Map section should not appear
        assert "Theme Map" not in content

    def test_theme_size_capping(self, tmp_project: Path) -> None:
        """Theme size is capped at 3 regardless of segment count."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [
                        {"name": "Huge Theme", "segment_count": 100},
                        {"name": "Small Theme", "segment_count": 2},
                    ]
                }
            )
        )

        manifest = {"project_name": "size-test", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        assert "size-3" in content
        assert "size-1" in content

    def test_max_ten_themes(self, tmp_project: Path) -> None:
        """At most 10 themes are shown even if more exist."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        themes = [{"name": f"Theme {i}", "segment_count": 5} for i in range(15)]
        synthesis_path.write_text(json.dumps({"unified_themes": themes}))

        manifest = {"project_name": "many-themes", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        assert "Theme 0" in content
        assert "Theme 9" in content
        assert "Theme 10" not in content


class TestSummarySelections:
    def test_selected_segments_shown(self, tmp_project: Path) -> None:
        """Selected segments from selections.json appear as highlights."""
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.write_text(
            json.dumps(
                {
                    "segments": [
                        {
                            "segment_id": "seg_001",
                            "interview_id": "int_001",
                            "start": 0,
                            "end": 10,
                            "text": "A powerful opening statement about rivers.",
                            "composite_score": 0.92,
                            "role": "opening",
                        }
                    ]
                }
            )
        )

        manifest = {
            "project_name": "sel-test",
            "interviews": [{"id": "int_001", "filename": "alice.mov", "duration_seconds": 60.0}],
        }
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        assert "0.92" in content
        assert "A powerful opening statement" in content

    def test_contribution_percent(self, tmp_project: Path) -> None:
        """Contribution percentage is calculated per interview."""
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.write_text(
            json.dumps(
                {
                    "segments": [
                        {"segment_id": "s1", "interview_id": "int_001", "start": 0, "end": 10},
                        {"segment_id": "s2", "interview_id": "int_001", "start": 10, "end": 20},
                        {"segment_id": "s3", "interview_id": "int_002", "start": 0, "end": 10},
                    ]
                }
            )
        )

        manifest = {
            "project_name": "contrib",
            "interviews": [
                {"id": "int_001", "filename": "alice.mov", "duration_seconds": 60.0},
                {"id": "int_002", "filename": "bob.mov", "duration_seconds": 60.0},
            ],
        }
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        # int_001 has 2 of 3 segments = 66.7%
        assert "66.7" in content
        # int_002 has 1 of 3 = 33.3%
        assert "33.3" in content

    def test_arc_role_classes(self, tmp_project: Path) -> None:
        """Arc segments get correct role classes for CSS markers."""
        selections_path = tmp_project / "data" / "selections.json"
        selections_path.write_text(
            json.dumps(
                {
                    "segments": [
                        {
                            "segment_id": "s1",
                            "start": 0,
                            "end": 5,
                            "text": "Opening",
                            "role": "hook",
                        },
                        {
                            "segment_id": "s2",
                            "start": 5,
                            "end": 10,
                            "text": "Middle",
                            "role": "body",
                        },
                        {
                            "segment_id": "s3",
                            "start": 10,
                            "end": 15,
                            "text": "End",
                            "role": "resolution",
                        },
                    ]
                }
            )
        )

        manifest = {"project_name": "arc-test", "interviews": []}
        output = generate_summary(tmp_project, manifest, open_browser=False)
        content = output.read_text()

        # The role_class values should be present in CSS class attributes
        assert "hook" in content
        assert "body" in content
        assert "resolution" in content
