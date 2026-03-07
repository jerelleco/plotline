"""
plotline.transcribe - Whisper transcription engine.

Pipeline Stage 2: Transcribe audio using faster-whisper (primary, CUDA/CPU)
or mlx-whisper (Apple Silicon). Produces segment-level transcripts with
word-level timestamps.
"""

from __future__ import annotations
