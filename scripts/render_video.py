#!/usr/bin/env python3
"""
YouTube Studio Counter Video Renderer.
Renders pixel-perfect 1080x1920 YouTube Shorts videos using Playwright + HTML5/CSS/JS + FFmpeg.
Combines visual subscriber counter animations with synchronized tick, shutter, milestone chime,
and trending background music effects.
"""

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Paths
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
ASSETS_DIR = REPO_ROOT / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
WORK_DIR = REPO_ROOT / "work"

def get_ffmpeg_exe() -> str:
    """Finds ffmpeg binary from PATH, imageio_ffmpeg, or environment."""
    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        return ffmpeg_in_path
    env_ffmpeg = os.environ.get("FFMPEG_PATH")
    if env_ffmpeg and Path(env_ffmpeg).exists():
        return env_ffmpeg
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    raise RuntimeError("FFmpeg executable could not be found. Run: pip install imageio-ffmpeg")

RANDOM_VIDEOS_POOL = [
    {
        "title": "Insane 1v4 Clutch Win! Ranked Match Gameplay",
        "time": "First 3 hours, 58 minutes",
        "thumbnail": ASSETS_DIR / "thumbnails" / "thumb_1.png",
        "ranking": "2 of 10 ›",
        "views": 2.4,
        "likes": 29,
        "comments": 21,
        "ctr": "13.3%",
        "avd": "2:19",
    },
    {
        "title": "GTA 6 Official Gameplay Leaks Breakdown & Secrets",
        "time": "First 5 hours, 12 minutes",
        "thumbnail": ASSETS_DIR / "thumbnails" / "thumb_2.png",
        "ranking": "1 of 10 ›",
        "views": 8.7,
        "likes": 142,
        "comments": 68,
        "ctr": "16.8%",
        "avd": "3:42",
    },
    {
        "title": "I Survived 100 Days in Hardcore Minecraft (World Tour)",
        "time": "First 1 day, 2 hours",
        "thumbnail": ASSETS_DIR / "thumbnails" / "thumb_3.png",
        "ranking": "1 of 10 ›",
        "views": 14.2,
        "likes": 310,
        "comments": 124,
        "ctr": "18.2%",
        "avd": "5:15",
    },
    {
        "title": "Zero Recoil Secret Weapon Loadout! (After Season Update)",
        "time": "First 4 hours, 45 minutes",
        "thumbnail": ASSETS_DIR / "thumbnails" / "thumb_4.png",
        "ranking": "3 of 10 ›",
        "views": 4.1,
        "likes": 88,
        "comments": 35,
        "ctr": "12.4%",
        "avd": "2:54",
    },
    {
        "title": "Unbeaten 10 Win Streak to Radiant Rank (Full Gameplay)",
        "time": "First 6 hours, 20 minutes",
        "thumbnail": ASSETS_DIR / "thumbnails" / "thumb_5.png",
        "ranking": "2 of 10 ›",
        "views": 6.8,
        "likes": 195,
        "comments": 52,
        "ctr": "14.9%",
        "avd": "3:18",
    },
]

