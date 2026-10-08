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

# Songs and their high-impact viral drop / chorus time ranges (start_sec, duration_sec)
TRENDING_SONGS = [
    {
        "id": "NT4eF9YsYnM",
        "name": "passo_bem_solto",
        "url": "https://www.youtube.com/watch?v=NT4eF9YsYnM",
        "start": 12.0,
        "duration": 22.0
    },
    {
        "id": "2eeoz2dKVIg",
        "name": "phonk_montage",
        "url": "https://www.youtube.com/watch?v=2eeoz2dKVIg",
        "start": 15.0,
        "duration": 22.0
    },
    {
        "id": "0BGoLgcz8zI",
        "name": "trending_beat_1",
        "url": "https://www.youtube.com/watch?v=0BGoLgcz8zI",
        "start": 10.0,
        "duration": 22.0
    },
    {
        "id": "xvT1jH8B9AM",
        "name": "viral_bounce",
        "url": "https://www.youtube.com/watch?v=xvT1jH8B9AM",
        "start": 14.0,
        "duration": 22.0
    },
    {
        "id": "IpFX2vq8HKw",
        "name": "pop_trend_1",
        "url": "https://www.youtube.com/watch?v=IpFX2vq8HKw",
        "start": 18.0,
        "duration": 22.0
    },
    {
        "id": "LTTUkVKcuRg",
        "name": "electronic_energy",
        "url": "https://www.youtube.com/watch?v=LTTUkVKcuRg",
        "start": 16.0,
        "duration": 22.0
    },
    {
        "id": "EzKubdskJUs",
        "name": "hype_bass",
        "url": "https://www.youtube.com/watch?v=EzKubdskJUs",
        "start": 12.0,
        "duration": 22.0
    },
    {
        "id": "X-r4nYoeo1k",
        "name": "club_drop",
        "url": "https://www.youtube.com/watch?v=X-r4nYoeo1k",
        "start": 15.0,
        "duration": 22.0
    },
    {
        "id": "7G-jUPn5RY8",
        "name": "viral_hook",
        "url": "https://www.youtube.com/watch?v=7G-jUPn5RY8",
        "start": 14.0,
        "duration": 22.0
    }
]

def download_and_trim_all():
    temp_dir = BGM_DIR / "_raw"
    temp_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎵 Downloading and trimming {len(TRENDING_SONGS)} trending songs into {BGM_DIR}...")

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
            if out_file.exists() and out_file.stat().st_size > 10000:
                print(f"[{idx+1}/{len(TRENDING_SONGS)}] Already exists: {out_file.name}")
                results.append(out_file)
                continue

            print(f"[{idx+1}/{len(TRENDING_SONGS)}] Downloading {item['name']} ({item['url']})...")
            try:
                info = ydl.extract_info(item['url'], download=True)
                downloaded_file = Path(ydl.prepare_filename(info))
                
                # If downloaded file doesn't exist, search temp_dir for match
                if not downloaded_file.exists():
                    matches = list(temp_dir.glob(f"{item['id']}.*"))
                    if matches:
                        downloaded_file = matches[0]

                if not downloaded_file.exists():
                    print(f"  ❌ Could not find raw file for {item['id']}")
                    continue

                # Trim best segment with ffmpeg
                cmd = [
                    FFMPEG_EXE, "-y",
                    "-ss", str(item["start"]),
                    "-i", str(downloaded_file),
                    "-t", str(item["duration"]),
                    "-af", "afade=t=in:st=0:d=0.3,afade=t=out:st=21.0:d=1.0",
                    "-ac", "2",
                    "-b:a", "192k",
                    str(out_file)
                ]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  ✅ Saved and trimmed: {out_file.name} ({out_file.stat().st_size // 1024} KB)")
                results.append(out_file)
            except Exception as e:
                print(f"  ❌ Error downloading/processing {item['name']}: {e}")

    # Clean up temp raw files
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"\n🎉 Done! {len(results)} trending background music tracks ready in {BGM_DIR}")
    return results

if __name__ == "__main__":
    download_and_trim_all()
