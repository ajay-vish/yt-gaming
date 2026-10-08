#!/usr/bin/env python3
"""
Daily YouTube Studio Counter Automation Pipeline.
Generates and schedules 1 YouTube Short daily celebrating progressive subscriber milestones.
Randomly picks an optimal upload slot: Morning 8:00 AM IST, Evening 5:30 PM IST, or Evening 8:30 PM IST.
Progressively scales milestone increments so each video's subscriber jump is greater than the last.
"""

import json
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Paths
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
STATE_FILE = REPO_ROOT / "state.json"
WORK_DIR = REPO_ROOT / "work"
DRAFTS_DIR = REPO_ROOT / "drafts"
ASSETS_DIR = REPO_ROOT / "assets"

# Timezone & Slots
try:
    IST = ZoneInfo("Asia/Kolkata")
except Exception:
    IST = timezone(timedelta(hours=5, minutes=30))

# Random Daily Slots: Morning 8:00 AM, Evening 5:30 PM, Evening 8:30 PM IST
DAILY_SLOTS_IST = [
    (8, 0),    # Morning 8:00 AM IST
    (17, 30),  # Evening 5:30 PM IST
    (20, 30),  # Evening 8:30 PM IST
]

DEFAULT_CHANNEL_NAME = "ASK Gaming"
DEFAULT_CHANNEL_HANDLE = "@askgaming"
DEFAULT_TAGS = [
    "ask gaming", "gaming", "gamer", "subscriber count", "youtube studio",
    "live sub counter", "shorts", "youtube shorts", "milestone", "viral gaming",
    "road to 10k", "celebration", "subscribers", "gameplay", "gaming shorts"
]


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    else:
        state = {}

    state.setdefault("channel_name", DEFAULT_CHANNEL_NAME)
    state.setdefault("channel_handle", DEFAULT_CHANNEL_HANDLE)
    state.setdefault("current_subscribers", 5)
    state.setdefault("last_increment", 0)
    state.setdefault("video_index", 0)
    state.setdefault("scheduled_slots", [])
    state.setdefault("uploaded_videos", [])
    state.setdefault("pending_comments", {})
    return state


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def compute_next_milestone(current_subs: int, last_increment: int = 0) -> tuple[int, int]:
    """
    Computes (start_count, target_count) ensuring each video's increase is greater
    than the previous video's increase with realistic jitter.
    Progression tiers:
      1. ~5 -> ~100 (gain ~95)
      2. ~100 -> ~250 (gain ~150)
      3. ~250 -> ~500 (gain ~250)
      4. ~500 -> ~1,000 (gain ~500)
      5. ~1,000 -> ~2,000 (gain ~1,000)
      6. ~2,000 -> ~3,500 (gain ~1,500)
      ...
    """
    start_count = current_subs if current_subs > 0 else 5

    if start_count < 50:
        target_count = random.choice([95, 100, 105])
    elif start_count < 180:
        gain = random.randint(140, 165)  # target ~250
        target_count = start_count + gain
    elif start_count < 380:
        gain = random.randint(235, 275)  # target ~500
        target_count = start_count + gain
    elif start_count < 750:
        gain = random.randint(475, 535)  # target ~1000
        target_count = start_count + gain
    elif start_count < 1600:
        gain = random.randint(950, 1100)  # target ~2000
        target_count = start_count + gain
    elif start_count < 3000:
        gain = random.randint(1400, 1650)  # target ~3500
        target_count = start_count + gain
    else:
        # Scale dynamically ensuring gain > last_increment
        min_gain = max(last_increment + random.randint(250, 500), int(start_count * 0.45))
        gain = random.randint(min_gain, min_gain + 350)
        target_count = start_count + gain

    return start_count, target_count


