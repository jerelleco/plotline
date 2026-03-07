"""Tests for Spanish/multi-language support across the pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

from plotline.enrich.merge import merge_transcript_and_delivery
from plotline.llm.templates import build_language_instruction, detect_project_language


# ---------------------------------------------------------------------------
# build_language_instruction
# ---------------------------------------------------------------------------


class TestBuildLanguageInstruction:
    def test_returns_none_for_english(self) -> None:
        assert build_language_instruction("en") is None

    def test_returns_none_for_none(self) -> None:
        assert build_language_instruction(None) is None

    def test_returns_none_for_empty_string(self) -> None:
        assert build_language_instruction("") is None

    def test_returns_instruction_for_spanish(self) -> None:
        result = build_language_instruction("es")
        assert result is not None
        assert "Spanish" in result
        assert "segment IDs" in result

    def test_returns_instruction_for_french(self) -> None:
        result = build_language_instruction("fr")
        assert result is not None
        assert "French" in result

    def test_returns_instruction_for_unknown_code(self) -> None:
        """Unknown language codes should still produce an instruction using the code itself."""
        result = build_language_instruction("xx")
        assert result is not None
        assert "xx" in result

    def test_instruction_mentions_json_fields_in_english(self) -> None:
        result = build_language_instruction("es")
        assert result is not None
        assert "JSON field names" in result
        assert "English" in result


# ---------------------------------------------------------------------------
# detect_project_language
# ---------------------------------------------------------------------------


class TestDetectProjectLanguage:
    def test_returns_none_for_empty_manifest(self) -> None:
        manifest: dict[str, Any] = {"interviews": []}
        assert detect_project_language(manifest) is None

    def test_returns_none_when_no_detected_language(self) -> None:
        manifest: dict[str, Any] = {
            "interviews": [
                {"id": "interview_001", "stages": {}},
                {"id": "interview_002", "stages": {}},
            ]
        }
        assert detect_project_language(manifest) is None

    def test_returns_language_for_single_interview(self) -> None:
        manifest: dict[str, Any] = {
            "interviews": [
                {"id": "interview_001", "detected_language": "es"},
            ]
        }
        assert detect_project_language(manifest) == "es"

    def test_returns_language_when_all_agree(self) -> None:
        manifest: dict[str, Any] = {
            "interviews": [
                {"id": "interview_001", "detected_language": "es"},
                {"id": "interview_002", "detected_language": "es"},
                {"id": "interview_003", "detected_language": "es"},
            ]
        }
        assert detect_project_language(manifest) == "es"

    def test_returns_most_common_for_mixed(self) -> None:
        manifest: dict[str, Any] = {
            "interviews": [
                {"id": "interview_001", "detected_language": "es"},
                {"id": "interview_002", "detected_language": "es"},
                {"id": "interview_003", "detected_language": "en"},
            ]
        }
        assert detect_project_language(manifest) == "es"

    def test_ignores_interviews_without_detected_language(self) -> None:
        manifest: dict[str, Any] = {
            "interviews": [
                {"id": "interview_001", "detected_language": "fr"},
                {"id": "interview_002", "stages": {}},
            ]
        }
        assert detect_project_language(manifest) == "fr"

    def test_returns_english(self) -> None:
        manifest: dict[str, Any] = {
            "interviews": [
                {"id": "interview_001", "detected_language": "en"},
            ]
        }
        assert detect_project_language(manifest) == "en"


# ---------------------------------------------------------------------------
# Language preserved through enrichment
# ---------------------------------------------------------------------------


class TestLanguagePreservedInEnrichment:
    def test_merge_preserves_language(self) -> None:
        transcript = {
            "interview_id": "interview_001",
            "language": "es",
            "duration_seconds": 60.0,
            "segments": [
                {
                    "segment_id": "seg_001",
                    "start": 0.0,
                    "end": 5.0,
                    "text": "Hola mundo",
                    "words": [],
                    "confidence": 0.95,
                    "corrected": False,
                },
            ],
        }

        delivery = {
            "segments": [
                {
                    "segment_id": "seg_001",
                    "normalized": {},
                    "composite_score": 0.5,
                    "delivery_label": "moderate",
                },
            ],
        }

        result = merge_transcript_and_delivery(transcript, delivery)

        assert result["language"] == "es"

    def test_merge_preserves_language_none(self) -> None:
        transcript = {
            "interview_id": "interview_001",
            "duration_seconds": 60.0,
            "segments": [],
        }

        delivery = {"segments": []}

        result = merge_transcript_and_delivery(transcript, delivery)

        assert result["language"] is None

    def test_merge_preserves_english(self) -> None:
        transcript = {
            "interview_id": "interview_001",
            "language": "en",
            "duration_seconds": 60.0,
            "segments": [],
        }

        delivery = {"segments": []}

        result = merge_transcript_and_delivery(transcript, delivery)

        assert result["language"] == "en"


# ---------------------------------------------------------------------------
# Language injection in LLM passes
# ---------------------------------------------------------------------------


def _make_mock_client(response_data: dict[str, Any]) -> MagicMock:
    client = MagicMock()
    client.model = "test-model"
    client.complete.return_value = json.dumps(response_data)
    client.get_token_usage.return_value = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
    return client


def _make_mock_template_manager() -> MagicMock:
    tm = MagicMock()
    tm.format_transcript_for_prompt.return_value = "formatted transcript"
    tm.format_brief_for_prompt.return_value = "formatted brief"
    tm.render.return_value = "rendered prompt"
    return tm


class TestThemesLanguageInjection:
    def test_spanish_language_injected_into_variables(self) -> None:
        from plotline.llm.themes import extract_themes_for_interview

        client = _make_mock_client({"themes": []})
        tm = _make_mock_template_manager()

        segments_data = {
            "interview_id": "interview_001",
            "segments": [],
        }

        extract_themes_for_interview(
            segments=segments_data,
            client=client,
            template_manager=tm,
            language="es",
        )

        # Verify render was called with LANGUAGE_INSTRUCTION in variables
        call_args = tm.render.call_args
        variables = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("variables", {})
        assert "LANGUAGE_INSTRUCTION" in variables
        assert "Spanish" in variables["LANGUAGE_INSTRUCTION"]

    def test_english_language_not_injected(self) -> None:
        from plotline.llm.themes import extract_themes_for_interview

        client = _make_mock_client({"themes": []})
        tm = _make_mock_template_manager()

        segments_data = {
            "interview_id": "interview_001",
            "segments": [],
        }

        extract_themes_for_interview(
            segments=segments_data,
            client=client,
            template_manager=tm,
            language="en",
        )

        call_args = tm.render.call_args
        variables = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("variables", {})
        assert "LANGUAGE_INSTRUCTION" not in variables

    def test_none_language_not_injected(self) -> None:
        from plotline.llm.themes import extract_themes_for_interview

        client = _make_mock_client({"themes": []})
        tm = _make_mock_template_manager()

        segments_data = {
            "interview_id": "interview_001",
            "segments": [],
        }

        extract_themes_for_interview(
            segments=segments_data,
            client=client,
            template_manager=tm,
            language=None,
        )

        call_args = tm.render.call_args
        variables = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("variables", {})
        assert "LANGUAGE_INSTRUCTION" not in variables


class TestSynthesisLanguageInjection:
    def test_spanish_language_injected(self) -> None:
        from plotline.llm.synthesis import synthesize_themes

        client = _make_mock_client({"unified_themes": [], "best_takes": []})
        tm = _make_mock_template_manager()

        synthesize_themes(
            themes_data=[],
            client=client,
            template_manager=tm,
            interview_count=0,
            language="es",
        )

        call_args = tm.render.call_args
        variables = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("variables", {})
        assert "LANGUAGE_INSTRUCTION" in variables
        assert "Spanish" in variables["LANGUAGE_INSTRUCTION"]


class TestArcLanguageInjection:
    def test_spanish_language_injected(self) -> None:
        from plotline.llm.arc import build_narrative_arc

        client = _make_mock_client({"arc": []})
        tm = _make_mock_template_manager()
        config = MagicMock()
        config.target_duration_seconds = 600
        config.project_profile = "documentary"

        build_narrative_arc(
            synthesis={},
            all_segments=[],
            client=client,
            template_manager=tm,
            config=config,
            language="es",
        )

        call_args = tm.render.call_args
        variables = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("variables", {})
        assert "LANGUAGE_INSTRUCTION" in variables
        assert "Spanish" in variables["LANGUAGE_INSTRUCTION"]


class TestFlagsLanguageInjection:
    def test_spanish_language_injected(self) -> None:
        from plotline.llm.flags import flag_segments

        client = _make_mock_client({"flags": []})
        tm = _make_mock_template_manager()

        flag_segments(
            segments=[{"segment_id": "seg_001", "text": "Hola"}],
            client=client,
            template_manager=tm,
            language="es",
        )

        call_args = tm.render.call_args
        variables = call_args[0][1] if len(call_args[0]) > 1 else call_args[1].get("variables", {})
        assert "LANGUAGE_INSTRUCTION" in variables
        assert "Spanish" in variables["LANGUAGE_INSTRUCTION"]

    def test_empty_segments_skips_language(self) -> None:
        from plotline.llm.flags import flag_segments

        client = _make_mock_client({"flags": []})
        tm = _make_mock_template_manager()

        result = flag_segments(
            segments=[],
            client=client,
            template_manager=tm,
            language="es",
        )

        assert result == {"flags": []}
        tm.render.assert_not_called()
