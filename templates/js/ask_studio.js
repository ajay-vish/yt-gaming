// Configuration defaults
const CLICKBAIT_POOL = [
  "Use this audio to<br>gain 1M views",
  "Use this audio to<br>gain 100K Subs",
  "Use this audio to<br>get 1M views in 24 hours 📈",
  "Use this audio to<br>blow up your channel 🚀",
  "Use this sound to<br>get 10M views instantly ⚡",
  "Use this sound to<br>gain 100K Subs this week 🔥",
  "Use this audio to<br>go viral overnight ✨",
  "Use this sound to<br>gain 50K Subs today 🎯",
  "Use this audio for<br>instant 1M views 🤯"
];

const config = Object.assign({
  mode: "journey", // "journey" (multi-screenshot transitions) or "live" (single session)
  theme: "light",  // "light", "dark", or "auto"
  channelName: "ASK Gaming",
  avatarUrl: "../assets/channel_avatar.png",
  startCount: 2157,
  endCount: 2200,
  durationSec: 8.5,
  holdStartSec: 1.5,
  holdEndSec: 2.5,
  clickbaitText: CLICKBAIT_POOL[Math.floor(Math.random() * CLICKBAIT_POOL.length)],
  // Base metrics that will count up live
  baseViews: 395.0,
  baseWatchTime: 3.0,
  baseSubsGain: 601,
  revenue: "₹0",
  // Video Card 1 stats
  recentVideoTitle: "Offline Shops vs GPS Cracker Sivakasi: The Truth Revealed",
  recentVideoTime: "First 5 hours, 46 minutes",
  baseVideoViews: 3.4,
  baseVideoLikes: 31,
  videoComments: 25,
  // Video Card 2 & 3 stats
  video2Title: "Saste Patakhe Yahan Milenge! 😱 Dilip Traders Full Review",
  video2Time: "First 8 hours, 1 minutes",
  video2Views: "7.4k",
  video2Likes: "119",
  video2Comments: "31",
  video3Title: "Sivakasi & Kurali Fail! 😱 Cheapest Fireworks Market Rate",
  video3Time: "First 21 hours, 22 minutes",
  video3Views: "3.3k",
  video3Likes: "40",
  video3Comments: "29",
  startTimeHour: 4,
  startTimeMinute: 1,
  batteryPercent: 30,
  milestoneMessage: "2,200 SUBSCRIBERS UNLOCKED!",
  // Multi-screenshot journey steps (from low numbers to final live session)
  journeySteps: [
    {
      timeHour: 8, timeMin: 14,
      theme: "light",
      battery: 92,
      subs: 140,
      views: "18.4k",
      watch: "150",
      subsGain: "+85",
      title: "My First Ranked Match (Road to Pro!)",
      videoTime: "First 2 days, 4 hours",
      thumbUrl: "../assets/thumbnails/thumb_1.png",
      vViews: "1.2k", vLikes: 18, vComments: 8
    },
    {
      timeHour: 1, timeMin: 35,
      theme: "light",
      battery: 68,
      subs: 620,
      views: "72.8k",
      watch: "580",
      subsGain: "+280",
      title: "Zero Recoil Secret Weapon Loadout! (After Season Update)",
      videoTime: "First 1 day, 6 hours",
      thumbUrl: "../assets/thumbnails/thumb_4.png",
      vViews: "4.1k", vLikes: 88, vComments: 35
    },
    {
      timeHour: 9, timeMin: 42,
      theme: "dark",
      battery: 36,
      subs: 1450,
      views: "185.2k",
      watch: "1.4k",
      subsGain: "+420",
      title: "GTA 6 Official Gameplay Leaks Breakdown & Secrets",
      videoTime: "First 8 hours, 20 minutes",
      thumbUrl: "../assets/thumbnails/thumb_2.png",
      vViews: "8.7k", vLikes: 142, vComments: 68
    }
  ]
}, window.CONFIG || {});

