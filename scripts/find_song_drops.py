import subprocess
import sys
from pathlib import Path
import yt_dlp

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
BGM_DIR = REPO_ROOT / "assets" / "sounds" / "bgm"
RAW_DIR = BGM_DIR / "_full_raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPTS_DIR))
from render_video import get_ffmpeg_exe
FFMPEG_EXE = get_ffmpeg_exe()

SONGS = [
    ("passo_bem_solto", "NT4eF9YsYnM"),
    ("phonk_montage", "2eeoz2dKVIg"),
    ("trending_beat_1", "0BGoLgcz8zI"),
    ("viral_bounce", "xvT1jH8B9AM"),
    ("pop_trend_1", "IpFX2vq8HKw"),
    ("electronic_energy", "LTTUkVKcuRg"),
    ("hype_bass", "EzKubdskJUs"),
    ("club_drop", "X-r4nYoeo1k"),
    ("viral_hook", "7G-jUPn5RY8")
]

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'outtmpl': str(RAW_DIR / '%(id)s.%(ext)s'),
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for name, vid in SONGS:
        raw_files = list(RAW_DIR.glob(f"{vid}.*"))
        if not raw_files:
            print(f"Downloading {name} ({vid})...")
            try:
                ydl.download([f"https://www.youtube.com/watch?v={vid}"])
            except Exception as e:
                print(f"Error {vid}: {e}")

print("\n--- Analysing energy across 5s windows ---")
for name, vid in SONGS:
    raw_files = [f for f in RAW_DIR.glob(f"{vid}.*") if f.suffix != ".part"]
    if not raw_files:
        print(f"{name}: File missing")
        continue
    fpath = raw_files[0]
    
    # Run ffmpeg to get duration
    dur_cmd = [FFMPEG_EXE, "-i", str(fpath)]
    p = subprocess.run(dur_cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    dur = 60.0
    for line in p.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip().split(":")
            dur = float(parts[0])*3600 + float(parts[1])*60 + float(parts[2])
            break

    print(f"\n{name} ({vid}) | Total Duration: {dur:.1f}s")
    # Sample every 10s up to dur-10 to find RMS energy
    best_rms = -999.0
    best_t = 0.0
    for t in range(0, int(dur) - 10, 8):
        # probe 6s slice volume
        cmd = [
            FFMPEG_EXE, "-ss", str(t), "-t", "6",
            "-i", str(fpath),
            "-filter:a", "volumedetect",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
        mean_vol = -99.0
        max_vol = -99.0
        for l in res.stderr.splitlines():
            if "mean_volume:" in l:
                mean_vol = float(l.split("mean_volume:")[1].replace("dB", "").strip())
            if "max_volume:" in l:
                max_vol = float(l.split("max_volume:")[1].replace("dB", "").strip())
        print(f"  t={t:3d}s - {t+6:3d}s | mean: {mean_vol:5.1f} dB | max: {max_vol:4.1f} dB")
