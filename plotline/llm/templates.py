"""
plotline.llm.templates - Prompt template loading and rendering.

Uses Jinja2 to load and render prompt templates from the project's
prompts/ directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template


class PromptTemplateManager:
    """Manages loading and rendering of prompt templates."""

    def __init__(self, prompts_dir: Path) -> None:
        self.prompts_dir = prompts_dir
        self.env = Environment(
            loader=FileSystemLoader(str(prompts_dir)),
            autoescape=False,
            keep_trailing_newline=True,
        )
        self._cache: dict[str, Template] = {}

    def get_template(self, name: str) -> Template:
        """Load a template by name.

        Args:
            name: Template filename (e.g., "themes.txt")

        Returns:
            Jinja2 Template object

        Raises:
            FileNotFoundError: If template doesn't exist
        """
        if name not in self._cache:
            template_path = self.prompts_dir / name
            if not template_path.exists():
                raise FileNotFoundError(f"Template not found: {template_path}")
            self._cache[name] = self.env.get_template(name)
        return self._cache[name]

    def render(
        self,
        template_name: str,
        variables: dict[str, Any],
    ) -> str:
        """Render a template with variables.

        Args:
            template_name: Template filename
            variables: Dict of template variables

        Returns:
            Rendered prompt string
        """
        template = self.get_template(template_name)
        return template.render(**variables)

    def list_templates(self) -> list[str]:
        """List available templates."""
        if not self.prompts_dir.exists():
            return []
        return [f.name for f in self.prompts_dir.glob("*.txt")]

    def format_transcript_for_prompt(self, segments: list[dict[str, Any]]) -> str:
        """Format enriched segments for LLM prompt."""
        return format_transcript_for_prompt(segments)

    def format_brief_for_prompt(self, brief: dict[str, Any]) -> str:
        """Format creative brief for LLM prompt."""
        return format_brief_for_prompt(brief)


def format_transcript_for_prompt(segments: list[dict[str, Any]]) -> str:
    """Format enriched segments for LLM prompt.

    Creates a readable transcript format with segment IDs, timecodes,
    speaker labels, and delivery labels.

    Args:
        segments: List of enriched segment dicts

    Returns:
        Formatted transcript string
    """
    lines = []

    for seg in segments:
        segment_id = seg.get("segment_id", "unknown")
        start = seg.get("start", 0)
        end = seg.get("end", 0)
        text = seg.get("text", "").strip()
        speaker = seg.get("speaker")
        delivery = seg.get("delivery", {})
        delivery_label = delivery.get("delivery_label", "")

        start_tc = format_timecode(start)
        end_tc = format_timecode(end)

        line = f"[{segment_id}] {start_tc} → {end_tc}"
        if speaker:
            line += f" | Speaker: {speaker}"
        if delivery_label:
            line += f" | Delivery: {delivery_label}"
        line += f'\n"{text}"\n'

        lines.append(line)

    return "\n".join(lines)


LANGUAGE_NAMES: dict[str, str] = {
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "nl": "Dutch",
    "pl": "Polish",
    "tr": "Turkish",
    "sv": "Swedish",
    "da": "Danish",
    "no": "Norwegian",
    "fi": "Finnish",
    "el": "Greek",
    "he": "Hebrew",
    "hi": "Hindi",
    "ca": "Catalan",
    "eu": "Basque",
    "gl": "Galician",
}


def build_language_instruction(language: str | None) -> str | None:
    """Build a language instruction for non-English transcripts.

    Returns an instruction string telling the LLM to output theme names,
    descriptions, and editorial notes in the transcript's language.
    Returns None for English or unknown languages.

    Args:
        language: ISO 639-1 language code (e.g., "es", "fr")

    Returns:
        Language instruction string, or None if not needed
    """
    if not language or language == "en":
        return None

    name = LANGUAGE_NAMES.get(language, language)
    return (
        f"LANGUAGE: This transcript is in {name}. "
        f"Provide all theme names, descriptions, emotional character descriptors, "
        f"and editorial notes in {name}. "
        f"Keep segment IDs, JSON field names, and structural labels in English."
    )


def detect_project_language(manifest: dict[str, Any]) -> str | None:
    """Detect the dominant language across all interviews in a project.

    Reads the ``detected_language`` field stored on each interview entry
    in the manifest (set during transcription).

    Args:
        manifest: Project manifest dict

    Returns:
        ISO 639-1 language code if all interviews agree, None otherwise
    """
    languages = [
        interview.get("detected_language")
        for interview in manifest.get("interviews", [])
        if interview.get("detected_language")
    ]

    if not languages:
        return None

    # If all interviews share the same language, use it
    if len(set(languages)) == 1:
        return languages[0]

    # Mixed languages — return the most common one
    from collections import Counter

    most_common = Counter(languages).most_common(1)[0][0]
    return most_common


def format_timecode(seconds: float) -> str:
    """Format seconds as HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_theme_map_for_prompt(themes_data: dict[str, Any]) -> str:
    """Format theme extraction results for synthesis prompt.

    Args:
        themes_data: themes.json content for an interview

    Returns:
        Formatted theme map string
    """
    lines = []

    interview_id = themes_data.get("interview_id", "unknown")
    lines.append(f"=== {interview_id} ===\n")

    for theme in themes_data.get("themes", []):
        name = theme.get("name", "Unnamed")
        description = theme.get("description", "")
        segment_ids = theme.get("segment_ids", [])
        strength = theme.get("strength", 0)
        emotional = theme.get("emotional_character", "")

        lines.append(f"THEME: {name}")
        lines.append(f"  Description: {description}")
        lines.append(f"  Strength: {strength:.2f}")
        if emotional:
            lines.append(f"  Emotional character: {emotional}")
        lines.append(f"  Segments: {', '.join(segment_ids[:5])}")
        if len(segment_ids) > 5:
            lines.append(f"           ... and {len(segment_ids) - 5} more")
        lines.append("")

    for intersection in themes_data.get("intersections", []):
        seg_id = intersection.get("segment_id", "")
        theme_list = intersection.get("themes", [])
        note = intersection.get("note", "")
        lines.append(f"INTERSECTION at {seg_id}: {', '.join(theme_list)}")
        if note:
            lines.append(f"  Note: {note}")
        lines.append("")

    return "\n".join(lines)