function formatClickbait(val) {
  if (!val) return "";
  if (val.includes("<br>")) return val;
  if (val.includes("\n")) return val.replace(/\n/g, "<br>");
  if (val.includes(" to ")) return val.replace(" to ", " to<br>");
  if (val.includes(" for ")) return val.replace(" for ", " for<br>");
  return val;
}

// Helper to safely set text/src without throwing if element is absent
function safeText(id, val) {
  const el = document.getElementById(id);
  if (el && val !== undefined && val !== null) el.textContent = val;
}
function safeSrc(id, val) {
  const el = document.getElementById(id);
  if (el && val !== undefined && val !== null) el.src = val;
}

// Apply Theme
if (config.theme === "dark") {
  document.body.classList.add("dark-theme");
}

// DOM Elements
const timeEl = document.getElementById("status-time");
const batteryEl = document.getElementById("battery-percent");
const counterEl = document.getElementById("counter-val");
const viewsEl = document.getElementById("metric-views");
const watchEl = document.getElementById("metric-watch");
const subsGainEl = document.getElementById("metric-subs");
const videoTitleEl = document.getElementById("video-title");
const videoTimeEl = document.getElementById("video-time");
const videoThumbEl = document.getElementById("video-thumbnail");
const quickViewsEl = document.getElementById("quick-views");
const quickLikesEl = document.getElementById("quick-likes");
const quickCommentsEl = document.getElementById("quick-comments");
const flashEl = document.getElementById("flash-overlay");

// Populate Initial Static UI
const clickbaitEl = document.getElementById("clickbait-text");
if (clickbaitEl && config.clickbaitText) {
  clickbaitEl.innerHTML = formatClickbait(config.clickbaitText);
}
safeText("channel-name", config.channelName);
safeSrc("channel-avatar", config.avatarUrl);
safeSrc("avatar-mini", config.avatarUrl);
safeText("metric-revenue", config.revenue);
safeText("battery-percent", config.batteryPercent);

const minPad = (config.startTimeMinute || 0).toString().padStart(2, '0');
safeText("status-time", `${config.startTimeHour || 4}:${minPad}`);

// Video Card 1
safeText("video-title", config.recentVideoTitle);
safeText("video-time", config.recentVideoTime);
safeText("quick-views", `${Number(config.baseVideoViews).toFixed(1)}k`);
safeText("quick-likes", config.baseVideoLikes);
safeText("quick-comments", config.videoComments);
if (config.videoThumbUrl) safeSrc("video-thumbnail", config.videoThumbUrl);

// Video Card 2 & 3
if (config.extraVideos && config.extraVideos.length >= 2) {
  safeText("video-title-2", config.extraVideos[0].title);
  safeText("video-time-2", config.extraVideos[0].time);
  safeText("quick-views-2", config.extraVideos[0].views);
  safeText("quick-likes-2", config.extraVideos[0].likes);
  safeText("quick-comments-2", config.extraVideos[0].comments);
  if (config.extraVideos[0].thumbUrl) safeSrc("video-thumbnail-2", config.extraVideos[0].thumbUrl);

  safeText("video-title-3", config.extraVideos[1].title);
  safeText("video-time-3", config.extraVideos[1].time);
  safeText("quick-views-3", config.extraVideos[1].views);
  safeText("quick-likes-3", config.extraVideos[1].likes);
  safeText("quick-comments-3", config.extraVideos[1].comments);
  if (config.extraVideos[1].thumbUrl) safeSrc("video-thumbnail-3", config.extraVideos[1].thumbUrl);
} else {
  safeText("video-title-2", config.video2Title);
  safeText("video-time-2", config.video2Time);
  safeText("quick-views-2", config.video2Views);
  safeText("quick-likes-2", config.video2Likes);
  safeText("quick-comments-2", config.video2Comments);

  safeText("video-title-3", config.video3Title);
  safeText("video-time-3", config.video3Time);
  safeText("quick-views-3", config.video3Views);
  safeText("quick-likes-3", config.video3Likes);
  safeText("quick-comments-3", config.video3Comments);
}

