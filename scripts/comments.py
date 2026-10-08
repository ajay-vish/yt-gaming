#!/usr/bin/env python3
"""
Automated YouTube Pinned Comments Poster.
Checks pending scheduled Shorts that have gone public,
posts an engaging pinned creator comment, and tracks them in state.json.
Modeled after yt-automation/scripts/comments.py.
"""

import json
import os
import sys
from pathlib import Path

# Paths
SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
STATE_FILE = REPO_ROOT / "state.json"
ENV_FILE = REPO_ROOT / ".env"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Auto-load .env
if ENV_FILE.exists():
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state = {}
    else:
        state = {}
    state.setdefault("pending_comments", {})
    state.setdefault("commented_video_ids", [])
    return state


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


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


def is_public(youtube, video_id: str) -> bool:
    resp = youtube.videos().list(part="status", id=video_id).execute()
    items = resp.get("items", [])
    return bool(items) and items[0]["status"]["privacyStatus"] == "public"


def post_comment(youtube, video_id: str, milestone_count: int):
    comment_text = (
        f"🎮 Road to 10K Subscribers! Which gameplay do you want to see next? Drop a comment below! 👇❤️"
    )
    youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {"snippet": {"textOriginal": comment_text}},
            }
        },
    ).execute()


def main():
    state = load_state()
    pending = dict(state.get("pending_comments", {}))
    if not pending:
        print("[Comments] No pending comments to check.")
        return

    youtube = get_youtube_client()
    if not youtube:
        print("[Comments] YouTube client not configured. Skipping.")
        return

    for video_id, info in pending.items():
        try:
            if not is_public(youtube, video_id):
                print(f"[Comments] {video_id}: not public yet, skipping.")
                continue
            milestone = info.get("target_count", 100)
            post_comment(youtube, video_id, milestone)
            print(f"[Comments] {video_id}: comment posted successfully.")
            state["commented_video_ids"].append(video_id)
            del state["pending_comments"][video_id]
        except Exception as exc:
            print(f"[Comments] {video_id}: failed to comment ({exc}). Will retry next run.")

    save_state(state)


if __name__ == "__main__":
    main()
