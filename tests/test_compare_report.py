"""Tests for plotline.reports.compare module."""

from __future__ import annotations

import json
from pathlib import Path

from plotline.reports.compare import generate_compare_report


class TestGenerateCompareReport:
    def test_raises_without_synthesis(self, tmp_project: Path) -> None:
        """Without synthesis.json, the report generator raises FileNotFoundError."""
        manifest = {"project_name": "compare-test", "interviews": []}
        from plotline.config import PlotlineConfig

        config = PlotlineConfig()
        try:
            generate_compare_report(tmp_project, manifest, config, open_browser=False)
            raise AssertionError("Expected FileNotFoundError")
        except FileNotFoundError as e:
            assert "synthesis" in str(e).lower()

    def test_generates_report_with_synthesis(self, tmp_project: Path) -> None:
        """With synthesis.json containing best_takes, report generates."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [{"name": "Test Theme", "source_themes": []}],
                    "best_takes": [
                        {
                            "topic": "Test Theme",
                            "candidates": [],
                        }
                    ],
                }
            )
        )

        manifest = {"project_name": "compare-test", "interviews": []}
        from plotline.config import PlotlineConfig

        config = PlotlineConfig()
        output = generate_compare_report(tmp_project, manifest, config, open_browser=False)

        assert output.exists()
        assert output.name == "compare.html"
        content = output.read_text()
        assert "compare-test" in content

    def test_key_messages_normalized_to_strings(self, tmp_project: Path) -> None:
        """key_messages in brief.json may be dicts; template must render as strings."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [{"name": "Sustainability", "source_themes": []}],
                    "best_takes": [
                        {
                            "topic": "Sustainability",
                            "candidates": [],
                        }
                    ],
                }
            )
        )

        brief_path = tmp_project / "brief.json"
        brief_path.write_text(
            json.dumps(
                {
                    "key_messages": [
                        {"id": "msg_001", "text": "First message"},
                        {"id": "msg_002", "text": "Second message"},
                    ]
                }
            )
        )

        manifest = {"project_name": "compare-test", "interviews": []}
        from plotline.config import PlotlineConfig

        config = PlotlineConfig()
        output = generate_compare_report(tmp_project, manifest, config, open_browser=False)

        content = output.read_text()
        assert "First message" in content
        assert "Second message" in content
        assert "msg_001" not in content
        assert "{" not in content or "First message" in content

    def test_custom_output_path(self, tmp_project: Path) -> None:
        """Custom output path is respected."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [],
                    "best_takes": [],
                }
            )
        )

        manifest = {"project_name": "compare-test", "interviews": []}
        from plotline.config import PlotlineConfig

        config = PlotlineConfig()
        custom_path = tmp_project / "my_compare.html"
        output = generate_compare_report(
            tmp_project, manifest, config, output_path=custom_path, open_browser=False
        )

        assert output == custom_path
        assert custom_path.exists()

    def test_nav_bar_includes_compare(self, tmp_project: Path) -> None:
        """Compare report includes nav bar with compare link active."""
        synthesis_path = tmp_project / "data" / "synthesis.json"
        synthesis_path.parent.mkdir(parents=True, exist_ok=True)
        synthesis_path.write_text(
            json.dumps(
                {
                    "unified_themes": [],
                    "best_takes": [],
                }
            )
        )

        manifest = {"project_name": "compare-test", "interviews": []}
        from plotline.config import PlotlineConfig

        config = PlotlineConfig()
        output = generate_compare_report(tmp_project, manifest, config, open_browser=False)

        content = output.read_text()
        assert "plotline-nav" in content
        assert 'href="compare.html"' in content