def generate_journey_steps(start_count: int, avatar_uri: str) -> list[dict]:
    """
    Generates 3 realistic previous milestone snapshot steps that lead up to start_count.
    Each snapshot has:
      - realistic lower sub counts (starting from low numbers)
      - realistic timestamps (morning, afternoon, evening)
      - realistic themes (light / dark)
      - realistic battery levels
      - random title and thumbnail from pool
    """
    if start_count <= 25:
        s1 = 1
        s2 = max(2, int(start_count * 0.35))
        s3 = max(3, int(start_count * 0.70))
    elif start_count <= 105:
        s1 = random.randint(3, 7)       # e.g. 5
        s2 = random.randint(18, 32)     # e.g. 25
        s3 = random.randint(55, 75)     # e.g. 68
    elif start_count <= 270:
        s1 = random.randint(8, 16)      # e.g. 12
        s2 = random.randint(50, 85)     # e.g. 70
        s3 = random.randint(140, 185)   # e.g. 165
    elif start_count <= 550:
        s1 = random.randint(15, 30)     # e.g. 24
        s2 = random.randint(110, 160)   # e.g. 135
        s3 = random.randint(280, 360)   # e.g. 320
    elif start_count <= 1100:
        s1 = random.randint(25, 55)     # e.g. 40
        s2 = random.randint(220, 340)   # e.g. 280
        s3 = random.randint(620, 780)   # e.g. 710
    else:
        s1 = random.randint(80, 160)    # e.g. 140
        s2 = random.randint(450, 750)   # e.g. 620
        s3 = random.randint(int(start_count * 0.60), int(start_count * 0.75)) # e.g. 1450

    steps_subs = [s1, s2, s3]
    sampled_vids = random.sample(RANDOM_VIDEOS_POOL, 3)

    step_configs = [
        {"theme": "light", "hour": random.randint(8, 10), "min": random.randint(5, 50), "battery": random.randint(88, 96), "time_label": "First 2 days, 4 hours"},
        {"theme": random.choice(["light", "dark"]), "hour": random.randint(1, 4), "min": random.randint(5, 50), "battery": random.randint(60, 74), "time_label": "First 1 day, 6 hours"},
        {"theme": "dark", "hour": random.randint(8, 11), "min": random.randint(5, 50), "battery": random.randint(32, 46), "time_label": "First 8 hours, 20 minutes"}
    ]

    steps = []
    for i in range(3):
        subs_val = steps_subs[i]
        vid = sampled_vids[i]
        cfg = step_configs[i]

        ch_views = subs_val * random.uniform(90, 140)
        views_str = f"{ch_views / 1000:.1f}k" if ch_views >= 1000 else f"{int(ch_views)}"

        ch_watch = ch_views * random.uniform(0.007, 0.011)
        watch_str = f"{ch_watch / 1000:.1f}k" if ch_watch >= 1000 else f"{int(ch_watch)}"

        subs_gain_val = max(1, int(subs_val * random.uniform(0.35, 0.65)))

        v_views = max(100, int(subs_val * random.uniform(4, 9)))
        v_views_str = f"{v_views / 1000:.1f}k" if v_views >= 1000 else f"{v_views}"
        v_likes = max(2, int(v_views * 0.016))
        v_comments = max(1, int(v_likes * 0.35))

        thumb_asset = vid["thumbnail"]
        thumb_uri = thumb_asset.resolve().as_uri() if thumb_asset.exists() else avatar_uri

        steps.append({
            "timeHour": cfg["hour"],
            "timeMin": cfg["min"],
            "theme": cfg["theme"],
            "battery": cfg["battery"],
            "subs": subs_val,
            "views": views_str,
            "watch": watch_str,
            "subsGain": f"+{subs_gain_val}",
            "title": vid["title"],
            "videoTime": cfg["time_label"],
            "thumbUrl": thumb_uri,
            "vViews": v_views_str,
            "vLikes": v_likes,
            "vComments": v_comments
        })

    return steps

