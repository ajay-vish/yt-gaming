"""
Scrapes metadata from https://www.youtube.com/@tryingtogetfamous1979
Fetches titles, descriptions, tags, view counts, and engagement patterns.
"""

import json
import sys
from pathlib import Path
import yt_dlp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def scrape_channel(channel_handle="@tryingtogetfamous1979", max_items=15):
    print(f"🔍 Fetching metadata for channel {channel_handle}...")
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'playlist_items': f'1-{max_items}'
    }

    urls_to_try = [
        f"https://www.youtube.com/{channel_handle}/shorts",
        f"https://www.youtube.com/{channel_handle}/videos",
    ]

    found_videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for tab_url in urls_to_try:
            print(f"Fetching from {tab_url}...")
            try:
                res = ydl.extract_info(tab_url, download=False)
                entries = res.get('entries', [])
                if entries:
                    print(f"Found {len(entries)} items on {tab_url}")
                    found_videos.extend(entries)
            except Exception as e:
                print(f"Failed to fetch {tab_url}: {e}")

    # Now get detailed metadata for top 10 unique videos
    detailed_opts = {
        'quiet': True,
        'skip_download': True
    }

    results = []
    seen_ids = set()

    with yt_dlp.YoutubeDL(detailed_opts) as ydl:
        for v in found_videos:
            vid_id = v.get('id')
            if not vid_id or vid_id in seen_ids:
                continue
            seen_ids.add(vid_id)

            url = f"https://www.youtube.com/watch?v={vid_id}"
            try:
                info = ydl.extract_info(url, download=False)
                results.append({
                    "id": vid_id,
                    "title": info.get("title"),
                    "description": info.get("description"),
                    "tags": info.get("tags", []),
                    "categories": info.get("categories", []),
                    "duration": info.get("duration"),
                    "view_count": info.get("view_count"),
                    "like_count": info.get("like_count"),
                    "comment_count": info.get("comment_count"),
                    "upload_date": info.get("upload_date")
                })
                print(f"Scraped [{len(results)}/{max_items}]: {info.get('title')}")
                if len(results) >= max_items:
                    break
            except Exception as e:
                print(f"Failed to extract info for {vid_id}: {e}")

    out_file = Path("work/scraped_channel_meta.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Scraped {len(results)} videos successfully. Saved to {out_file}")
    return results

if __name__ == "__main__":
    scrape_channel()
