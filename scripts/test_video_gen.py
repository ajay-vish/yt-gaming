#!/usr/bin/env python3
"""
Test script to generate a sample YouTube Studio counter video locally.
Allows you to preview different subscriber counts, durations, modes, themes, and styles without uploading to YouTube.
"""

import argparse
import sys
from pathlib import Path

# Paths
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
WORK_DIR = REPO_ROOT / "work"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

if str(SCRIPTS_DIR) not in sys.path:
    sys.path.append(str(SCRIPTS_DIR))

from render_video import render_counter_video

def main():
    parser = argparse.ArgumentParser(
        description="Generate a sample subscriber counter video using the YouTube Studio template."
    )
    parser.add_argument(
        "--template",
        choices=["ask_studio", "mobile_studio", "live_counter"],
        default="ask_studio",
        help="Template style (default: ask_studio, matching your exact screenshot)."
    )
    parser.add_argument(
        "--channel-name",
        default="ASK Gaming",
        help="Display channel name."
    )
    parser.add_argument(
        "--channel-handle",
        default="@askgaming",
        help="Channel @handle."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=5,
        help="Starting subscriber count (default: 5)."
    )
    parser.add_argument(
        "--end",
        type=int,
        default=100,
        help="Ending milestone subscriber count (default: 100)."
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=14.0,
        help="Total video duration in seconds (recommended 12-15s for Shorts)."
    )
    parser.add_argument(
        "--mode",
        choices=["journey", "live"],
        default="journey",
        help="Video progression mode: 'journey' (multi-screenshot transitions) or 'live' (single countdown session)."
    )
    parser.add_argument(
        "--theme",
        choices=["auto", "light", "dark"],
        default="auto",
        help="Color theme for live stage: 'auto' (random), 'light', or 'dark'."
    )
    parser.add_argument(
        "--output",
        default="work/preview_studio_counter.mp4",
        help="Output video file path."
    )
    parser.add_argument(
        "--no-sound",
        action="store_true",
        help="Disable tick, shutter, and milestone chime audio effects."
    )
    parser.add_argument(
        "--no-bgm",
        action="store_true",
        help="Disable trending background music."
    )

    args = parser.parse_args()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.output).resolve()

    print("=" * 70)
    print("Generating YouTube Studio Counter Test Video")
    print("=" * 70)
    print(f"Template: {args.template}")
    print(f"Channel: {args.channel_name} ({args.channel_handle})")
    print(f"Counter: {args.start:,} -> {args.end:,}")
    print(f"Mode: {args.mode}")
    print(f"Theme: {args.theme}")
    print(f"Duration: {args.duration}s")
    print(f"Output: {out_path}")
    print("=" * 70)

    render_counter_video(
        template_name=args.template,
        channel_name=args.channel_name,
        channel_handle=args.channel_handle,
        start_count=args.start,
        end_count=args.end,
        duration_sec=args.duration,
        hold_start_sec=2.0,
        hold_end_sec=3.5,
        mode=args.mode,
        theme=args.theme,
        milestone_message=f"{args.end:,} SUBSCRIBERS UNLOCKED!",
        output_path=out_path,
        include_sound=not args.no_sound,
        include_bgm=not args.no_bgm
    )

if __name__ == "__main__":
    main()