def render_counter_video(
    template_name: str = "ask_studio",
    channel_name: str = "ASK Gaming",
    channel_handle: str = "@askgaming",
    avatar_path: str = None,
    video_thumb_path: str = None,
    start_count: int = 2151,
    end_count: int = 2200,
    duration_sec: float = 14.0,
    hold_start_sec: float = 2.0,
    hold_end_sec: float = 3.5,
    milestone_message: str = None,
    mode: str = "journey",
    theme: str = "auto",
    base_views: float = None,
    base_watch_time: float = None,
    base_subs_gain: int = None,
    revenue: str = "₹0",
    output_path: Path = None,
    include_sound: bool = True,
    include_bgm: bool = True
) -> Path:
    from playwright.sync_api import sync_playwright

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    if output_path is None:
        output_path = WORK_DIR / f"studio_sub_counter_{end_count}.mp4"
    output_path = Path(output_path).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    template_file = TEMPLATES_DIR / f"{template_name}.html"
    if not template_file.exists():
        template_file = TEMPLATES_DIR / "ask_studio.html"

    # Avatar fallback
    channel_avatar_asset = ASSETS_DIR / "channel_avatar.png"
    if avatar_path and Path(avatar_path).exists():
        avatar_file = Path(avatar_path).resolve()
    elif channel_avatar_asset.exists():
        avatar_file = channel_avatar_asset.resolve()
    else:
        avatar_file = (ASSETS_DIR / "default_avatar.png").resolve()

    # Pick random recent video card from pool
    chosen_video = random.choice(RANDOM_VIDEOS_POOL)
    thumb_path = chosen_video["thumbnail"]
    if video_thumb_path and Path(video_thumb_path).exists():
        thumb_file = Path(video_thumb_path).resolve()
    elif thumb_path.exists():
        thumb_file = thumb_path.resolve()
    elif (ASSETS_DIR / "video_thumb.png").exists():
        thumb_file = (ASSETS_DIR / "video_thumb.png").resolve()
    else:
        thumb_file = avatar_file

    if not milestone_message:
        milestone_message = f"{end_count:,} SUBSCRIBERS UNLOCKED!"

    # Theme selection for the live recording stage
    if theme in ("dark", "light"):
        live_theme = theme
    else:
        live_theme = random.choice(["dark", "light"])

    # Clock time and battery for live stage
    if live_theme == "dark":
        live_hour = random.choice([9, 10, 11, 1])
        live_minute = random.randint(12, 49)
        live_battery = random.randint(28, 52)
    else:
        live_hour = random.choice([8, 10, 11, 2, 4])
        live_minute = random.randint(12, 49)
        live_battery = random.randint(62, 88)

    # Base channel metrics scaled to sub size if not explicitly provided
    if base_views is None:
        base_views = round(max(5.0, (start_count * random.uniform(130, 165)) / 1000.0), 1)
    if base_watch_time is None:
        base_watch_time = round(max(0.2, base_views * random.uniform(0.007, 0.009)), 1)
    if base_subs_gain is None:
        base_subs_gain = max(2, int(start_count * random.uniform(0.22, 0.28)))

    # Ensure sound files exist
    tick_sound = SOUNDS_DIR / "tick.wav"
    ding_sound = SOUNDS_DIR / "milestone_ding.wav"
    riser_sound = SOUNDS_DIR / "riser.wav"
    shutter_sound = SOUNDS_DIR / "shutter.wav"
    bgm_sound = SOUNDS_DIR / "bgm_trending.mp3"

    if include_sound and (not tick_sound.exists() or not ding_sound.exists() or not shutter_sound.exists()):
        from sound_synth import build_all_sounds
        build_all_sounds()

    # Journey steps
    journey_steps = []
    if mode == "journey":
        journey_steps = generate_journey_steps(start_count, avatar_file.as_uri())

    config_data = {
        "mode": mode,
        "theme": live_theme,
        "channelName": channel_name,
        "channelHandle": channel_handle,
        "avatarUrl": avatar_file.as_uri(),
        "videoThumbUrl": thumb_file.as_uri(),
        "startCount": start_count,
        "endCount": end_count,
        "durationSec": duration_sec,
        "holdStartSec": hold_start_sec,
        "holdEndSec": hold_end_sec,
        "baseViews": base_views,
        "baseWatchTime": base_watch_time,
        "baseSubsGain": base_subs_gain,
        "revenue": revenue,
        "recentVideoTitle": chosen_video["title"],
        "recentVideoTime": chosen_video["time"],
        "ranking": chosen_video["ranking"],
        "baseVideoViews": chosen_video["views"],
        "baseVideoLikes": chosen_video["likes"],
        "videoComments": chosen_video["comments"],
        "ctr": chosen_video["ctr"],
        "avd": chosen_video["avd"],
        "startTimeHour": live_hour,
        "startTimeMinute": live_minute,
        "batteryPercent": live_battery,
        "milestoneMessage": milestone_message,
        "journeySteps": journey_steps
    }

    temp_record_dir = WORK_DIR / f"temp_rec_{int(time.time()*1000)}"
    temp_record_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎬 Starting Playwright video capture ({template_name}, {start_count:,} -> {end_count:,}, theme={live_theme}, mode={mode})...")

    with sync_playwright() as p:
        # Detect Edge or Chromium
        browser_channel = "msedge" if os.name == "nt" and (shutil.which("msedge") or Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe").exists()) else None
        
        try:
            if browser_channel:
                browser = p.chromium.launch(channel=browser_channel, headless=True)
            else:
                browser = p.chromium.launch(headless=True)
        except Exception:
            browser = p.chromium.launch(headless=True)

        context = browser.new_context(
            record_video_dir=str(temp_record_dir),
            record_video_size={"width": 1080, "height": 1920},
            viewport={"width": 1080, "height": 1920},
            device_scale_factor=1
        )

        # Inject config BEFORE navigating so that config is available instantly
        context.add_init_script(f"window.CONFIG = {json.dumps(config_data)};")

        page = context.new_page()

        # Load template
        template_uri = template_file.as_uri()
        page.goto(template_uri)

        # Wait for animation duration
        wait_ms = int((duration_sec + 0.6) * 1000)
        page.wait_for_timeout(wait_ms)

        # Extract timing events for audio sync
        tick_events = page.evaluate("window.TICK_EVENTS || []")
        shutter_events = page.evaluate("window.SHUTTER_EVENTS || []")
        milestone_time_ms = page.evaluate("window.MILESTONE_TIME_MS || null")

        video_path = page.video.path()
        context.close()
        browser.close()

    recorded_raw_video = Path(video_path)
    if not recorded_raw_video.exists():
        raise RuntimeError("Failed to capture video from Playwright.")

    print(f"🎥 Raw video recorded. Post-processing with FFmpeg and mixing audio...")

    ffmpeg_exe = get_ffmpeg_exe()

    # Calculate milestone audio trigger time
    if milestone_time_ms is not None:
        milestone_sec = milestone_time_ms / 1000.0
    else:
        milestone_sec = duration_sec - hold_end_sec

    # Build audio filter graph if sounds are included
    if include_sound and tick_sound.exists() and ding_sound.exists():
        inputs = ["-i", str(recorded_raw_video), "-i", str(tick_sound), "-i", str(ding_sound)]
        
        # Audio indices:
        # 0: video
        # 1: tick.wav
        # 2: milestone_ding.wav
        next_idx = 3

        riser_input_idx = None
        if riser_sound.exists():
            inputs += ["-i", str(riser_sound)]
            riser_input_idx = next_idx
            next_idx += 1

        shutter_input_idx = None
        if shutter_sound.exists():
            inputs += ["-i", str(shutter_sound)]
            shutter_input_idx = next_idx
            next_idx += 1

        bgm_input_idx = None
        if include_bgm and bgm_sound.exists():
            inputs += ["-i", str(bgm_sound)]
            bgm_input_idx = next_idx
            next_idx += 1

        filter_parts = []
        mix_inputs = []

        # 1. Shutter camera clicks for snapshot transitions
        if shutter_input_idx is not None and shutter_events:
            for s_idx, ev in enumerate(shutter_events):
                t_ms = max(0, int(ev.get("timeMs", 0)))
                label = f"shutter_{s_idx}"
                filter_parts.append(f"[{shutter_input_idx}:a]adelay={t_ms}|{t_ms},volume=0.75[{label}]")
                mix_inputs.append(f"[{label}]")

        # 2. Sampled tick pops during live counter count-up
        if tick_events:
            step = max(1, len(tick_events) // 12)
            for idx, i in enumerate(range(0, len(tick_events), step)):
                t_sec = tick_events[i]["timeMs"] / 1000.0
                if t_sec < milestone_sec - 0.2:
                    delay_ms = max(1, int(t_sec * 1000))
                    label = f"tick_{idx}"
                    filter_parts.append(f"[1:a]adelay={delay_ms}|{delay_ms},volume=0.85[{label}]")
                    mix_inputs.append(f"[{label}]")

        # 3. Anticipation Riser
        if riser_input_idx is not None:
            riser_delay_ms = max(1, int((milestone_sec - 1.1) * 1000))
            filter_parts.append(f"[{riser_input_idx}:a]adelay={riser_delay_ms}|{riser_delay_ms},volume=0.45[riser_delayed]")
            mix_inputs.append("[riser_delayed]")

        # 4. Milestone Chime Ding
        ding_delay_ms = max(1, int(milestone_sec * 1000))
        filter_parts.append(f"[2:a]adelay={ding_delay_ms}|{ding_delay_ms},volume=1.0[ding_delayed]")
        mix_inputs.append("[ding_delayed]")

        # 5. Trending Shorts Background Music (trimmed with volume control & gentle fade-out)
        if bgm_input_idx is not None:
            fade_start = max(0.5, duration_sec - 0.9)
            filter_parts.append(f"[{bgm_input_idx}:a]atrim=0:{duration_sec},volume=0.28,afade=t=out:st={fade_start:.2f}:d=0.8[bgm_out]")
            mix_inputs.append("[bgm_out]")

        filter_parts.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:normalize=0:duration=longest[aout]")
        filter_complex = ";".join(filter_parts)

        cmd = [
            ffmpeg_exe, "-y",
            *inputs,
            "-filter_complex", filter_complex,
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration_sec),
            str(output_path)
        ]
    else:
        cmd = [
            ffmpeg_exe, "-y",
            "-i", str(recorded_raw_video),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
            "-t", str(duration_sec),
            str(output_path)
        ]

    subprocess.run(cmd, check=True)

    # Clean up temp recordings
    shutil.rmtree(temp_record_dir, ignore_errors=True)

    print(f"✨ Successfully rendered subscriber counter video: {output_path} ({output_path.stat().st_size / 1024 / 1024:.2f} MB)")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Render a YouTube Studio subscriber counter video.")
    parser.add_argument("--template", default="ask_studio", help="Template style.")
    parser.add_argument("--channel-name", default="ASK Gaming", help="Channel display name.")
    parser.add_argument("--channel-handle", default="@askgaming", help="Channel @handle.")
    parser.add_argument("--avatar", default=None, help="Path to channel avatar image.")
    parser.add_argument("--thumb", default=None, help="Path to video thumbnail image.")
    parser.add_argument("--start", type=int, default=2151, help="Starting subscriber count.")
    parser.add_argument("--end", type=int, default=2200, help="Target milestone subscriber count.")
    parser.add_argument("--duration", type=float, default=14.0, help="Video duration in seconds.")
    parser.add_argument("--mode", choices=["journey", "live"], default="journey", help="Video progression mode.")
    parser.add_argument("--theme", choices=["auto", "light", "dark"], default="auto", help="App color theme.")
    parser.add_argument("--milestone-message", default=None, help="Celebration banner message.")
    parser.add_argument("--views", type=float, default=None, help="Base views in thousands (e.g. 345.7).")
    parser.add_argument("--watch-time", type=float, default=None, help="Base watch time in thousands (e.g. 2.6).")
    parser.add_argument("--subs-metric", type=int, default=None, help="Base subscribers gain (e.g. 544).")
    parser.add_argument("--revenue", default="₹0", help="Analytics estimated revenue.")
    parser.add_argument("--output", default="work/test_counter.mp4", help="Output MP4 file path.")
    parser.add_argument("--no-sound", action="store_true", help="Disable audio effects.")
    parser.add_argument("--no-bgm", action="store_true", help="Disable background music.")

    args = parser.parse_args()

    render_counter_video(
        template_name=args.template,
        channel_name=args.channel_name,
        channel_handle=args.channel_handle,
        avatar_path=args.avatar,
        video_thumb_path=args.thumb,
        start_count=args.start,
        end_count=args.end,
        duration_sec=args.duration,
        mode=args.mode,
        theme=args.theme,
        milestone_message=args.milestone_message,
        base_views=args.views,
        base_watch_time=args.watch_time,
        base_subs_gain=args.subs_metric,
        revenue=args.revenue,
        output_path=Path(args.output),
        include_sound=not args.no_sound,
        include_bgm=not args.no_bgm
    )

if __name__ == "__main__":
    main()
