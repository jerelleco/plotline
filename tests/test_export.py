"""Tests for plotline.export module."""

import pytest

from plotline.export.edl import generate_edl
from plotline.export.fcpxml import (
    generate_fcpxml,
    get_fcpxml_format,
    path_to_file_url,
    seconds_to_fcpxml_time,
)
from plotline.export.timecode import (
    frames_to_timecode,
    is_drop_frame_fps,
    seconds_to_timecode,
    timecode_to_frames,
    timecode_to_seconds,
)


class TestTimecode:
    def test_is_drop_frame_fps(self):
        assert is_drop_frame_fps(29.97) is True
        assert is_drop_frame_fps(23.976) is False
        assert is_drop_frame_fps(24) is False
        assert is_drop_frame_fps(25) is False
        assert is_drop_frame_fps(30) is False

    def test_seconds_to_timecode_24fps(self):
        tc = seconds_to_timecode(0, 24, drop_frame=False)
        assert tc == "00:00:00:00"

        tc = seconds_to_timecode(3600, 24, drop_frame=False)
        assert tc == "01:00:00:00"

        tc = seconds_to_timecode(65.5, 24, drop_frame=False)
        assert tc == "00:01:05:12"

    def test_seconds_to_timecode_2997_drop_frame(self):
        tc = seconds_to_timecode(0, 29.97, drop_frame=True)
        assert tc == "00:00:00;00"

        tc = seconds_to_timecode(60, 29.97, drop_frame=True)
        assert tc == "00:00:59;28"

    def test_timecode_to_seconds_24fps(self):
        assert timecode_to_seconds("00:00:00:00", 24) == 0
        assert timecode_to_seconds("01:00:00:00", 24) == 3600
        assert timecode_to_seconds("00:01:05:12", 24) == pytest.approx(65.5)

    def test_timecode_to_frames(self):
        assert timecode_to_frames("00:00:00:00", 24) == 0
        assert timecode_to_frames("00:00:01:00", 24) == 24
        assert timecode_to_frames("00:01:00:00", 24) == 1440

    def test_frames_to_timecode(self):
        assert frames_to_timecode(0, 24, drop_frame=False) == "00:00:00:00"
        assert frames_to_timecode(24, 24, drop_frame=False) == "00:00:01:00"
        assert frames_to_timecode(1440, 24, drop_frame=False) == "00:01:00:00"

    def test_df_timecode_round_trip_1_hour(self):
        """Verify drop-frame round-trip at 1 hour boundary is frame-accurate."""
        # 01:00:00;00 should convert to ~3600 seconds
        secs = timecode_to_seconds("01:00:00;00", 29.97)
        assert secs == pytest.approx(3600, abs=0.04)  # Within ~1 frame

        # And converting 3600s to timecode should give 01:00:00;00
        tc = seconds_to_timecode(3600, 29.97, drop_frame=True)
        assert tc == "01:00:00;00"

    def test_df_timecode_round_trip_2_hours(self):
        """Verify drop-frame round-trip at 2 hour boundary."""
        secs = timecode_to_seconds("02:00:00;00", 29.97)
        assert secs == pytest.approx(7200, abs=0.04)

        tc = seconds_to_timecode(7200, 29.97, drop_frame=True)
        assert tc == "02:00:00;00"

    def test_df_timecode_10_minutes(self):
        """Verify 10-minute boundary (no frame drop at 10th minute)."""
        secs = timecode_to_seconds("00:10:00;00", 29.97)
        assert secs == pytest.approx(600, abs=0.04)

        tc = seconds_to_timecode(600, 29.97, drop_frame=True)
        assert tc == "00:10:00;00"

    def test_df_source_timecode_offset_accuracy(self):
        """Simulate EDL export with DF start_timecode — the critical real-world scenario."""
        # Camera starts recording at 01:00:00;00
        # Segment is 10 seconds into the video
        offset = timecode_to_seconds("01:00:00;00", 29.97)
        absolute = offset + 10.0
        src_tc = seconds_to_timecode(absolute, 29.97, True)
        # Must produce 01:00:10;00, not 01:00:13;18 (the old buggy result)
        assert src_tc == "01:00:10;00"

    def test_ndf_23976_frame_accurate(self):
        """Verify 23.976 NDF timecodes are frame-accurate at key boundaries."""
        # Frame 24 at 23.976fps occurs at exactly 1001/24000 * 24 = 1.001 seconds
        tc = seconds_to_timecode(24 * 1001 / 24000, 23.976, drop_frame=False)
        assert tc == "00:00:01:00"

        # Frame 86400 = 1 hour of 24fps display = 3603.6 seconds at 23.976fps
        tc = seconds_to_timecode(86400 * 1001 / 24000, 23.976, drop_frame=False)
        assert tc == "01:00:00:00"