// Confetti Engine
const canvas = document.getElementById("confetti-canvas");
const ctx = canvas.getContext("2d");
canvas.width = 1080;
canvas.height = 1920;
let particles = [];
const colors = ["#0F9D58", "#34A853", "#FFCC00", "#FF0000", "#3EA6FF", "#FF8C00", "#9B51E0"];

function triggerConfetti() {
  particles = [];
  for (let i = 0; i < 200; i++) {
    particles.push({
      x: Math.random() * 1080,
      y: Math.random() * -100,
      vx: (Math.random() - 0.5) * 6,
      vy: Math.random() * 7 + 4,
      size: Math.random() * 12 + 6,
      color: colors[Math.floor(Math.random() * colors.length)],
      rotation: Math.random() * 360,
      rotSpeed: (Math.random() - 0.5) * 10,
      gravity: 0.18,
      opacity: 1
    });
  }
}

function renderConfetti() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < particles.length; i++) {
    const p = particles[i];
    p.x += p.vx;
    p.y += p.vy;
    p.vy += p.gravity;
    p.rotation += p.rotSpeed;
    p.opacity -= 0.0016;

    if (p.opacity > 0) {
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = Math.max(0, p.opacity);
      ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.5);
      ctx.restore();
    }
  }
  requestAnimationFrame(renderConfetti);
}
renderConfetti();

// Audio event buffers for Playwright/FFmpeg audio mixing
window.TICK_EVENTS = [];
window.SHUTTER_EVENTS = [];

function applyCard(idx, data) {
  if (!data) return;
  const suffix = idx === 1 ? "" : `-${idx}`;
  safeText(`video-title${suffix}`, data.title);
  safeText(`video-time${suffix}`, data.time);
  if (data.thumbUrl) safeSrc(`video-thumbnail${suffix}`, data.thumbUrl);
  safeText(`quick-views${suffix}`, data.views);
  safeText(`quick-likes${suffix}`, data.likes);
  safeText(`quick-comments${suffix}`, data.comments);
}

// Trigger Snapshot Transition (0.5s intervals, direct clean cut, zero flash)
function performSnapshotTransition(stepData, elapsed) {
  window.SHUTTER_EVENTS.push({ timeMs: elapsed });

  if (stepData.theme === "dark") {
    document.body.classList.add("dark-theme");
  } else {
    document.body.classList.remove("dark-theme");
  }

  const minStr = stepData.timeMin.toString().padStart(2, '0');
  safeText("status-time", `${stepData.timeHour}:${minStr}`);
  safeText("battery-percent", stepData.battery);
  safeText("counter-val", Number(stepData.subs).toLocaleString());
  safeText("metric-views", stepData.views);
  safeText("metric-watch", stepData.watch);
  safeText("metric-subs", stepData.subsGain);

  if (stepData.cards && Array.isArray(stepData.cards)) {
    stepData.cards.forEach((c, idx) => applyCard(idx + 1, c));
  } else {
    applyCard(1, {
      title: stepData.title,
      time: stepData.videoTime,
      thumbUrl: stepData.thumbUrl,
      views: stepData.vViews,
      likes: stepData.vLikes,
      comments: stepData.vComments
    });
  }
}