def get_random_daily_slot(state: dict) -> str:
    """
    Selects 1 random slot from Morning 8:00 AM, Evening 5:30 PM, or Evening 8:30 PM IST.
    Guarantees exactly 1 upload per day without colliding with already scheduled slots.
    """
    now_utc = datetime.now(timezone.utc)
    # Prune passed slots from state
    state["scheduled_slots"] = [
        s for s in state["scheduled_slots"]
        if datetime.fromisoformat(s.replace("Z", "+00:00")) > now_utc
    ]
    taken = set(state["scheduled_slots"])

    now_ist = datetime.now(IST)
    today_ist = now_ist.date()

    # Shuffle the daily slots to pick randomly
    for day_offset in range(14):
        target_day = today_ist + timedelta(days=day_offset)
        
        # Check if this day already has an upload scheduled
        day_already_scheduled = False
        for s in taken:
            s_dt = datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(IST)
            if s_dt.date() == target_day:
                day_already_scheduled = True
                break
        if day_already_scheduled:
            continue

        # Shuffle the 3 candidate time slots
        candidate_slots = list(DAILY_SLOTS_IST)
        random.shuffle(candidate_slots)

        for hour, minute in candidate_slots:
            slot_ist = datetime(
                target_day.year, target_day.month, target_day.day,
                hour, minute, tzinfo=IST
            )
            slot_utc = slot_ist.astimezone(timezone.utc)

            # Ensure slot is at least 30 minutes in the future
            if slot_utc <= now_utc + timedelta(minutes=30):
                continue

            iso_utc = slot_utc.isoformat().replace("+00:00", "Z")
            if iso_utc not in taken:
                state["scheduled_slots"].append(iso_utc)
                print(f"[Slot Scheduler] Reserved 1 daily slot: {slot_ist.strftime('%Y-%m-%d %I:%M %p')} IST ({iso_utc})")
                return iso_utc

    raise RuntimeError("No available slot found in the next 14 days.")


def get_youtube_client():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")

    if not (refresh_token and client_id and client_secret):
        return None

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("youtube", "v3", credentials=creds)


def fetch_channel_stats(youtube) -> dict | None:
    """Fetches real-time channel statistics if YouTube API client is authenticated."""
    if not youtube:
        return None
    try:
        response = youtube.channels().list(mine=True, part="snippet,statistics").execute()
        items = response.get("items", [])
        if not items:
            return None
        ch = items[0]
        snippet = ch.get("snippet", {})
        stats = ch.get("statistics", {})
        return {
            "title": snippet.get("title", DEFAULT_CHANNEL_NAME),
            "customUrl": snippet.get("customUrl", DEFAULT_CHANNEL_HANDLE),
            "subscribers": int(stats.get("subscriberCount", 5)),
            "views": int(stats.get("viewCount", 0)),
            "videos": int(stats.get("videoCount", 0))
        }
    except Exception as e:
        print(f"[YouTube API] Warning fetching channel stats: {e}")
        return None


def generate_metadata(channel_name: str, start_count: int, target_count: int) -> tuple[str, str, list[str]]:
    """Generates viral title, description, and tags with Gemini or high-performing fallbacks."""
    api_key = os.environ.get("GEMINI_API_KEY", "")

    if api_key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            prompt = (
                f"You are a YouTube Shorts growth strategist for the gaming channel '{channel_name}'. "
                f"A new Short video was generated showing a real YouTube Studio screenshot animation "
                f"where subscriber count increases from {start_count:,} to {target_count:,} with celebration confetti.\n\n"
                f"Create viral YouTube Shorts metadata with high CTR and engagement.\n"
                f"Return JSON with exactly these 3 keys:\n"
                f"  'title': under 90 characters, emotional hook, milestone numbers, e.g. "
                f"'{target_count:,} Subscribers! We Did It! 🥹🎉 #Shorts #YouTubeStudio'\n"
                f"  'description': 3-4 short lines thanking subscribers, asking viewers to subscribe for next milestone, "
                f"and 8 viral hashtags including #Shorts, #YouTubeStudio, #SubscriberCounter, #{channel_name.replace(' ', '')}\n"
                f"  'tags': 15-20 relevant tags as array of strings."
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            data = json.loads(response.text)
            title = str(data.get("title", f"{target_count:,} Subscribers! Milestone Reached! 🥹🎉 #Shorts"))[:100]
            desc = str(data.get("description", ""))
            tags = [str(t) for t in data.get("tags", DEFAULT_TAGS)][:20]
            return title, desc, tags
        except Exception as e:
            print(f"[Gemini] Warning: {e}. Using optimized fallback metadata.")

    # High-performing fallback template
    title = f"{target_count:,} Subscribers Unlocked! Road to {target_count + 500:,}! 🥹🎉 #Shorts #YouTubeStudio"
    desc = (
        f"Thank you everyone for supporting {channel_name}! ❤️\n"
        f"We just hit {target_count:,} subscribers on YouTube Studio live!\n"
        f"Subscribe to be part of our next milestone! 🚀\n\n"
        f"#Shorts #YouTubeStudio #SubscriberCount #{channel_name.replace(' ', '')} #ViralShorts #Trending #LiveSubCount"
    )
    tags = DEFAULT_TAGS
    return title, desc, tags


def upload_video(video_path: Path, title: str, description: str, tags: list[str], publish_at: str, youtube) -> str:
    from googleapiclient.http import MediaFileUpload

    status = {
        "privacyStatus": "private",
        "publishAt": publish_at,
        "selfDeclaredMadeForKids": False,
    }

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "tags": tags,
            "categoryId": "24",  # Entertainment
            "defaultLanguage": "en",
        },
        "status": status,
    }

    media = MediaFileUpload(str(video_path), chunksize=-1, resumable=True, mimetype="video/mp4")
    response = youtube.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    return response["id"]