def format_synthesis_for_prompt(synthesis: dict[str, Any]) -> str:
    """Format synthesis results for arc prompt.

    Args:
        synthesis: synthesis.json content

    Returns:
        Formatted synthesis string
    """
    lines = []

    for theme in synthesis.get("unified_themes", []):
        name = theme.get("name", "Unnamed")
        description = theme.get("description", "")
        perspectives = theme.get("perspectives", "")
        seg_ids = theme.get("all_segment_ids", [])

        lines.append(f"UNIFIED THEME: {name}")
        lines.append(f"  {description}")
        if perspectives:
            lines.append(f"  Perspectives: {perspectives}")
        lines.append(f"  Total segments: {len(seg_ids)}")
        lines.append("")

    return "\n".join(lines)


def format_brief_for_prompt(brief: dict[str, Any]) -> str:
    """Format creative brief for LLM prompt.

    Args:
        brief: brief.json content

    Returns:
        Formatted brief string
    """
    lines = ["CREATIVE BRIEF", "=" * 40, ""]

    for msg in brief.get("key_messages", []):
        msg_id = msg.get("id", "")
        text = msg.get("text", "")
        lines.append(f"[{msg_id}] {text}")
    lines.append("")

    if brief.get("audience"):
        lines.append(f"TARGET AUDIENCE: {brief['audience']}")
        lines.append("")

    if brief.get("target_duration_seconds"):
        mins = brief["target_duration_seconds"] // 60
        lines.append(f"TARGET DURATION: {mins} minutes")
        lines.append("")

    if brief.get("tone_direction"):
        lines.append(f"TONE: {brief['tone_direction']}")
        lines.append("")

    if brief.get("must_include"):
        lines.append(f"MUST INCLUDE: {', '.join(brief['must_include'])}")
        lines.append("")

    if brief.get("avoid"):
        lines.append(f"AVOID: {', '.join(brief['avoid'])}")
        lines.append("")

    return "\n".join(lines)
