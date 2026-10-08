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

sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from gaming_titles import GAMING_TITLES_POOL
except ImportError:
    GAMING_TITLES_POOL = ["Epic Gaming Strategy & Highlights"]

AVAILABLE_THUMBS = [
    ASSETS_DIR / "thumbnails" / f"thumb_{i}.png" for i in range(1, 7)
    if (ASSETS_DIR / "thumbnails" / f"thumb_{i}.png").exists()
]
if not AVAILABLE_THUMBS:
    AVAILABLE_THUMBS = [ASSETS_DIR / "thumbnails" / "thumb_1.png"]

def build_random_cards(count: int = 3, avatar_uri: str = "") -> list[dict]:
    """Builds random gaming video cards sampled from 100 gaming titles and uploaded thumbnails."""
    titles = random.sample(GAMING_TITLES_POOL, min(count, len(GAMING_TITLES_POOL)))
    thumbs_pool = [t for t in AVAILABLE_THUMBS if t.exists()]
    if not thumbs_pool:
        thumbs_pool = AVAILABLE_THUMBS

    chosen_thumbs = random.sample(thumbs_pool, min(count, len(thumbs_pool)))
    while len(chosen_thumbs) < count:
        chosen_thumbs.append(random.choice(thumbs_pool))

    time_templates = [
        "First {h} hours, {m} minutes",
        "First {h} hours, {m} minutes",
        "First {d} days, {h} hours",
        "First {d} day, {h} hours",
        "First 48 minutes",
    ]

    cards = []
    for i in range(count):
        t = titles[i]
        thumb = chosen_thumbs[i]
        thumb_uri = thumb.resolve().as_uri() if thumb.exists() else avatar_uri

        v_views_num = round(random.uniform(2.1, 16.5), 1)
        v_likes_num = max(15, int(v_views_num * random.uniform(18, 28)))
        v_comments_num = max(5, int(v_likes_num * random.uniform(0.18, 0.32)))

        tpl = random.choice(time_templates)
        time_str = tpl.format(
            h=random.randint(1, 14),
            m=random.randint(4, 58),
            d=random.randint(1, 3)
        )
        cards.append({
            "title": t,
            "time": time_str,
            "thumbUrl": thumb_uri,
            "views": f"{v_views_num}k",
            "likes": str(v_likes_num),
            "comments": str(v_comments_num),
        })
    return cards

def generate_subs_progression(start_count: int, num_steps: int) -> list[int]:
    """Generates an authentic viral growth curve of subscriber counts up to start_count."""
    if start_count <= 50:
        base_start = max(1, int(start_count * 0.1))
    elif start_count <= 500:
        base_start = random.randint(10, 40)
    elif start_count <= 1500:
        base_start = random.randint(40, 100)
    else:
        base_start = random.randint(80, 160)

    points = [base_start]
    remaining = num_steps - 1
    for i in range(1, num_steps):
        ratio = (i / remaining) ** 1.6
        val = int(base_start + (start_count - base_start) * ratio)
        val = max(points[-1] + random.randint(10, 45), val)
        val = min(val, start_count - (remaining - i) * 2)
        points.append(val)
    return points

def generate_journey_steps(start_count: int, avatar_uri: str, num_steps: int = 6) -> list[dict]:
    """
    Generates multi-screenshot journey steps (each lasting exactly 0.5s).
    Every screenshot has 3 randomized gaming cards, realistic time, battery, theme, and sub count.
    """
    steps_subs = generate_subs_progression(start_count, num_steps)
    steps = []

    for i in range(num_steps):
        subs_val = steps_subs[i]
        theme_val = "light" if i % 2 == 0 else "dark"
        hour_val = random.randint(8, 11) if theme_val == "dark" else random.randint(1, 5)
        min_val = random.randint(5, 55)
        battery_val = random.randint(30, 95)

        ch_views = subs_val * random.uniform(90, 140)
        views_str = f"{ch_views / 1000:.1f}k" if ch_views >= 1000 else f"{int(ch_views)}"

        ch_watch = ch_views * random.uniform(0.007, 0.011)
        watch_str = f"{ch_watch / 1000:.1f}k" if ch_watch >= 1000 else f"{int(ch_watch)}"

        subs_gain_val = max(1, int(subs_val * random.uniform(0.35, 0.65)))

        cards = build_random_cards(3, avatar_uri)

        steps.append({
            "timeHour": hour_val,
            "timeMin": min_val,
            "theme": theme_val,
            "battery": battery_val,
            "subs": subs_val,
            "views": views_str,
            "watch": watch_str,
            "subsGain": f"+{subs_gain_val}",
            "cards": cards,
            # Top-level backwards compatibility fields
            "title": cards[0]["title"],
            "videoTime": cards[0]["time"],
            "thumbUrl": cards[0]["thumbUrl"],
            "vViews": cards[0]["views"],
            "vLikes": cards[0]["likes"],
            "vComments": cards[0]["comments"]
        })

    return steps