def run_pipeline(force_counts: tuple[int, int] = None) -> int:
    state = load_state()
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Reserve 1 random daily slot
    try:
        publish_at = get_random_daily_slot(state)
    except RuntimeError as e:
        print(f"[Scheduler] {e}")
        return 0

    # 2. Channel & Progressive Subscriber calculation
    youtube = get_youtube_client()
    live_stats = fetch_channel_stats(youtube) if youtube else None

    channel_name = live_stats["title"] if live_stats else state.get("channel_name", DEFAULT_CHANNEL_NAME)
    channel_handle = live_stats["customUrl"] if live_stats else state.get("channel_handle", DEFAULT_CHANNEL_HANDLE)

    if force_counts:
        start_count, target_count = force_counts
    else:
        current_subs = state.get("current_subscribers", 5)
        last_increment = state.get("last_increment", 0)
        start_count, target_count = compute_next_milestone(current_subs, last_increment)

    increment = target_count - start_count

    print("=" * 70)
    print(f"Channel: {channel_name} ({channel_handle})")
    print(f"Video #{state.get('video_index', 0) + 1} Progression: {start_count:,} -> {target_count:,} (+{increment:,} subs)")
    print(f"Target Upload Slot: {publish_at}")
    print("=" * 70)

    # 3. Render Video
    from render_video import render_counter_video
    video_out = WORK_DIR / f"counter_{target_count}_{int(datetime.now().timestamp())}.mp4"
    
    render_counter_video(
        template_name="ask_studio",
        channel_name=channel_name,
        channel_handle=channel_handle,
        start_count=start_count,
        end_count=target_count,
        duration_sec=14.0,
        hold_start_sec=2.0,
        hold_end_sec=3.5,
        mode="journey",
        theme="auto",
        milestone_message=f"{target_count:,} SUBSCRIBERS UNLOCKED!",
        output_path=video_out,
        include_sound=True,
        include_bgm=True
    )

    # 4. Generate AI Metadata
    title, desc, tags = generate_metadata(channel_name, start_count, target_count)
    
    # Save draft text
    draft_file = DRAFTS_DIR / f"draft_{target_count}.txt"
    draft_file.write_text(f"TITLE:\n{title}\n\nDESCRIPTION:\n{desc}\n\nTAGS:\n{', '.join(tags)}\n", encoding="utf-8")
    print(f"Saved metadata draft to {draft_file}")

    # 5. Upload to YouTube (if authenticated)
    if youtube:
        try:
            uploaded_id = upload_video(video_out, title, desc, tags, publish_at, youtube)
            print(f"Successfully uploaded! Video URL: https://youtu.be/{uploaded_id} (Scheduled for {publish_at})")
            state["uploaded_videos"].append({
                "video_id": uploaded_id,
                "title": title,
                "milestone": target_count,
                "publish_at": publish_at,
                "uploaded_at": datetime.now(timezone.utc).isoformat()
            })
        except Exception as e:
            print(f"[Upload Error] Could not upload to YouTube: {e}")
    else:
        print("\n[Notice] YouTube credentials not found in environment. Video rendered locally without upload.")
        print(f"Rendered video available at: {video_out}")

    # 6. Update state for progressive growth
    state["current_subscribers"] = target_count
    state["last_increment"] = increment
    state["video_index"] = state.get("video_index", 0) + 1
    save_state(state)
    print(f"State updated: Next starting subs = {target_count:,}, Last increment = +{increment:,}")
    return 0


if __name__ == "__main__":
    sys.exit(run_pipeline())