class TestEDL:
    def test_generate_edl_basic(self):
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 10.0,
                "end": 25.0,
                "role": "hook",
                "text": "This is a test segment",
                "editorial_notes": "Good take",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        edl = generate_edl(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
            handle_frames=12,
        )

        assert "TITLE: Plotline Selects - TestProject" in edl
        assert "NON-DROP FRAME" in edl
        assert "int-001" in edl or "R001" in edl
        assert "FROM CLIP NAME: interview1.mp4" in edl

    def test_generate_edl_includes_speaker_comment(self):
        """Test that EDL includes speaker comment when present."""
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 10.0,
                "end": 25.0,
                "role": "hook",
                "text": "Test segment",
                "speaker": "SPEAKER_00",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        edl = generate_edl(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert "* SPEAKER: SPEAKER_00" in edl

    def test_generate_edl_no_speaker_when_none(self):
        """Test that EDL omits speaker comment when not present."""
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 10.0,
                "end": 25.0,
                "role": "hook",
                "text": "Test segment",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        edl = generate_edl(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert "* SPEAKER:" not in edl

    def test_generate_edl_multiple_selections(self):
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 10.0,
                "end": 20.0,
                "role": "hook",
            },
            {
                "segment_id": "seg-2",
                "interview_id": "int-001",
                "start": 30.0,
                "end": 45.0,
                "role": "body",
            },
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        edl = generate_edl(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        lines = [line for line in edl.split("\n") if line.strip() and not line.startswith("*")]
        # Each event produces 3 lines: V, A1, A2 (standard CMX 3600)
        event_lines = [line for line in lines if line[0:3].strip().isdigit()]
        assert len(event_lines) == 6  # 2 events * 3 tracks (V, A1, A2)
        # Verify 2 distinct event numbers
        video_lines = [line for line in event_lines if "  V  " in line]
        assert len(video_lines) == 2

    def test_generate_edl_drop_frame(self):
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 0,
                "end": 10,
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 29.97,
                "duration_seconds": 120,
            }
        }

        edl = generate_edl(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert "DROP FRAME" in edl


class TestFCPXML:
    def test_seconds_to_fcpxml_time_24fps(self):
        time_str = seconds_to_fcpxml_time(1.0, 24)
        assert "s" in time_str

    def test_seconds_to_fcpxml_time_23976fps(self):
        time_str = seconds_to_fcpxml_time(1.0, 23.976)
        assert "s" in time_str

    def test_get_fcpxml_format_24fps(self):
        fmt = get_fcpxml_format(24)
        assert fmt["frameDuration"] == "100/2400s"
        assert "24" in fmt["name"]

    def test_get_fcpxml_format_2997fps(self):
        fmt = get_fcpxml_format(29.97)
        assert fmt["frameDuration"] == "1001/30000s"
        assert "2997" in fmt["name"]

    def test_path_to_file_url(self):
        from pathlib import Path

        url = path_to_file_url(Path("/Users/test/video.mp4"))
        assert url.startswith("file://")
        assert "video.mp4" in url

    def test_generate_fcpxml_basic(self):
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 10.0,
                "end": 25.0,
                "role": "hook",
                "text": "Test segment text",
                "themes": ["theme1", "theme2"],
                "delivery_label": "confident",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        fcpxml = generate_fcpxml(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert '<?xml version="1.0"' in fcpxml
        assert "fcpxml" in fcpxml
        assert "TestProject" in fcpxml
        assert "Plotline Selects" in fcpxml

    def test_generate_fcpxml_with_keywords(self):
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 0,
                "end": 10,
                "themes": ["journey", "transformation"],
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        fcpxml = generate_fcpxml(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert "keyword" in fcpxml
        assert "journey" in fcpxml or "transformation" in fcpxml

    def test_generate_fcpxml_includes_speaker_keyword(self):
        """Test that FCPXML includes speaker keyword when present."""
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 0,
                "end": 10,
                "speaker": "SPEAKER_00",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        fcpxml = generate_fcpxml(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert 'value="Speaker: SPEAKER_00"' in fcpxml

    def test_generate_fcpxml_speaker_in_clip_name(self):
        """Test that speaker is included in clip name."""
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 0,
                "end": 10,
                "speaker": "SPEAKER_01",
                "role": "hook",
                "text": "Test segment text here",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        fcpxml = generate_fcpxml(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert "SPEAKER_01" in fcpxml
        assert "Hook" in fcpxml

    def test_generate_fcpxml_no_speaker_keyword_when_none(self):
        """Test that FCPXML omits speaker keyword when not present."""
        selections = [
            {
                "segment_id": "seg-1",
                "interview_id": "int-001",
                "start": 0,
                "end": 10,
                "text": "Test segment",
            }
        ]
        interviews = {
            "int-001": {
                "id": "int-001",
                "filename": "interview1.mp4",
                "source_file": "/path/to/interview1.mp4",
                "frame_rate": 24,
                "duration_seconds": 120,
            }
        }

        fcpxml = generate_fcpxml(
            project_name="TestProject",
            selections=selections,
            interviews=interviews,
        )

        assert "Speaker:" not in fcpxml
