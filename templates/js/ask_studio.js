// Configuration defaults
    const config = Object.assign({
      mode: "journey", // "journey" (multi-screenshot transitions) or "live" (single session)
      theme: "light",  // "light", "dark", or "auto"
      channelName: "ASK Gaming",
      avatarUrl: "../assets/channel_avatar.png",
      startCount: 2151,
      endCount: 2200,
      durationSec: 14,
      holdStartSec: 2.0,
      holdEndSec: 3.5,
      // Base metrics that will count up live
      baseViews: 345.7,
      baseWatchTime: 2.6,
      baseSubsGain: 544,
      revenue: "₹0",
      // Recent video stats
      recentVideoTitle: "Insane 1v4 Clutch Win! Ranked Match Gameplay",
      recentVideoTime: "First 3 hours, 58 minutes",
      ranking: "2 of 10 ›",
      baseVideoViews: 2.4,
      baseVideoLikes: 29,
      videoComments: 21,
      ctr: "13.3%",
      avd: "2:19",
      startTimeHour: 2,
      startTimeMinute: 13,
      batteryPercent: 44,
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

    // Apply Theme
    if (config.theme === "dark") {
      document.body.classList.add("dark-theme");
    }

    // Elements
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
    const detailViewsEl = document.getElementById("detail-views");
    const detailCommentsEl = document.getElementById("detail-comments-count");
    const flashEl = document.getElementById("flash-overlay");

    // Populate Initial Static UI
    document.getElementById("channel-name").textContent = config.channelName;
    document.getElementById("channel-avatar").src = config.avatarUrl;
    document.getElementById("avatar-mini").src = config.avatarUrl;
    document.getElementById("island-art").src = config.avatarUrl;
    document.getElementById("metric-revenue").textContent = config.revenue;
    document.getElementById("detail-ranking").textContent = config.ranking;
    document.getElementById("detail-ctr").textContent = config.ctr;
    document.getElementById("detail-duration").textContent = config.avd;
    batteryEl.textContent = config.batteryPercent;

    // Confetti Engine
    const canvas = document.getElementById("confetti-canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = 1080;
    canvas.height = 1920;
    let particles = [];
    const colors = ["#0F9D58", "#34A853", "#FFCC00", "#FF0000", "#3EA6FF", "#FF8C00", "#9B51E0"];

    function triggerConfetti() {
      particles = [];
      for (let i = 0; i < 180; i++) {
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
        p.opacity -= 0.0035;

        if (p.opacity > 0) {
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.fillStyle = p.color;
          ctx.globalAlpha = Math.max(0, p.opacity);
          ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size * 1.4);
          ctx.restore();
        }
      }
      requestAnimationFrame(renderConfetti);
    }
    renderConfetti();

    // Sound Events Log
    window.TICK_EVENTS = [];
    window.SHUTTER_EVENTS = [];

    // Trigger Snapshot Transition
    function performSnapshotTransition(stepData, elapsed) {
      flashEl.classList.add("snap");
      window.SHUTTER_EVENTS.push({ timeMs: elapsed });

      setTimeout(() => {
        // Apply step state
        if (stepData.theme === "dark") {
          document.body.classList.add("dark-theme");
        } else {
          document.body.classList.remove("dark-theme");
        }

        const minStr = stepData.timeMin.toString().padStart(2, '0');
        timeEl.textContent = `${stepData.timeHour}:${minStr}`;
        batteryEl.textContent = stepData.battery;
        counterEl.textContent = Number(stepData.subs).toLocaleString();
        viewsEl.textContent = stepData.views;
        watchEl.textContent = stepData.watch;
        subsGainEl.textContent = stepData.subsGain;
        videoTitleEl.textContent = stepData.title;
        videoTimeEl.textContent = stepData.videoTime;
        videoThumbEl.src = stepData.thumbUrl;
        quickViewsEl.textContent = stepData.vViews;
        detailViewsEl.textContent = stepData.vViews;
        quickLikesEl.textContent = stepData.vLikes;
        quickCommentsEl.textContent = stepData.vComments;
        detailCommentsEl.textContent = stepData.vComments;

        setTimeout(() => flashEl.classList.remove("snap"), 90);
      }, 40);
    }

    // Set Live Stage State
    function setupLiveStage(elapsed) {
      flashEl.classList.add("snap");
      window.SHUTTER_EVENTS.push({ timeMs: elapsed });

      setTimeout(() => {
        if (config.theme === "dark") {
          document.body.classList.add("dark-theme");
        } else {
          document.body.classList.remove("dark-theme");
        }

        const minStr = config.startTimeMinute.toString().padStart(2, '0');
        timeEl.textContent = `${config.startTimeHour}:${minStr}`;
        batteryEl.textContent = config.batteryPercent;
        counterEl.textContent = Number(config.startCount).toLocaleString();
        viewsEl.textContent = `${config.baseViews.toFixed(1)}k`;
        watchEl.textContent = `${config.baseWatchTime.toFixed(1)}k`;
        subsGainEl.textContent = `+${config.baseSubsGain}`;
        videoTitleEl.textContent = config.recentVideoTitle;
        videoTimeEl.textContent = config.recentVideoTime;
        videoThumbEl.src = config.videoThumbUrl;
        quickViewsEl.textContent = `${config.baseVideoViews.toFixed(1)}k`;
        detailViewsEl.textContent = `${config.baseVideoViews.toFixed(1)}k`;
        quickLikesEl.textContent = config.baseVideoLikes;
        quickCommentsEl.textContent = config.videoComments;
        detailCommentsEl.textContent = config.videoComments;

        setTimeout(() => flashEl.classList.remove("snap"), 90);
      }, 40);
    }

    // =========================================
    // MASTER PLAYBACK TIMELINE
    // =========================================
    const startTime = performance.now();
    const totalDurationMs = config.durationSec * 1000;

    // In journey mode: first 4.8 seconds shows 3 snapshots (1.6s each), then live stage
    const isJourney = config.mode === "journey" && config.journeySteps && config.journeySteps.length > 0;
    const journeyDurationMs = isJourney ? 4800 : 0;
    const stepDurationMs = isJourney ? (journeyDurationMs / config.journeySteps.length) : 0;

    let currentStepIdx = -1;
    let liveStageInitialized = !isJourney;

    // Live Stage Counters
    const liveStartMs = journeyDurationMs;
    const liveActiveMs = totalDurationMs - liveStartMs - (config.holdEndSec * 1000);
    let currentCount = config.startCount;
    let currentSubsGain = config.baseSubsGain;
    let milestoneTriggered = false;

    // Initial setup
    if (isJourney) {
      // Load first step immediately
      const firstStep = config.journeySteps[0];
      if (firstStep.theme === "dark") document.body.classList.add("dark-theme");
      const minStr = firstStep.timeMin.toString().padStart(2, '0');
      timeEl.textContent = `${firstStep.timeHour}:${minStr}`;
      batteryEl.textContent = firstStep.battery;
      counterEl.textContent = Number(firstStep.subs).toLocaleString();
      viewsEl.textContent = firstStep.views;
      watchEl.textContent = firstStep.watch;
      subsGainEl.textContent = firstStep.subsGain;
      videoTitleEl.textContent = firstStep.title;
      videoTimeEl.textContent = firstStep.videoTime;
      videoThumbEl.src = firstStep.thumbUrl;
      quickViewsEl.textContent = firstStep.vViews;
      detailViewsEl.textContent = firstStep.vViews;
      quickLikesEl.textContent = firstStep.vLikes;
      quickCommentsEl.textContent = firstStep.vComments;
      detailCommentsEl.textContent = firstStep.vComments;
      currentStepIdx = 0;
    } else {
      setupLiveStage(0);
    }

    function updateTimeline(nowTimestamp) {
      const elapsed = nowTimestamp - startTime;

      if (isJourney && elapsed < journeyDurationMs) {
        // Multi-Screenshot Journey Stage
        const targetStep = Math.min(config.journeySteps.length - 1, Math.floor(elapsed / stepDurationMs));
        if (targetStep !== currentStepIdx) {
          currentStepIdx = targetStep;
          performSnapshotTransition(config.journeySteps[currentStepIdx], elapsed);
        }
      } else {
        // Live Screen Recording Stage
        if (!liveStageInitialized) {
          liveStageInitialized = true;
          setupLiveStage(elapsed);
        }

        const liveElapsed = elapsed - liveStartMs;
        const liveProgress = Math.min(1, Math.max(0, liveElapsed / liveActiveMs));

        // ⏱️ Clock Ticks Live
        const currentMinute = liveProgress > 0.45 
          ? (config.startTimeMinute + 1) % 60 
          : config.startTimeMinute;
        const minStr = currentMinute.toString().padStart(2, '0');
        timeEl.textContent = `${config.startTimeHour}:${minStr}`;

        if (liveProgress < 1.0) {
          // Counting Up
          const targetNumber = Math.floor(config.startCount + (config.endCount - config.startCount) * liveProgress);
          
          if (targetNumber > currentCount) {
            const delta = targetNumber - currentCount;
            currentCount = Math.min(config.endCount, targetNumber);
            currentSubsGain += delta;

            window.TICK_EVENTS.push({ timeMs: elapsed, count: currentCount });
            
            counterEl.classList.add("ticking");
            subsGainEl.classList.add("ticking");
            setTimeout(() => {
              counterEl.classList.remove("ticking");
              subsGainEl.classList.remove("ticking");
            }, 70);
          }

          // Live views counter
          const liveViews = config.baseViews + (liveProgress * 0.4);
          viewsEl.textContent = `${liveViews.toFixed(1)}k`;

          // Live watch time
          const liveWatch = config.baseWatchTime + (liveProgress * 0.2);
          watchEl.textContent = `${liveWatch.toFixed(1)}k`;

          // Video views & likes
          const liveVidViews = config.baseVideoViews + (liveProgress * 0.15);
          quickViewsEl.textContent = `${liveVidViews.toFixed(1)}k`;
          detailViewsEl.textContent = `${liveVidViews.toFixed(1)}k`;
          if (liveProgress > 0.6) {
            quickLikesEl.textContent = config.baseVideoLikes + 1;
          }
        } else {
          // Milestone Hit!
          currentCount = config.endCount;
          currentSubsGain = config.baseSubsGain + (config.endCount - config.startCount);
          viewsEl.textContent = `${(config.baseViews + 0.4).toFixed(1)}k`;
          watchEl.textContent = `${(config.baseWatchTime + 0.2).toFixed(1)}k`;
          quickViewsEl.textContent = `${(config.baseVideoViews + 0.15).toFixed(1)}k`;
          detailViewsEl.textContent = `${(config.baseVideoViews + 0.15).toFixed(1)}k`;
          quickLikesEl.textContent = config.baseVideoLikes + 1;

          if (!milestoneTriggered) {
            milestoneTriggered = true;
            window.MILESTONE_TIME_MS = elapsed;
            counterEl.classList.add("milestone");
            subsGainEl.classList.add("milestone");
            const island = document.getElementById("dynamic-island");
            if (island) {
              island.classList.add("expanded");
              const msg = document.getElementById("island-milestone-msg");
              if (msg) msg.textContent = `${Number(config.endCount).toLocaleString()} Subs Reached!`;
            }
            triggerConfetti();
          }
        }

        counterEl.textContent = Number(currentCount).toLocaleString();
        subsGainEl.textContent = `+${currentSubsGain}`;
      }

      if (elapsed < totalDurationMs) {
        requestAnimationFrame(updateTimeline);
      } else {
        window.ANIMATION_COMPLETED = true;
      }
    }

    requestAnimationFrame(updateTimeline);
