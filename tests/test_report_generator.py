"""Tests for plotline.reports.generator and reports __init__ exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from plotline.reports import (
    ReportGenerator,
    generate_compare_report,
    generate_coverage,
    generate_dashboard,
    generate_review,
    generate_summary,
    generate_themes_report,
    generate_transcript,
)
from plotline.reports.generator import ReportGenerator as DirectGenerator


class TestReportsInit:
    def test_all_generators_exported(self) -> None:
        """All seven generators plus ReportGenerator are importable from plotline.reports."""
        assert callable(generate_dashboard)
        assert callable(generate_transcript)
        assert callable(generate_themes_report)
        assert callable(generate_compare_report)
        assert callable(generate_coverage)
        assert callable(generate_review)
        assert callable(generate_summary)
        assert ReportGenerator is DirectGenerator

    def test_all_list_complete(self) -> None:
        """__all__ includes every public name."""
        from plotline.reports import __all__

        expected = {
            "ReportGenerator",
            "generate_compare_report",
            "generate_coverage",
            "generate_dashboard",
            "generate_review",
            "generate_summary",
            "generate_themes_report",
            "generate_transcript",
        }
        assert set(__all__) == expected


class TestReportGeneratorRender:
    def test_render_creates_file(self, tmp_path: Path) -> None:
        """render() writes an HTML file to the given path."""
        gen = ReportGenerator()
        output = tmp_path / "reports" / "test.html"
        data: dict[str, Any] = {"project_name": "Test"}
        gen.render("dashboard.html", data, output)

        assert output.exists()
        content = output.read_text()
        assert "Test" in content

    def test_render_injects_nav_interviews(self, tmp_path: Path) -> None:
        """When manifest is passed, nav_interviews list is injected into data."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        manifest = {
            "interviews": [
                {"id": "int_001", "filename": "alice.mov"},
                {"id": "int_002", "filename": "bob.mov"},
            ]
        }
        data: dict[str, Any] = {"project_name": "Nav Test"}
        gen.render("dashboard.html", data, output, manifest=manifest)

        content = output.read_text()
        assert "alice.mov" in content
        assert "bob.mov" in content
        assert "transcript_int_001.html" in content
        assert "transcript_int_002.html" in content

    def test_render_no_manifest_no_crash(self, tmp_path: Path) -> None:
        """render() works without manifest (no nav interviews)."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        data: dict[str, Any] = {"project_name": "No Nav"}
        gen.render("dashboard.html", data, output)

        content = output.read_text()
        assert "No interviews" in content

    def test_render_manifest_without_interviews(self, tmp_path: Path) -> None:
        """Manifest with empty interviews list shows 'No interviews'."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        manifest: dict[str, Any] = {"interviews": []}
        data: dict[str, Any] = {"project_name": "Empty"}
        gen.render("dashboard.html", data, output, manifest=manifest)

        content = output.read_text()
        assert "No interviews" in content

    def test_render_does_not_overwrite_existing_nav(self, tmp_path: Path) -> None:
        """If data already has nav_interviews, manifest does not overwrite it."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        manifest = {"interviews": [{"id": "int_001", "filename": "manifest.mov"}]}
        data: dict[str, Any] = {
            "project_name": "Pre-set",
            "nav_interviews": [{"id": "custom_001", "filename": "custom.mov"}],
        }
        gen.render("dashboard.html", data, output, manifest=manifest)

        content = output.read_text()
        assert "custom.mov" in content
        # manifest interview should NOT appear since nav_interviews was pre-set
        assert "manifest.mov" not in content

    def test_render_manifest_interview_missing_filename(self, tmp_path: Path) -> None:
        """Interview without filename falls back to id."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        manifest = {"interviews": [{"id": "int_fallback"}]}
        data: dict[str, Any] = {"project_name": "Fallback"}
        gen.render("dashboard.html", data, output, manifest=manifest)

        content = output.read_text()
        assert "int_fallback" in content


class TestNavBarInHtml:
    def test_nav_contains_all_report_links(self, tmp_path: Path) -> None:
        """The rendered nav bar has links to all seven report views."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        data: dict[str, Any] = {"project_name": "Links"}
        gen.render("dashboard.html", data, output)

        content = output.read_text()
        assert 'href="dashboard.html"' in content
        assert 'href="themes.html"' in content
        assert 'href="compare.html"' in content
        assert 'href="coverage.html"' in content
        assert 'href="review.html"' in content
        assert 'href="summary.html"' in content

    def test_active_class_on_dashboard(self, tmp_path: Path) -> None:
        """Dashboard template marks its own nav link as active."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        data: dict[str, Any] = {"project_name": "Active"}
        gen.render("dashboard.html", data, output)

        content = output.read_text()
        # The dashboard link should have the active class
        assert "active" in content

    def test_nav_hidden_in_print(self, tmp_path: Path) -> None:
        """Nav bar has no-print class for print media."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        data: dict[str, Any] = {"project_name": "Print"}
        gen.render("dashboard.html", data, output)

        content = output.read_text()
        assert "no-print" in content

    def test_nav_has_aria_label(self, tmp_path: Path) -> None:
        """Nav bar has aria-label for accessibility."""
        gen = ReportGenerator()
        output = tmp_path / "out.html"
        data: dict[str, Any] = {"project_name": "A11y"}
        gen.render("dashboard.html", data, output)

        content = output.read_text()
        assert 'aria-label="Report navigation"' in content