// Setup Frozen Final Milestone Screenshot (No counter +++, completely frozen screen, all 3 cards updated)
function setupFinalMilestoneStage(elapsed) {
  window.SHUTTER_EVENTS.push({ timeMs: elapsed });
  window.MILESTONE_TIME_MS = elapsed;

  if (config.theme === "dark") {
    document.body.classList.add("dark-theme");
  } else {
    document.body.classList.remove("dark-theme");
  }

  const minStr = (config.startTimeMinute || 0).toString().padStart(2, '0');
  safeText("status-time", `${config.startTimeHour || 4}:${minStr}`);
  safeText("battery-percent", config.batteryPercent);
  safeText("counter-val", Number(config.endCount).toLocaleString());
  safeText("metric-views", `${(config.baseViews + 0.4).toFixed(1)}k`);
  safeText("metric-watch", `${(config.baseWatchTime + 0.2).toFixed(1)}k`);
  safeText("metric-subs", `+${config.baseSubsGain + (config.endCount - config.startCount)}`);

  if (config.finalCards && Array.isArray(config.finalCards)) {
    config.finalCards.forEach((c, idx) => applyCard(idx + 1, c));
  } else {
    applyCard(1, {
      title: config.recentVideoTitle,
      time: config.recentVideoTime,
      thumbUrl: config.videoThumbUrl,
      views: `${(config.baseVideoViews + 0.15).toFixed(1)}k`,
      likes: config.baseVideoLikes,
      comments: config.videoComments
    });
    if (config.extraVideos && config.extraVideos.length >= 2) {
      applyCard(2, config.extraVideos[0]);
      applyCard(3, config.extraVideos[1]);
    }
  }

  triggerConfetti();
}

// =========================================
// MASTER PLAYBACK TIMELINE (Screenshot switches each 0.5sec, 100% Frozen Screens)
// =========================================
const startTime = performance.now();
const totalDurationMs = config.durationSec * 1000;
const STEP_INTERVAL_MS = 500; // Switch screenshot every 0.5 seconds

const isJourney = config.mode === "journey" && config.journeySteps && config.journeySteps.length > 0;
const journeyDurationMs = isJourney ? (config.journeySteps.length * STEP_INTERVAL_MS) : 0;

let currentStepIdx = -1;
let milestoneStageInitialized = !isJourney;

// Initial setup
if (isJourney) {
  const firstStep = config.journeySteps[0];
  if (firstStep.theme === "dark") document.body.classList.add("dark-theme");
  const minStr = firstStep.timeMin.toString().padStart(2, '0');
  safeText("status-time", `${firstStep.timeHour}:${minStr}`);
  safeText("battery-percent", firstStep.battery);
  safeText("counter-val", Number(firstStep.subs).toLocaleString());
  safeText("metric-views", firstStep.views);
  safeText("metric-watch", firstStep.watch);
  safeText("metric-subs", firstStep.subsGain);
  if (firstStep.cards && Array.isArray(firstStep.cards)) {
    firstStep.cards.forEach((c, idx) => applyCard(idx + 1, c));
  } else {
    applyCard(1, {
      title: firstStep.title,
      time: firstStep.videoTime,
      thumbUrl: firstStep.thumbUrl,
      views: firstStep.vViews,
      likes: firstStep.vLikes,
      comments: firstStep.vComments
    });
  }
  currentStepIdx = 0;
} else {
  setupFinalMilestoneStage(0);
}

function updateTimeline(nowTimestamp) {
  const elapsed = nowTimestamp - startTime;

  if (isJourney && elapsed < journeyDurationMs) {
    // Multi-Screenshot Journey Stage: step changes exactly every 0.5 seconds (500ms)
    const targetStep = Math.min(config.journeySteps.length - 1, Math.floor(elapsed / STEP_INTERVAL_MS));
    if (targetStep !== currentStepIdx) {
      currentStepIdx = targetStep;
      performSnapshotTransition(config.journeySteps[currentStepIdx], elapsed);
    }
  } else {
    // Final Milestone Stage (Frozen Screenshot with celebration)
    if (!milestoneStageInitialized) {
      milestoneStageInitialized = true;
      setupFinalMilestoneStage(elapsed);
    }
  }

  if (elapsed < totalDurationMs) {
    requestAnimationFrame(updateTimeline);
  } else {
    window.ANIMATION_COMPLETED = true;
  }
}

requestAnimationFrame(updateTimeline);
