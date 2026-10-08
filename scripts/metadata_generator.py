"""
Metadata generator based on the viral formula of @tryingtogetfamous1979.
Generates high-CTR Titles, Descriptions, and Tags for YouTube Shorts.
"""

import random
import sys
from typing import Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Core Viral Title Formulas from @tryingtogetfamous1979
TITLE_TEMPLATES = [
    "Use this audio to get {sub_str} subs! 📈 #shorts",
    "This audio got me {sub_str} subs! 🔥 #shorts",
    "Try this audio to go viral! ⚡ #shorts",
    "Use this sound for 1M views! 🤯 #shorts",
    "{views_str} views from this sound! 😮 #shorts",
    "This audio got me millions of views! 🚀 #shorts",
    "Try this audio 🎧 You will become famous #shorts",
    "Use this sound to blow up your channel! 🎯 #shorts",
    "{sub_str} subs complete ✅ Road to 100K! #shorts",
    "Let’s get {sub_str} subs soon! 🤝 #shorts",
    "Use this audio for instant viral views! ✨ #shorts",
    "This sound is literally a cheat code 🤯 #shorts",
    "Use this audio before it gets patched ⚡ #shorts",
    "99% of creators don't know this sound 🔥 #shorts",
    "Use this audio to gain {sub_str} subs today! 🚀 #shorts"
]

# High-Retention Shorts Tags
OPTIMIZED_TAGS = [
    "shorts",
    "youtube shorts",
    "use this audio",
    "viral audio",
    "trending audio",
    "gain subscribers",
    "how to get 1m views",
    "viral sound",
    "grow on youtube",
    "trending shorts",
    "fyp",
    "viral",
    "gaming",
    "ask gaming",
    "youtube studio",
    "youtube algorithm"
]

# Hashtags for Description
HASHTAGS = [
    "#shorts",
    "#trending",
    "#viral",
    "#audio",
    "#usethisaudio",
    "#youtubeshorts",
    "#fyp",
    "#blowup",
    "#growth"
]

def format_count_short(count: int) -> str:
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M".replace(".0M", "M")
    elif count >= 1_000:
        return f"{count / 1_000:.1f}k".replace(".0k", "k").upper()
    return str(count)

def generate_video_metadata(
    channel_name: str = "ASK Gaming",
    channel_handle: str = "@askgaming",
    target_subs: int = 2200,
    song_name: str = None
) -> Dict[str, any]:
    """Generates complete upload-ready YouTube Shorts metadata."""
    sub_str = format_count_short(target_subs)
    views_str = f"{random.randint(15, 65)} MILLION"

    template = random.choice(TITLE_TEMPLATES)
    title = template.format(sub_str=sub_str, views_str=views_str)

    hashtags_str = " ".join(random.sample(HASHTAGS, 6))

    description_parts = [
        f"Use this audio to blow up your channel! 📈🔥",
        f"Milestone unlocked: {target_subs:,} Subscribers! 🚀",
        f"Sound: {song_name if song_name else 'Trending Viral Sound 🎧'}",
        f"",
        f"Subscribe to {channel_handle} for more! 🎯",
        f"",
        hashtags_str
    ]
    description = "\n".join(description_parts)

    tags = list(OPTIMIZED_TAGS)
    if song_name:
        tags.insert(0, song_name.lower().replace("_", " "))

    return {
        "title": title,
        "description": description,
        "tags": tags,
        "category": "Entertainment",
        "privacy": "public",
        "made_for_kids": False
    }

if __name__ == "__main__":
    meta = generate_video_metadata("ASK Gaming", "@askgaming", 2200, "club_drop")
    print("================ Generated Metadata ================")
    print("TITLE:\n", meta["title"])
    print("\nDESCRIPTION:\n", meta["description"])
    print("\nTAGS:\n", ", ".join(meta["tags"]))
    print("====================================================")
