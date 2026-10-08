# YouTube Studio Subscriber Counter Automation (ASK Gaming)

Automated daily YouTube Shorts generator that creates a **photorealistic iPhone screen recording of the YouTube Studio mobile app** for **ASK Gaming** (`@askgaming`).

The video simulates an authentic creator experience: displaying past screenshot milestones (multi-snapshot journey) from low numbers, transitioning into an active live countdown session where subscribers, channel analytics, clock time, and video metrics tick up live, celebrating milestones with iOS Dynamic Island expansion, confetti, synchronized sound effects, and trending Shorts background music.

---

## ✨ Features

- **Modular & Maintainable Architecture**:
  - `templates/ask_studio.html`: Clean, semantic HTML structure (~230 lines).
  - `templates/css/ask_studio.css`: Complete styling for Light & Dark themes, Dynamic Island, typography, cards, and animations.
  - `templates/js/ask_studio.js`: Modular animation and multi-counter timing engine.
- **Multi-Screenshot Journey Transitions**:
  - Instead of a single static screen, the Short opens with historical milestone snapshots starting from low numbers (e.g. 1 ➔ 25 ➔ 70), transitioning with a realistic camera snapshot flash and shutter click sound into the live session.
- **Progressive Milestone Scaling Formula**:
  - Subscriber jump sizes increase with each subsequent video:
    - **Video 1**: `~5 ➔ ~100` (gain `+95`)
    - **Video 2**: `~100 ➔ ~250` (gain `+150`)
    - **Video 3**: `~250 ➔ ~500` (gain `+250`)
    - **Video 4**: `~500 ➔ ~1,000` (gain `+500`)
    - **Video 5+**: `~1,000 ➔ ~2,000+` (gain `+1,000+`)
- **Active Multi-Counter Engine**:
  - ⏱️ **Status Bar Clock**: Ticks forward mid-video (e.g. `11:34` ➔ `11:35`).
  - 👥 **Total Subscribers**: Smoothly increments tick-by-tick with synchronized pop sound effects.
  - 📈 **Recently Gained Subscribers**: Analytics card increments in lockstep (e.g. `+41` ➔ `+97`).
  - 👀 **28-Day Channel Views**: Counts up live (e.g. `5.2k` ➔ `5.4k`).
  - ⏳ **Watch Time Hours**: Live ticks up (e.g. `0.3k` ➔ `0.4k`).
  - 🎮 **Recent Video Metrics**: Video views and likes update live.
- **Randomized Themes & Times**:
  - Randomly alternates between **Light Mode** (morning/day screenshots) and **Dark Mode** (evening/night screenshots).
- **Audio Mixing**:
  - 🎵 **Trending Shorts BGM**: Seamlessly mixes background music (`assets/sounds/bgm_trending.mp3`) with gentle fade-out.
  - 📸 **Camera Shutter**: Real mechanical click sound during snapshot transitions.
  - 🔊 **Tick Pops & Chimes**: Procedurally generated wooden/bubble ticks, anticipation riser, and rich celebratory milestone chime.
- **Clean Celebration**:
  - No obtrusive banners. Celebration is natively integrated into the **iOS Dynamic Island** (expands to display `🎉 100 Subs Reached! 🏆`) accompanied by full-screen falling confetti.
- **1 Daily Upload with Random Slot Scheduling**:
  - Automatically schedules 1 Short daily across peak Indian audience slots:
    - 🌅 **Morning 8:00 AM IST** (02:30 UTC)
    - 🌇 **Evening 5:30 PM IST** (12:00 UTC)
    - 🌙 **Evening 8:30 PM IST** (15:00 UTC)

---

## 📁 Project Structure

```
yt-sub/
├── .github/workflows/
│   └── daily_counter_short.yml   # 1 Daily run at 07:00 AM IST to schedule random slot
├── assets/
│   ├── channel_avatar.png        # ASK Gaming custom avatar
│   ├── thumbnails/               # Pool of 5 realistic gaming thumbnails
│   │   ├── thumb_1.png ... thumb_5.png
│   └── sounds/                   # Mixed audio assets
│       ├── bgm_trending.mp3      # Trending Shorts background track
│       ├── shutter.wav           # Camera snapshot click
│       ├── tick.wav              # Subscriber pop sound
│       ├── riser.wav             # Anticipation riser
│       └── milestone_ding.wav    # Celebratory chime chord
├── templates/
│   ├── ask_studio.html           # Modular HTML skeleton
│   ├── css/
│   │   └── ask_studio.css        # Clean CSS stylesheet (Light & Dark mode)
│   └── js/
│       └── ask_studio.js         # Modular animation & counter engine
├── scripts/
│   ├── render_video.py           # Playwright + FFmpeg multi-track audio renderer
│   ├── pipeline.py               # Daily pipeline with progressive scaling & YouTube API
│   ├── test_video_gen.py         # Local preview CLI with options
│   ├── setup_oauth.py            # YouTube OAuth token generator
│   ├── sound_synth.py            # Synthesizes UI sound effects
│   └── requirements.txt          # Python dependencies
├── drafts/                       # AI-generated metadata logs
├── state.json                    # Stores channel subscriber progress & slots
├── .env.example                  # Environment secrets template
└── README.md
```

---

## 🚀 Quick Start (Local Preview)

### 1. Install Dependencies
```bash
pip install -r scripts/requirements.txt
playwright install chromium
```

### 2. Generate Sample Video
Run the preview CLI with your desired settings:

```bash
# Preview Journey mode with Dark theme starting from 5 to 100:
python scripts/test_video_gen.py --start 5 --end 100 --theme dark --output work/preview_5_to_100.mp4

# Preview Light theme with custom sub range:
python scripts/test_video_gen.py --start 100 --end 250 --theme light --output work/preview_100_to_250.mp4
```

The output video is saved at 1080x1920 (9:16 vertical) in `work/` with all audio mixed in!

---

## ⚙️ Running Daily Pipeline
To run a daily generation and automated upload:
```bash
python scripts/pipeline.py
```
This automatically:
1. Picks the next progressive milestone from `state.json` (e.g. 5 ➔ 100, then 100 ➔ 250, etc.).
2. Reserves 1 random daily slot (8:00 AM, 5:30 PM, or 8:30 PM IST).
3. Renders the video with multi-screenshot journey, live counters, shutter FX, and trending BGM.
4. Generates AI metadata via Gemini.
5. Uploads and schedules via YouTube Data API v3 (or saves locally if credentials are not configured).
6. Updates `state.json` for the next day's run.