CLICKBAIT_PHRASES = [
    "USE THIS SOUND!",
    "🤑\nUSE THIS SOUND!",
    "Use this audio to gain 1M views",
    "Use this audio to gain 100K Subs",
    "Use this audio to get 1M views in 24 hours 📈",
    "Use this audio to blow up your channel 🚀",
    "Use this sound to get 10M views instantly ⚡",
    "Use this sound to gain 100K Subs this week 🔥",
    "Use this audio to go viral overnight ✨",
    "Use this sound to gain 50K Subs today 🎯",
    "Use this audio for instant 1M views 🤯",
]

def render_counter_video(
    template_name: str = "ask_studio",
    channel_name: str = "ASK Gaming",
    channel_handle: str = "@askgaming",
    avatar_path: str = None,
    video_thumb_path: str = None,
    start_count: int = 2157,
    end_count: int = 2200,
    duration_sec: float = None,
    hold_start_sec: float = None,
    hold_end_sec: float = None,
    milestone_message: str = None,
    clickbait_text: str = None,
    mode: str = "journey",
    theme: str = "auto",
    show_poll: bool = True,
    poll_question: str = "Will you subscribe?",
    poll_opt1: str = "Yes",
    poll_opt2: str = "No but I'll like",
    poll_votes: str = "0 votes",
    base_views: float = None,
    base_watch_time: float = None,
    base_subs_gain: int = None,
    revenue: str = "₹0",
    output_path: Path = None,
    include_sound: bool = True,
    include_bgm: bool = True
) -> Path:
    from playwright.sync_api import sync_playwright

    # Default duration 5.5s (3.5s journey at 0.5s/step + 2.0s frozen final milestone)
    if duration_sec is None:
        duration_sec = 5.5

    if hold_end_sec is None:
        hold_end_sec = 2.0
    else:
        hold_end_sec = min(hold_end_sec, round(duration_sec * 0.4, 1))

    if hold_start_sec is None:
        hold_start_sec = 0.5

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

    # Generate 3 random gaming cards for final milestone stage
    final_cards = build_random_cards(3, avatar_file.as_uri())
    chosen_card = final_cards[0]
    extra_videos_data = final_cards[1:]

    thumb_file = Path(video_thumb_path).resolve() if video_thumb_path and Path(video_thumb_path).exists() else avatar_file

    if not milestone_message:
        milestone_message = f"{end_count:,} SUBSCRIBERS UNLOCKED!"

    # Theme selection for the live recording stage
    if theme in ("dark", "light"):
        live_theme = theme
    else:
        live_theme = "light" if template_name == "ask_studio" else random.choice(["dark", "light"])

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

    # Select random trending background song from assets/sounds/bgm/
    bgm_pool = list((SOUNDS_DIR / "bgm").glob("*.mp3"))
    if bgm_pool:
        bgm_sound = random.choice(bgm_pool)
        print(f"🎵 Using trending background track: {bgm_sound.name}")
    else:
        bgm_sound = SOUNDS_DIR / "bgm_trending.mp3"

    if include_sound and (not tick_sound.exists() or not ding_sound.exists() or not shutter_sound.exists()):
        from sound_synth import build_all_sounds
        build_all_sounds()

    # Clickbait banner text
    if not clickbait_text:
        clickbait_text = random.choice(CLICKBAIT_PHRASES)

    # Journey steps (each step lasts exactly 0.5s)
    journey_steps = []
    if mode == "journey":
        journey_duration = max(1.5, duration_sec - hold_end_sec)
        num_steps = max(3, int(round(journey_duration / 0.5)))
        journey_steps = generate_journey_steps(start_count, avatar_file.as_uri(), num_steps=num_steps)

    config_data = {
        "mode": mode,
        "theme": live_theme,
        "channelName": channel_name,
        "channelHandle": channel_handle,
        "avatarUrl": avatar_file.as_uri(),
        "videoThumbUrl": chosen_card["thumbUrl"],
        "startCount": start_count,
        "endCount": end_count,
        "durationSec": duration_sec,
        "holdStartSec": hold_start_sec,
        "holdEndSec": hold_end_sec,
        "clickbaitText": clickbait_text,
        "finalCards": final_cards,
        "extraVideos": extra_videos_data,
        "baseViews": base_views,
        "baseWatchTime": base_watch_time,
        "baseSubsGain": base_subs_gain,
        "revenue": revenue,
        "recentVideoTitle": chosen_card["title"],
        "recentVideoTime": chosen_card["time"],
        "ranking": "1 of 10 ›",
        "baseVideoViews": float(chosen_card["views"].replace("k", "")),
        "baseVideoLikes": int(chosen_card["likes"]),
        "videoComments": int(chosen_card["comments"]),
        "ctr": f"{random.uniform(12.5, 17.5):.1f}%",
        "avd": f"{random.randint(2, 4)}:{random.randint(10, 59):02d}",
        "startTimeHour": live_hour,
        "startTimeMinute": live_minute,
        "batteryPercent": live_battery,
        "milestoneMessage": milestone_message,
        "showPoll": show_poll,
        "pollQuestion": poll_question,
        "pollOption1": poll_opt1,
        "pollOption2": poll_opt2,
        "pollVotes": poll_votes,
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
        inputs = ["-ss", "0.50", "-i", str(recorded_raw_video), "-i", str(tick_sound), "-i", str(ding_sound)]
        
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
                filter_parts.append(f"[{shutter_input_idx}:a]adelay={t_ms}|{t_ms},volume=0.45[{label}]")
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

        # 3. Anticipation Riser (only if active count-up ticks exist)
        if riser_input_idx is not None and tick_events:
            riser_delay_ms = max(1, int((milestone_sec - 1.1) * 1000))
            filter_parts.append(f"[{riser_input_idx}:a]adelay={riser_delay_ms}|{riser_delay_ms},volume=0.45[riser_delayed]")
            mix_inputs.append("[riser_delayed]")

        # 4. Milestone Chime Ding
        ding_delay_ms = max(1, int(milestone_sec * 1000))
        filter_parts.append(f"[2:a]adelay={ding_delay_ms}|{ding_delay_ms},volume=1.0[ding_delayed]")
        mix_inputs.append("[ding_delayed]")

        # 5. Trending Shorts Background Music (trimmed with volume control & gentle fade-out)
        if bgm_input_idx is not None:
            fade_duration = min(0.8, round(duration_sec * 0.1, 2))
            fade_start = max(0.5, duration_sec - fade_duration)
            filter_parts.append(f"[{bgm_input_idx}:a]atrim=0:{duration_sec},volume=0.42,afade=t=out:st={fade_start:.2f}:d={fade_duration:.2f}[bgm_out]")
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
            "-ss", "0.50",
            "-i", str(recorded_raw_video),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "fast",
            "-t", str(duration_sec),
            str(output_path)
        ]

    subprocess.run(cmd, check=True)

    # Save matching metadata JSON alongside the video
    try:
        from metadata_generator import generate_video_metadata
        bgm_name = bgm_sound.stem if 'bgm_sound' in locals() and bgm_sound else "viral_sound"
        meta = generate_video_metadata(
            channel_name=channel_name,
            channel_handle=channel_handle,
            target_subs=end_count,
            song_name=bgm_name
        )
        meta_path = output_path.with_suffix(".json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        print(f"📝 Upload metadata saved to: {meta_path}")
    except Exception as e:
        print(f"Warning: Could not save metadata: {e}")

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
    parser.add_argument("--duration", type=float, default=None, help="Video duration in seconds (random 5-10s if omitted).")
    parser.add_argument("--mode", choices=["journey", "live"], default="journey", help="Video progression mode.")
    parser.add_argument("--theme", choices=["auto", "light", "dark"], default="auto", help="App color theme.")
    parser.add_argument("--milestone-message", default=None, help="Celebration banner message.")
    parser.add_argument("--clickbait-text", default=None, help="Bold viral text overlay (e.g. 'Use this audio to gain 1M views').")
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
        clickbait_text=args.clickbait_text,
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
