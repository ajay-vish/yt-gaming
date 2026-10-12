"""
Downloads and trims trending YouTube Shorts songs for background music pool.
"""

import os
import sys
import subprocess
from pathlib import Path
import yt_dlp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
ASSETS_DIR = REPO_ROOT / "assets"
BGM_DIR = ASSETS_DIR / "sounds" / "bgm"
BGM_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPTS_DIR))
from render_video import get_ffmpeg_exe
FFMPEG_EXE = get_ffmpeg_exe()

# Songs and their exact high-impact viral drop / chorus time ranges
TRENDING_SONGS = [
    {
        "id": "NT4eF9YsYnM",
        "name": "passo_bem_solto",
        "url": "https://www.youtube.com/watch?v=NT4eF9YsYnM",
        "start": 16.0,
        "duration": 22.0
    },
    {
        "id": "2eeoz2dKVIg",
        "name": "phonk_montage",
        "url": "https://www.youtube.com/watch?v=2eeoz2dKVIg",
        "start": 64.0,
        "duration": 22.0
    },
    {
        "id": "0BGoLgcz8zI",
        "name": "trending_beat_1",
        "url": "https://www.youtube.com/watch?v=0BGoLgcz8zI",
        "start": 72.0,
        "duration": 22.0
    },
    {
        "id": "xvT1jH8B9AM",
        "name": "viral_bounce",
        "url": "https://www.youtube.com/watch?v=xvT1jH8B9AM",
        "start": 48.0,
        "duration": 22.0
    },
    {
        "id": "IpFX2vq8HKw",
        "name": "pop_trend_1",
        "url": "https://www.youtube.com/watch?v=IpFX2vq8HKw",
        "start": 48.0,
        "duration": 22.0
    },
    {
        "id": "LTTUkVKcuRg",
        "name": "electronic_energy",
        "url": "https://www.youtube.com/watch?v=LTTUkVKcuRg",
        "start": 40.0,
        "duration": 22.0
    },
    {
        "id": "EzKubdskJUs",
        "name": "hype_bass",
        "url": "https://www.youtube.com/watch?v=EzKubdskJUs",
        "start": 16.0,
        "duration": 22.0
    },
    {
        "id": "X-r4nYoeo1k",
        "name": "club_drop",
        "url": "https://www.youtube.com/watch?v=X-r4nYoeo1k",
        "start": 24.0,
        "duration": 22.0
    },
    {
        "id": "7G-jUPn5RY8",
        "name": "viral_hook",
        "url": "https://www.youtube.com/watch?v=7G-jUPn5RY8",
        "start": 24.0,
        "duration": 22.0
    }
]

def download_and_trim_all(force: bool = False):
    temp_dir = BGM_DIR / "_raw"
    temp_dir.mkdir(parents=True, exist_ok=True)
    full_raw_dir = BGM_DIR / "_full_raw"

    print(f"🎵 Trimming {len(TRENDING_SONGS)} trending songs with peak drop sections into {BGM_DIR}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': str(temp_dir / '%(id)s.%(ext)s'),
    }

    results = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for idx, item in enumerate(TRENDING_SONGS):
            out_file = BGM_DIR / f"{item['name']}.mp3"
            if not force and out_file.exists() and out_file.stat().st_size > 10000:
                print(f"[{idx+1}/{len(TRENDING_SONGS)}] Updating drop for: {out_file.name}")

            # Check if already present in full_raw_dir
            downloaded_file = None
            if full_raw_dir.exists():
                existing_raw = [f for f in full_raw_dir.glob(f"{item['id']}.*") if f.suffix != ".part"]
                if existing_raw:
                    downloaded_file = existing_raw[0]

            if not downloaded_file or not downloaded_file.exists():
                print(f"[{idx+1}/{len(TRENDING_SONGS)}] Downloading {item['name']} ({item['url']})...")
                try:
                    info = ydl.extract_info(item['url'], download=True)
                    downloaded_file = Path(ydl.prepare_filename(info))
                    if not downloaded_file.exists():
                        matches = list(temp_dir.glob(f"{item['id']}.*"))
                        if matches:
                            downloaded_file = matches[0]
                except Exception as e:
                    print(f"  ❌ Error downloading {item['name']}: {e}")
                    continue

            if not downloaded_file or not downloaded_file.exists():
                print(f"  ❌ Could not find source file for {item['id']}")
                continue

            try:
                # Trim peak drop with ffmpeg: instant hit at 0.0s (no fade-in delay)
                cmd = [
                    FFMPEG_EXE, "-y",
                    "-ss", str(item["start"]),
                    "-i", str(downloaded_file),
                    "-t", str(item["duration"]),
                    "-af", "afade=t=out:st=21.0:d=1.0",
                    "-ac", "2",
                    "-b:a", "192k",
                    str(out_file)
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  ✅ Saved peak drop ({item['start']}s -> {item['start']+item['duration']}s): {out_file.name} ({out_file.stat().st_size // 1024} KB)")
                results.append(out_file)
            except Exception as e:
                print(f"  ❌ Error processing {item['name']}: {e}")

    # Clean up temp raw files
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"\n🎉 Done! {len(results)} trending background music tracks ready in {BGM_DIR}")
    return results

if __name__ == "__main__":
    download_and_trim_all()
