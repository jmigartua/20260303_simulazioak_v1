from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Sequence

from sim_framework.adapters.web.runtime_bridge import BridgeConfig, WebRuntimeBridge
from sim_framework.app.runtime import RuntimeMode
from sim_framework.scenarios.registry import list_scenarios


_SHELL_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>sim-framework M1 shell</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #efe9dc;
      --panel: #fffdf8;
      --ink: #1f2937;
      --muted: #6b7280;
      --accent: #0f766e;
      --accent-2: #c06210;
      --line: #d6d0c2;
      --stage: #15202b;
      --stage-2: #0f1720;
      --good: #16a34a;
      --warn: #f59e0b;
      --info: #60a5fa;
    }
    body {
      margin: 0;
      font-family: "Avenir Next", "IBM Plex Sans", "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(255,255,255,0.75), transparent 30%),
        linear-gradient(180deg, #f7f3ea 0%, var(--bg) 100%);
      color: var(--ink);
    }
    .wrap {
      max-width: 1260px;
      margin: 0 auto;
      padding: 18px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 360px;
      gap: 18px;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 12px 35px rgba(39, 28, 10, 0.08);
    }
    .controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }
    button {
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.92);
      color: var(--ink);
      border-radius: 12px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 600;
    }
    button.primary {
      background: var(--accent);
      color: #fff;
      border-color: transparent;
    }
    button.secondary {
      background: var(--accent-2);
      color: #fff;
      border-color: transparent;
    }
    #sim-canvas {
      width: 100%;
      aspect-ratio: 1.2;
      border-radius: 16px;
      border: 1px solid rgba(255,255,255,0.2);
      background: linear-gradient(180deg, var(--stage), var(--stage-2));
      box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
    }
    .stat {
      margin: 6px 0;
      font-size: 14px;
      color: var(--muted);
    }
    .stat strong {
      color: var(--ink);
      font-weight: 700;
    }
    .row {
      display: flex;
      gap: 8px;
      align-items: center;
      margin-top: 8px;
    }
    input[type=number], select {
      width: 80px;
      padding: 8px 10px;
      border-radius: 10px;
      border: 1px solid var(--line);
      background: #fff;
    }
    input[type=range] {
      width: 150px;
    }
    input[type=checkbox] {
      width: auto;
    }
    #scenario-select {
      width: 220px;
    }
    #capture-list {
      width: 100%;
    }
    .canvas-meta {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }
    .chip {
      border-radius: 999px;
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      border: 1px solid rgba(0,0,0,0.06);
    }
    .chip.stage {
      background: rgba(21, 32, 43, 0.08);
      color: #0f172a;
    }
    .chip.nest {
      background: rgba(15, 118, 110, 0.12);
      color: #0f766e;
    }
    .chip.forage {
      background: rgba(245, 158, 11, 0.14);
      color: #b45309;
    }
    .chip.signal {
      background: rgba(59, 130, 246, 0.14);
      color: #1d4ed8;
    }
    .hero {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 12px;
      margin-bottom: 12px;
    }
    .hero h3 {
      margin: 0;
      font-size: 15px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    .hero p {
      margin: 0;
      font-size: 13px;
      color: var(--muted);
    }
    .metric-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin: 10px 0 12px;
    }
    .metric-card {
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 10px 12px;
      background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(247, 244, 238, 0.92));
    }
    .metric-card span {
      display: block;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
      margin-bottom: 4px;
    }
    .metric-card strong {
      font-size: 24px;
      line-height: 1;
    }
    .progress-block {
      margin: 12px 0;
    }
    .progress-block label {
      display: flex;
      justify-content: space-between;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .progress-track {
      position: relative;
      overflow: hidden;
      height: 11px;
      border-radius: 999px;
      background: #ebe4d4;
    }
    .progress-fill {
      height: 100%;
      border-radius: inherit;
      transition: width 120ms linear;
    }
    #food-progress {
      background: linear-gradient(90deg, #16a34a, #84cc16);
    }
    #delivery-progress {
      background: linear-gradient(90deg, #f59e0b, #f97316);
    }
    .legend {
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 12px;
      margin: 12px 0;
      background: rgba(255,255,255,0.78);
    }
    .legend h4 {
      margin: 0 0 10px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--muted);
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 6px 0;
      font-size: 13px;
      color: var(--ink);
    }
    .swatch {
      width: 12px;
      height: 12px;
      border-radius: 999px;
      flex: 0 0 auto;
    }
    .swatch.zone {
      border-radius: 4px;
    }
    .swatch.searching { background: #2dd4bf; }
    .swatch.carrying { background: #f97316; }
    .swatch.food { background: #84cc16; border-radius: 4px; }
    .swatch.nest { background: rgba(45, 212, 191, 0.45); border-radius: 4px; }
    .swatch.forage { background: rgba(245, 158, 11, 0.45); border-radius: 4px; }
    .swatch.obstacle { background: #52525b; border-radius: 4px; }
    .capture-path {
      display: block;
      font-size: 12px;
      line-height: 1.35;
      overflow-wrap: anywhere;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="panel">
      <div class="hero">
        <h3>Simulation Stage</h3>
        <p id="scene-summary">Foragers leaving nest, probing forage zones, and returning with food.</p>
      </div>
      <div class="controls">
        <select id="scenario-select"></select>
        <button id="switch-scenario">Switch Scenario</button>
        <button id="play" class="primary">Play</button>
        <button id="pause">Pause</button>
        <button id="step">Step</button>
        <button id="reset" class="secondary">Reset</button>
        <button id="capture-json">Capture JSON</button>
        <button id="capture-png">Capture PNG</button>
      </div>
      <div class="canvas-meta">
        <div class="chip stage">Live Terrain</div>
        <div class="chip nest">Nest Zone</div>
        <div class="chip forage">Forage Zones</div>
        <div class="chip signal">Signal Field</div>
      </div>
      <canvas id="sim-canvas" width="900" height="600"></canvas>
    </section>
    <aside class="panel">
      <div class="hero">
        <h3>M1 Live State</h3>
        <p id="hud-summary">Operational overview</p>
      </div>
      <div class="stat">Renderer: <strong id="renderer">-</strong></div>
      <div class="stat">Target tick Hz: <strong id="target-hz">-</strong></div>
      <div class="stat">Refresh Hz: <strong id="fps">0.0</strong></div>
      <div class="stat">API latency ms: <strong id="latency">0.0</strong></div>
      <div class="stat">Tick drift: <strong id="drift">0</strong></div>
      <div class="stat">Last capture: <strong id="capture-path" class="capture-path">-</strong></div>
      <div class="stat">Capture files: <strong id="capture-count">0</strong></div>
      <div class="stat">Scenario: <strong id="scenario">-</strong></div>
      <div class="stat">Tick: <strong id="tick">0</strong></div>
      <div class="stat">Paused: <strong id="paused">true</strong></div>
      <div class="metric-grid">
        <div class="metric-card">
          <span>Agents</span>
          <strong id="agents">0</strong>
        </div>
        <div class="metric-card">
          <span>Carrying</span>
          <strong id="carrying">0</strong>
        </div>
        <div class="metric-card">
          <span>Delivered</span>
          <strong id="delivered">0</strong>
        </div>
        <div class="metric-card">
          <span>Signal</span>
          <strong id="signal">0.00</strong>
        </div>
      </div>
      <div class="progress-block">
        <label><span>Food Remaining</span><strong id="food-remaining">0.00</strong></label>
        <div class="progress-track"><div id="food-progress" class="progress-fill" style="width: 0%;"></div></div>
      </div>
      <div class="progress-block">
        <label><span>Delivery Progress</span><strong id="delivery-ratio">0 / 0</strong></label>
        <div class="progress-track"><div id="delivery-progress" class="progress-fill" style="width: 0%;"></div></div>
      </div>
      <div class="legend">
        <h4>Scene Legend</h4>
        <div class="legend-item"><span class="swatch searching"></span><span>Searching ants</span></div>
        <div class="legend-item"><span class="swatch carrying"></span><span>Returning with food</span></div>
        <div class="legend-item"><span class="swatch food"></span><span>Food deposits</span></div>
        <div class="legend-item"><span class="swatch zone nest"></span><span>Nest and colony core</span></div>
        <div class="legend-item"><span class="swatch zone forage"></span><span>Forage targets</span></div>
        <div class="legend-item"><span class="swatch obstacle"></span><span>Structural obstacles</span></div>
      </div>
      <div class="row">
        <label for="speed">Speed</label>
        <input id="speed" type="number" min="0.1" step="0.1" value="1.0" />
        <button id="set-speed">Apply</button>
      </div>
      <div class="row">
        <label for="timeline-slider">Timeline</label>
        <input id="timeline-slider" type="range" min="0" max="0" value="0" />
        <strong id="timeline-label">0 / 0</strong>
      </div>
      <div class="row">
        <label for="seek-tick">Seek tick</label>
        <input id="seek-tick" type="number" min="0" step="1" value="0" />
        <button id="seek-btn">Seek</button>
        <button id="rewind-10">Rewind 10</button>
        <button id="rewind-50">Rewind 50</button>
        <button id="jump-latest">Jump Latest</button>
      </div>
      <div class="row">
        <label for="show-signal">Signal overlay</label>
        <input id="show-signal" type="checkbox" />
      </div>
      <div class="row">
        <label for="capture-list">Captures</label>
        <select id="capture-list"></select>
      </div>
      <div class="row">
        <button id="refresh-captures">Refresh Captures</button>
        <button id="delete-capture">Delete Capture</button>
      </div>
    </aside>
  </div>
<script src="https://cdn.jsdelivr.net/npm/pixi.js@7.4.2/dist/pixi.min.js"></script>
<script>
const canvas = document.getElementById("sim-canvas");
const scenarioSelect = document.getElementById("scenario-select");
const seekTickInput = document.getElementById("seek-tick");
const timelineSlider = document.getElementById("timeline-slider");
const timelineLabel = document.getElementById("timeline-label");
const showSignalToggle = document.getElementById("show-signal");
const rendererLabel = document.getElementById("renderer");
const targetHzLabel = document.getElementById("target-hz");
const fpsLabel = document.getElementById("fps");
const latencyLabel = document.getElementById("latency");
const driftLabel = document.getElementById("drift");
const capturePathLabel = document.getElementById("capture-path");
const captureCountLabel = document.getElementById("capture-count");
const captureList = document.getElementById("capture-list");
let latest = null;
let meta = null;
let pixiApp = null;
let pixiLayers = null;
let fallbackCtx = null;
let lastRenderTs = null;
let lastTick = null;
let lastApiLatencyMs = 0.0;
const agentTrails = new Map();
const TRAIL_MAX_POINTS = 14;

function initRenderer() {
  if (window.PIXI) {
    pixiApp = new PIXI.Application({
      view: canvas,
      width: canvas.width,
      height: canvas.height,
      antialias: true,
      backgroundColor: 0xeef7f7,
    });
    pixiLayers = {
      signal: new PIXI.Container(),
      terrain: new PIXI.Container(),
      agents: new PIXI.Container(),
    };
    pixiApp.stage.addChild(pixiLayers.signal);
    pixiApp.stage.addChild(pixiLayers.terrain);
    pixiApp.stage.addChild(pixiLayers.agents);
    rendererLabel.textContent = "PixiJS";
    return;
  }

  fallbackCtx = canvas.getContext("2d");
  rendererLabel.textContent = "Canvas fallback";
}

function signalColorForKind(kind) {
  if (kind === "radio") return 0x2563eb;
  if (kind === "thermal") return 0xea580c;
  return 0xb45309;
}

function signalRgbaForKind(kind, alpha) {
  if (kind === "radio") return `rgba(37, 99, 235, ${alpha.toFixed(3)})`;
  if (kind === "thermal") return `rgba(234, 88, 12, ${alpha.toFixed(3)})`;
  return `rgba(180, 83, 9, ${alpha.toFixed(3)})`;
}

function clearPixiContainer(container) {
  const children = container.removeChildren();
  for (const child of children) {
    if (child && typeof child.destroy === "function") {
      child.destroy();
    }
  }
}

function updateAgentTrails(state, sx, sy) {
  if (!state || !Array.isArray(state.agents)) return;
  const activeIds = new Set();
  for (const agent of state.agents) {
    const id = String(agent.id || "");
    if (!id) continue;
    activeIds.add(id);
    const x = agent.x * sx;
    const y = agent.y * sy;
    const trail = agentTrails.get(id) || [];
    const last = trail.length > 0 ? trail[trail.length - 1] : null;
    if (!last || Math.hypot(last.x - x, last.y - y) > 0.5) {
      trail.push({x, y});
      while (trail.length > TRAIL_MAX_POINTS) trail.shift();
      agentTrails.set(id, trail);
    }
  }
  for (const id of Array.from(agentTrails.keys())) {
    if (!activeIds.has(id)) {
      agentTrails.delete(id);
    }
  }
}

async function postJson(url, payload) {
  const t0 = performance.now();
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
  });
  lastApiLatencyMs = performance.now() - t0;
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "request failed");
  }
  return data;
}

async function postCommand(payload) {
  latest = await postJson("/api/command", payload);
  render();
}

async function switchScenario(scenarioName) {
  latest = await postJson("/api/scenario", {scenario: scenarioName});
  if (meta) {
    meta.current_scenario = scenarioName;
  }
  render();
}

async function captureJson() {
  const capture = await postJson("/api/capture", {});
  latest = capture.state;
  capturePathLabel.textContent = capture.capture_file;
  await refreshCaptures(capture.capture_name || null);
  render();
}

async function capturePng() {
  const dataUrl = canvas.toDataURL("image/png");
  const marker = "base64,";
  const idx = dataUrl.indexOf(marker);
  const encoded = idx >= 0 ? dataUrl.slice(idx + marker.length) : "";
  if (!encoded) return;
  const capture = await postJson("/api/capture/screenshot", {
    image_base64: encoded,
    mime_type: "image/png",
  });
  latest = capture.state;
  capturePathLabel.textContent = capture.bundle_file;
  await refreshCaptures(capture.capture_name || null);
  render();
}

async function refreshCaptures(preferredName = null) {
  try {
    const res = await fetch("/api/captures");
    if (!res.ok) return;
    const payload = await res.json();
    const captures = Array.isArray(payload.captures) ? payload.captures : [];
    const previous = preferredName || captureList.value || "";
    captureList.innerHTML = "";
    for (const capture of captures) {
      const option = document.createElement("option");
      option.value = String(capture.name || "");
      const tick = Number.isFinite(capture.tick) ? capture.tick : "?";
      option.textContent = `${capture.name} (tick ${tick})`;
      captureList.appendChild(option);
    }
    if (captures.length > 0) {
      const chosen = captures.some((item) => item.name === previous)
        ? previous
        : captures[0].name;
      captureList.value = chosen;
    }
    captureCountLabel.textContent = String(captures.length);
  } catch (_err) {
    // Keep UI usable when capture listing endpoint is unavailable.
  }
}

async function deleteSelectedCapture() {
  const name = captureList.value;
  if (!name) return;
  const payload = await postJson("/api/capture/delete", {name});
  const captures = Array.isArray(payload.captures) ? payload.captures : [];
  captureList.innerHTML = "";
  for (const capture of captures) {
    const option = document.createElement("option");
    option.value = String(capture.name || "");
    const tick = Number.isFinite(capture.tick) ? capture.tick : "?";
    option.textContent = `${capture.name} (tick ${tick})`;
    captureList.appendChild(option);
  }
  captureCountLabel.textContent = String(captures.length);
  if (captures.length === 0) {
    capturePathLabel.textContent = "-";
  }
}

function drawSignalOverlay(state, sx, sy) {
  if (!showSignalToggle.checked) return;
  if (!state.signal || !state.signal.data) return;

  let maxSignal = 0.0;
  for (const row of state.signal.data) {
    for (const value of row) {
      if (value > maxSignal) maxSignal = value;
    }
  }
  if (maxSignal <= 0) return;
  const signalKind = state.signal.kind || "pheromone";
  const pixiColor = signalColorForKind(signalKind);

  for (let y = 0; y < state.signal.data.length; y++) {
    const row = state.signal.data[y];
    for (let x = 0; x < row.length; x++) {
      const value = row[x];
      if (value <= 0) continue;
      const alpha = Math.min(0.45, (value / maxSignal) * 0.45);
      if (pixiApp) {
        const cell = new PIXI.Graphics();
        cell.beginFill(pixiColor, alpha);
        cell.drawRect(x * sx, y * sy, Math.ceil(sx), Math.ceil(sy));
        cell.endFill();
        pixiLayers.signal.addChild(cell);
      } else if (fallbackCtx) {
        fallbackCtx.fillStyle = signalRgbaForKind(signalKind, alpha);
        fallbackCtx.fillRect(x * sx, y * sy, Math.ceil(sx), Math.ceil(sy));
      }
    }
  }
}

function zoneStyle(zoneKind) {
  if (zoneKind === "forage") return {color: 0xf59e0b, alpha: 0.12, stroke: 0xf59e0b};
  if (zoneKind === "patrol") return {color: 0x2563eb, alpha: 0.08, stroke: 0x2563eb};
  if (zoneKind === "corridor") return {color: 0x7c3aed, alpha: 0.08, stroke: 0x7c3aed};
  return {color: 0x0f766e, alpha: 0.1, stroke: 0x0f766e};
}

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function totalFoodAmount(state) {
  return (state.food_sources || []).reduce((sum, source) => sum + Number(source.amount || 0), 0);
}

function progressMetrics(state) {
  const delivered = Number(state.metrics.delivered_food || 0);
  const remaining = totalFoodAmount(state);
  const total = Math.max(remaining + delivered, 1);
  return {
    delivered,
    remaining,
    total,
    remainingPct: clamp01(remaining / total) * 100,
    deliveredPct: clamp01(delivered / total) * 100,
  };
}

function scenarioSummary(state) {
  if (state.scenario === "drone_patrol") {
    return "Patrol drones are cycling the perimeter, clearing corridors, and preserving coverage.";
  }
  const delivered = Number(state.metrics.delivered_food || 0);
  const carrying = Number(state.metrics.carrying_agents || 0);
  const waiting = Number(state.metrics.waiting_agents || 0);
  const released = Number(state.metrics.released_agents || 0);
  if (!state.metrics.food_discovered) {
    return `${released} scouts are probing the field while ${waiting} workers remain at the nest.`;
  }
  if (delivered > 0 && carrying > 0) {
    return "Foragers are harvesting outer food zones and streaming resources back to the nest.";
  }
  if (delivered > 0) {
    return "A scout has returned to the nest and the worker column is now released toward the food trail.";
  }
  if (carrying > 0) {
    return "A scout has found food and is returning to the nest to trigger worker recruitment.";
  }
  return "Foragers are leaving the nest, probing forage zones, and establishing outbound routes.";
}

function hudSummary(state) {
  const zoneCount = Array.isArray(state.zones) ? state.zones.length : 0;
  const obstacleCount = Array.isArray(state.obstacles) ? state.obstacles.length : 0;
  if (state.scenario === "drone_patrol") {
    return `${state.metrics.agent_count} drones, ${zoneCount} patrol zones, ${obstacleCount} structural blocks`;
  }
  return `${state.metrics.agent_count} ants, ${state.metrics.waiting_agents || 0} waiting, ${obstacleCount} structural obstacles`;
}

function zoneLabel(zone) {
  if (zone.label) return String(zone.label);
  if (zone.kind === "forage") return "Forage";
  if (zone.kind === "patrol") return "Patrol";
  if (zone.kind === "corridor") return "Corridor";
  return "Nest";
}

function stageBackgroundPixi(width, height) {
  const backdrop = new PIXI.Graphics();
  backdrop.beginFill(0x08111d, 1.0);
  backdrop.drawRoundedRect(0, 0, width, height, 18);
  backdrop.endFill();
  pixiLayers.terrain.addChild(backdrop);

  const horizon = new PIXI.Graphics();
  horizon.beginFill(0x0f1f2b, 0.85);
  horizon.drawRoundedRect(12, 12, width - 24, height - 24, 16);
  horizon.endFill();
  pixiLayers.terrain.addChild(horizon);
}

function stageBackgroundCanvas(width, height) {
  fallbackCtx.fillStyle = "#08111d";
  fallbackCtx.beginPath();
  fallbackCtx.roundRect(0, 0, width, height, 18);
  fallbackCtx.fill();
  fallbackCtx.fillStyle = "#0f1f2b";
  fallbackCtx.beginPath();
  fallbackCtx.roundRect(12, 12, width - 24, height - 24, 16);
  fallbackCtx.fill();
}

function drawStatePixi(state) {
  if (!state || !pixiApp) return;
  clearPixiContainer(pixiLayers.signal);
  clearPixiContainer(pixiLayers.terrain);
  clearPixiContainer(pixiLayers.agents);

  const width = canvas.width;
  const height = canvas.height;
  const worldW = state.world.width;
  const worldH = state.world.height;
  const sx = width / worldW;
  const sy = height / worldH;
  const isDroneScenario = state.scenario === "drone_patrol";
  updateAgentTrails(state, sx, sy);

  stageBackgroundPixi(width, height);
  drawSignalOverlay(state, sx, sy);

  const frame = new PIXI.Graphics();
  frame.lineStyle(2.5, isDroneScenario ? 0x1d4ed8 : 0x94a3b8, 0.75);
  frame.drawRoundedRect(6, 6, width - 12, height - 12, 18);
  pixiLayers.terrain.addChild(frame);

  for (const zone of state.zones || []) {
    const style = zoneStyle(zone.kind);
    const rect = new PIXI.Graphics();
    rect.lineStyle(1.5, style.stroke, 0.65);
    rect.beginFill(style.color, style.alpha);
    rect.drawRoundedRect(zone.x * sx, zone.y * sy, zone.width * sx, zone.height * sy, 10);
    rect.endFill();
    pixiLayers.terrain.addChild(rect);

    const label = new PIXI.Text(zoneLabel(zone), {
      fill: 0xe2e8f0,
      fontSize: 12,
      fontWeight: "600",
    });
    label.alpha = 0.9;
    label.x = zone.x * sx + 10;
    label.y = zone.y * sy + 8;
    pixiLayers.terrain.addChild(label);
  }

  for (const obstacle of state.obstacles || []) {
    const block = new PIXI.Graphics();
    block.lineStyle(1, 0xf8fafc, 0.18);
    block.beginFill(0x52525b, 0.92);
    block.drawRoundedRect(
      obstacle.x * sx,
      obstacle.y * sy,
      obstacle.width * sx,
      obstacle.height * sy,
      4,
    );
    block.endFill();
    pixiLayers.terrain.addChild(block);
  }

  const colonyHalo = new PIXI.Graphics();
  colonyHalo.lineStyle(3, isDroneScenario ? 0x60a5fa : 0x2dd4bf, 0.35);
  colonyHalo.drawCircle(state.colony.x * sx, state.colony.y * sy, isDroneScenario ? 16 : 18);
  pixiLayers.terrain.addChild(colonyHalo);

  const colony = new PIXI.Graphics();
  colony.lineStyle(2, 0xffffff, 0.8);
  colony.beginFill(isDroneScenario ? 0x1e3a8a : 0x1f2937, 1.0);
  colony.drawCircle(state.colony.x * sx, state.colony.y * sy, isDroneScenario ? 10 : 11);
  colony.endFill();
  pixiLayers.terrain.addChild(colony);

  const colonyLabel = new PIXI.Text(isDroneScenario ? "Base" : "Nest", {
    fill: 0xf8fafc,
    fontSize: 12,
    fontWeight: "700",
  });
  colonyLabel.x = state.colony.x * sx + 14;
  colonyLabel.y = state.colony.y * sy - 22;
  pixiLayers.terrain.addChild(colonyLabel);

  if (isDroneScenario) {
    const margin = 2.0;
    const waypoints = [
      [margin, margin],
      [worldW - margin, margin],
      [worldW - margin, worldH - margin],
      [margin, worldH - margin],
    ];
    const path = new PIXI.Graphics();
    path.lineStyle(1.5, 0x1d4ed8, 0.85);
    path.moveTo(waypoints[0][0] * sx, waypoints[0][1] * sy);
    for (let i = 1; i < waypoints.length; i++) {
      path.lineTo(waypoints[i][0] * sx, waypoints[i][1] * sy);
    }
    path.lineTo(waypoints[0][0] * sx, waypoints[0][1] * sy);
    pixiLayers.terrain.addChild(path);
  }

  for (const food of state.food_sources) {
    const sprite = new PIXI.Graphics();
    const size = Math.max(10, Math.min(20, 8 + Math.sqrt(Math.max(food.amount, 1))));
    sprite.lineStyle(1.5, 0xeafff7, 0.9);
    sprite.beginFill(0x84cc16, 1.0);
    sprite.drawRoundedRect(food.x * sx - size / 2, food.y * sy - size / 2, size, size, 4);
    sprite.endFill();
    const core = new PIXI.Graphics();
    core.beginFill(0xecfccb, 0.9);
    core.drawCircle(food.x * sx, food.y * sy, Math.max(2.5, size * 0.2));
    core.endFill();
    pixiLayers.terrain.addChild(sprite);
    pixiLayers.terrain.addChild(core);
  }

  for (const trail of agentTrails.values()) {
    if (trail.length < 2) continue;
    const path = new PIXI.Graphics();
    path.lineStyle(1.4, 0xcbd5e1, 0.14);
    path.moveTo(trail[0].x, trail[0].y);
    for (let i = 1; i < trail.length; i++) {
      path.lineTo(trail[i].x, trail[i].y);
    }
    pixiLayers.terrain.addChild(path);
  }

  for (const agent of state.agents) {
    const sprite = new PIXI.Graphics();
    if (isDroneScenario) {
      sprite.beginFill(0x0f766e, 0.95);
      sprite.drawPolygon([
        agent.x * sx,
        agent.y * sy - 8,
        agent.x * sx + 6,
        agent.y * sy + 6,
        agent.x * sx - 6,
        agent.y * sy + 6,
      ]);
      sprite.endFill();
    } else {
      const color = agent.carrying > 0 ? 0xf97316 : 0x14b8a6;
      sprite.beginFill(color, 1.0);
      sprite.lineStyle(1.2, 0xf8fafc, 0.72);
      sprite.drawCircle(agent.x * sx, agent.y * sy, agent.carrying > 0 ? 6.2 : 5.8);
      sprite.endFill();

      const trail = agentTrails.get(agent.id);
      if (trail && trail.length >= 2) {
        const prev = trail[trail.length - 2];
        const dx = agent.x * sx - prev.x;
        const dy = agent.y * sy - prev.y;
        const mag = Math.hypot(dx, dy);
        if (mag > 0.25) {
          const heading = new PIXI.Graphics();
          heading.lineStyle(1.2, 0xffffff, 0.55);
          heading.moveTo(agent.x * sx, agent.y * sy);
          heading.lineTo(
            agent.x * sx + (dx / mag) * 8,
            agent.y * sy + (dy / mag) * 8,
          );
          pixiLayers.agents.addChild(heading);
        }
      }
    }
    pixiLayers.agents.addChild(sprite);
  }
}

function drawStateCanvasFallback(state) {
  if (!fallbackCtx) return;
  const width = canvas.width;
  const height = canvas.height;
  fallbackCtx.clearRect(0, 0, width, height);
  if (!state) return;

  const worldW = state.world.width;
  const worldH = state.world.height;
  const sx = width / worldW;
  const sy = height / worldH;
  const isDroneScenario = state.scenario === "drone_patrol";
  updateAgentTrails(state, sx, sy);

  stageBackgroundCanvas(width, height);
  drawSignalOverlay(state, sx, sy);

  fallbackCtx.strokeStyle = isDroneScenario ? "#1d4ed8" : "#94a3b8";
  fallbackCtx.lineWidth = 2.5;
  fallbackCtx.beginPath();
  fallbackCtx.roundRect(6, 6, width - 12, height - 12, 18);
  fallbackCtx.stroke();

  for (const zone of state.zones || []) {
    const style = zoneStyle(zone.kind);
    fallbackCtx.strokeStyle = `#${style.stroke.toString(16).padStart(6, "0")}`;
    fallbackCtx.fillStyle =
      zone.kind === "forage"
        ? "rgba(245, 158, 11, 0.12)"
        : zone.kind === "patrol"
          ? "rgba(37, 99, 235, 0.08)"
          : zone.kind === "corridor"
            ? "rgba(124, 58, 237, 0.08)"
            : "rgba(15, 118, 110, 0.10)";
    fallbackCtx.lineWidth = 1.5;
    fallbackCtx.beginPath();
    fallbackCtx.roundRect(zone.x * sx, zone.y * sy, zone.width * sx, zone.height * sy, 10);
    fallbackCtx.fill();
    fallbackCtx.stroke();
    fallbackCtx.fillStyle = "rgba(226, 232, 240, 0.92)";
    fallbackCtx.font = "600 12px ui-sans-serif, system-ui, sans-serif";
    fallbackCtx.fillText(zoneLabel(zone), zone.x * sx + 10, zone.y * sy + 22);
  }

  for (const obstacle of state.obstacles || []) {
    fallbackCtx.fillStyle = "rgba(82, 82, 91, 0.92)";
    fallbackCtx.strokeStyle = "rgba(248, 250, 252, 0.18)";
    fallbackCtx.lineWidth = 1;
    fallbackCtx.beginPath();
    fallbackCtx.roundRect(
      obstacle.x * sx,
      obstacle.y * sy,
      obstacle.width * sx,
      obstacle.height * sy,
      4,
    );
    fallbackCtx.fill();
    fallbackCtx.stroke();
  }

  fallbackCtx.strokeStyle = isDroneScenario ? "rgba(96, 165, 250, 0.35)" : "rgba(45, 212, 191, 0.35)";
  fallbackCtx.lineWidth = 3;
  fallbackCtx.beginPath();
  fallbackCtx.arc(state.colony.x * sx, state.colony.y * sy, isDroneScenario ? 16 : 18, 0, Math.PI * 2);
  fallbackCtx.stroke();
  fallbackCtx.fillStyle = isDroneScenario ? "#1e3a8a" : "#1f2937";
  fallbackCtx.strokeStyle = "rgba(248, 250, 252, 0.8)";
  fallbackCtx.lineWidth = 2;
  fallbackCtx.beginPath();
  fallbackCtx.arc(state.colony.x * sx, state.colony.y * sy, isDroneScenario ? 10 : 11, 0, Math.PI * 2);
  fallbackCtx.fill();
  fallbackCtx.stroke();
  fallbackCtx.fillStyle = "#f8fafc";
  fallbackCtx.font = "700 12px ui-sans-serif, system-ui, sans-serif";
  fallbackCtx.fillText(isDroneScenario ? "Base" : "Nest", state.colony.x * sx + 14, state.colony.y * sy - 12);

  if (isDroneScenario) {
    const margin = 2.0;
    const waypoints = [
      [margin, margin],
      [worldW - margin, margin],
      [worldW - margin, worldH - margin],
      [margin, worldH - margin],
    ];
    fallbackCtx.strokeStyle = "#1d4ed8";
    fallbackCtx.lineWidth = 1.5;
    fallbackCtx.beginPath();
    fallbackCtx.moveTo(waypoints[0][0] * sx, waypoints[0][1] * sy);
    for (let i = 1; i < waypoints.length; i++) {
      fallbackCtx.lineTo(waypoints[i][0] * sx, waypoints[i][1] * sy);
    }
    fallbackCtx.closePath();
    fallbackCtx.stroke();
  }

  for (const food of state.food_sources) {
    const size = Math.max(10, Math.min(20, 8 + Math.sqrt(Math.max(food.amount, 1))));
    fallbackCtx.fillStyle = "#84cc16";
    fallbackCtx.strokeStyle = "rgba(248, 250, 252, 0.9)";
    fallbackCtx.lineWidth = 1.5;
    fallbackCtx.beginPath();
    fallbackCtx.roundRect(food.x * sx - size / 2, food.y * sy - size / 2, size, size, 4);
    fallbackCtx.fill();
    fallbackCtx.stroke();
    fallbackCtx.fillStyle = "rgba(236, 252, 203, 0.9)";
    fallbackCtx.beginPath();
    fallbackCtx.arc(food.x * sx, food.y * sy, Math.max(2.5, size * 0.2), 0, Math.PI * 2);
    fallbackCtx.fill();
  }

  fallbackCtx.strokeStyle = "rgba(203, 213, 225, 0.14)";
  fallbackCtx.lineWidth = 1.4;
  for (const trail of agentTrails.values()) {
    if (trail.length < 2) continue;
    fallbackCtx.beginPath();
    fallbackCtx.moveTo(trail[0].x, trail[0].y);
    for (let i = 1; i < trail.length; i++) {
      fallbackCtx.lineTo(trail[i].x, trail[i].y);
    }
    fallbackCtx.stroke();
  }

  for (const agent of state.agents) {
    if (isDroneScenario) {
      fallbackCtx.fillStyle = "#0f766e";
      fallbackCtx.beginPath();
      fallbackCtx.moveTo(agent.x * sx, agent.y * sy - 8);
      fallbackCtx.lineTo(agent.x * sx + 6, agent.y * sy + 6);
      fallbackCtx.lineTo(agent.x * sx - 6, agent.y * sy + 6);
      fallbackCtx.closePath();
      fallbackCtx.fill();
    } else {
      fallbackCtx.fillStyle = agent.carrying > 0 ? "#f97316" : "#14b8a6";
      fallbackCtx.strokeStyle = "rgba(248, 250, 252, 0.75)";
      fallbackCtx.lineWidth = 1.2;
      fallbackCtx.beginPath();
      fallbackCtx.arc(agent.x * sx, agent.y * sy, agent.carrying > 0 ? 6.2 : 5.8, 0, Math.PI * 2);
      fallbackCtx.fill();
      fallbackCtx.stroke();

      const trail = agentTrails.get(agent.id);
      if (trail && trail.length >= 2) {
        const prev = trail[trail.length - 2];
        const dx = agent.x * sx - prev.x;
        const dy = agent.y * sy - prev.y;
        const mag = Math.hypot(dx, dy);
        if (mag > 0.25) {
          fallbackCtx.strokeStyle = "rgba(255, 255, 255, 0.55)";
          fallbackCtx.lineWidth = 1.2;
          fallbackCtx.beginPath();
          fallbackCtx.moveTo(agent.x * sx, agent.y * sy);
          fallbackCtx.lineTo(
            agent.x * sx + (dx / mag) * 8,
            agent.y * sy + (dy / mag) * 8,
          );
          fallbackCtx.stroke();
        }
      }
    }
  }
}

function drawState(state) {
  if (pixiApp) {
    drawStatePixi(state);
  } else {
    drawStateCanvasFallback(state);
  }
}

function render() {
  if (!latest) return;
  const now = performance.now();
  if (lastRenderTs !== null) {
    const dt = now - lastRenderTs;
    if (dt > 0) {
      const hz = 1000 / dt;
      fpsLabel.textContent = hz.toFixed(1);
    }
  }
  lastRenderTs = now;
  if (lastTick !== null) {
    if (latest.tick < lastTick) {
      agentTrails.clear();
    }
    driftLabel.textContent = String(latest.tick - lastTick);
  }
  lastTick = latest.tick;
  document.getElementById("scenario").textContent = latest.scenario;
  document.getElementById("tick").textContent = String(latest.tick);
  document.getElementById("paused").textContent = String(latest.paused);
  document.getElementById("agents").textContent = String(latest.metrics.agent_count);
  document.getElementById("carrying").textContent = String(latest.metrics.carrying_agents);
  document.getElementById("food-remaining").textContent = Number(
    latest.metrics.food_remaining || 0,
  ).toFixed(2);
  document.getElementById("delivered").textContent = String(latest.metrics.delivered_food || 0);
  document.getElementById("signal").textContent = latest.metrics.signal_total.toFixed(2);
  document.getElementById("scene-summary").textContent = scenarioSummary(latest);
  document.getElementById("hud-summary").textContent = hudSummary(latest);
  const progress = progressMetrics(latest);
  document.getElementById("food-progress").style.width = `${progress.remainingPct.toFixed(1)}%`;
  document.getElementById("delivery-progress").style.width = `${progress.deliveredPct.toFixed(1)}%`;
  document.getElementById("delivery-ratio").textContent = `${progress.delivered} / ${progress.total.toFixed(0)}`;
  latencyLabel.textContent = lastApiLatencyMs.toFixed(1);
  const maxTick = latest.timeline ? latest.timeline.max_tick_reached : latest.tick;
  seekTickInput.max = String(Math.max(0, maxTick));
  timelineSlider.max = String(Math.max(0, maxTick));
  timelineSlider.value = String(Math.max(0, latest.tick));
  timelineLabel.textContent = `${latest.tick} / ${maxTick}`;
  if (scenarioSelect.value !== latest.scenario) {
    scenarioSelect.value = latest.scenario;
  }
  drawState(latest);
}

async function refresh() {
  try {
    const t0 = performance.now();
    const res = await fetch("/api/state");
    lastApiLatencyMs = performance.now() - t0;
    latest = await res.json();
    render();
  } catch (_err) {
    // Keep UI resilient while server is restarting.
  }
}

async function loadMeta() {
  const res = await fetch("/api/meta");
  meta = await res.json();
  targetHzLabel.textContent = Number(meta.target_tick_hz).toFixed(2);
  scenarioSelect.innerHTML = "";
  for (const scenario of meta.available_scenarios) {
    const option = document.createElement("option");
    option.value = scenario;
    option.textContent = scenario;
    scenarioSelect.appendChild(option);
  }
  scenarioSelect.value = meta.current_scenario;
}

document.getElementById("play").onclick = () => postCommand({kind: "play"});
document.getElementById("pause").onclick = () => postCommand({kind: "pause"});
document.getElementById("step").onclick = () => postCommand({kind: "step", steps: 1});
document.getElementById("reset").onclick = () => postCommand({kind: "reset"});
document.getElementById("set-speed").onclick = () => {
  const speed = Number(document.getElementById("speed").value);
  postCommand({kind: "set_speed", speed_multiplier: speed});
};
document.getElementById("seek-btn").onclick = () => {
  const tick = Math.max(0, Math.floor(Number(seekTickInput.value)));
  postCommand({kind: "seek", tick});
};
document.getElementById("rewind-10").onclick = () => {
  if (!latest) return;
  const tick = Math.max(0, latest.tick - 10);
  seekTickInput.value = String(tick);
  postCommand({kind: "seek", tick});
};
document.getElementById("rewind-50").onclick = () => {
  if (!latest) return;
  const tick = Math.max(0, latest.tick - 50);
  seekTickInput.value = String(tick);
  postCommand({kind: "seek", tick});
};
document.getElementById("jump-latest").onclick = () => {
  if (!latest || !latest.timeline) return;
  const tick = Math.max(0, latest.timeline.max_tick_reached);
  seekTickInput.value = String(tick);
  postCommand({kind: "seek", tick});
};
timelineSlider.oninput = () => {
  const tick = Math.max(0, Math.floor(Number(timelineSlider.value)));
  seekTickInput.value = String(tick);
  const max = Number(timelineSlider.max || "0");
  timelineLabel.textContent = `${tick} / ${max}`;
};
timelineSlider.onchange = () => {
  const tick = Math.max(0, Math.floor(Number(timelineSlider.value)));
  seekTickInput.value = String(tick);
  postCommand({kind: "seek", tick});
};
document.getElementById("switch-scenario").onclick = () => {
  switchScenario(scenarioSelect.value);
};
document.getElementById("capture-json").onclick = () => {
  captureJson();
};
document.getElementById("capture-png").onclick = () => {
  capturePng();
};
document.getElementById("refresh-captures").onclick = () => {
  refreshCaptures();
};
document.getElementById("delete-capture").onclick = () => {
  deleteSelectedCapture();
};
showSignalToggle.onchange = () => render();

initRenderer();
loadMeta().then(() => {
  refresh();
  refreshCaptures();
});
setInterval(refresh, 120);
</script>
</body>
</html>
"""


_MAX_SCREENSHOT_BASE64_CHARS = 12_000_000


def _capture_digest_for_payload(payload: dict[str, Any]) -> str:
    stable_blob = json.dumps(
        {"state": payload["state"], "meta": payload["meta"]},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(stable_blob.encode("utf-8")).hexdigest()


def _capture_payload(bridge: WebRuntimeBridge) -> dict[str, Any]:
    payload = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "state": bridge.state_payload(),
        "meta": bridge.meta_payload(),
    }
    payload["capture_digest"] = _capture_digest_for_payload(payload)
    return payload


def _capture_basename(payload: dict[str, Any]) -> str:
    state = payload.get("state", {})
    scenario = str(state.get("scenario", "unknown"))
    tick = int(state.get("tick", 0))
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"capture_{scenario}_tick{tick}_{timestamp}"


def _write_capture_file(capture_root: Path, payload: dict[str, Any]) -> Path:
    capture_root.mkdir(parents=True, exist_ok=True)
    out_path = capture_root / f"{_capture_basename(payload)}.json"
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path


def _decode_png_bytes_from_payload(payload: dict[str, Any]) -> bytes:
    encoded = payload.get("image_base64")
    if not isinstance(encoded, str) or not encoded:
        raise ValueError("image_base64 must be a non-empty string")
    if len(encoded) > _MAX_SCREENSHOT_BASE64_CHARS:
        raise ValueError("image_base64 payload exceeds size limit")
    mime_type = payload.get("mime_type", "image/png")
    if mime_type != "image/png":
        raise ValueError("mime_type must be image/png")
    try:
        image_bytes = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ValueError("image_base64 is not valid base64") from exc
    if not image_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("image payload is not a PNG file")
    return image_bytes


def _write_screenshot_bundle(
    capture_root: Path,
    *,
    payload: dict[str, Any],
    image_bytes: bytes,
) -> tuple[Path, Path, dict[str, Any]]:
    capture_root.mkdir(parents=True, exist_ok=True)
    base = _capture_basename(payload)
    image_path = capture_root / f"{base}.png"
    bundle_path = capture_root / f"{base}_screenshot.json"

    image_path.write_bytes(image_bytes)
    image_digest = hashlib.sha256(image_bytes).hexdigest()
    bundle = {
        "captured_at_utc": payload["captured_at_utc"],
        "state": payload["state"],
        "meta": payload["meta"],
        "capture_digest": payload["capture_digest"],
        "image_file": str(image_path),
        "image_digest": image_digest,
        "bundle_digest": hashlib.sha256(
            json.dumps(
                {
                    "state": payload["state"],
                    "meta": payload["meta"],
                    "image_digest": image_digest,
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest(),
    }
    bundle_path.write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
    return image_path, bundle_path, bundle


def _capture_path_from_name(capture_root: Path, name: str) -> Path:
    if not name:
        raise ValueError("capture name must be non-empty")
    if "/" in name or "\\" in name:
        raise ValueError("capture name must be a plain filename")
    if not name.endswith(".json"):
        raise ValueError("capture name must end with .json")
    root = capture_root.resolve()
    candidate = (capture_root / name).resolve()
    if candidate.parent != root:
        raise ValueError("capture name points outside capture root")
    return candidate


def _capture_index_entry(path: Path) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "name": path.name,
        "path": str(path),
        "size_bytes": path.stat().st_size,
    }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return entry

    state = payload.get("state", {})
    entry["scenario"] = state.get("scenario")
    entry["tick"] = state.get("tick")
    entry["captured_at_utc"] = payload.get("captured_at_utc")
    entry["capture_digest"] = payload.get("capture_digest")
    if "image_file" in payload:
        entry["kind"] = "screenshot_bundle"
        entry["image_file"] = payload.get("image_file")
        entry["image_digest"] = payload.get("image_digest")
        entry["bundle_digest"] = payload.get("bundle_digest")
    else:
        entry["kind"] = "state_capture"
    return entry


def _list_capture_index(capture_root: Path) -> list[dict[str, Any]]:
    if not capture_root.exists():
        return []
    files = sorted(
        capture_root.glob("capture_*.json"),
        key=lambda item: item.stat().st_mtime,
        reverse=True,
    )
    return [_capture_index_entry(path) for path in files]


def _make_handler(bridge: WebRuntimeBridge, *, capture_root: Path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, _format: str, *_args) -> None:
            return

        def _json(self, payload: dict[str, Any], *, status: int = 200) -> None:
            encoded = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self) -> None:  # noqa: N802 - stdlib hook name
            if self.path in {"/", "/index.html"}:
                body = _SHELL_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if self.path == "/api/state":
                self._json(bridge.state_payload())
                return
            if self.path == "/api/meta":
                self._json(bridge.meta_payload())
                return
            if self.path == "/api/captures":
                self._json({"captures": _list_capture_index(capture_root)})
                return

            if self.path == "/health":
                self._json({"ok": True})
                return

            self._json({"error": "not found"}, status=404)

        def do_POST(self) -> None:  # noqa: N802 - stdlib hook name
            if self.path not in {
                "/api/command",
                "/api/scenario",
                "/api/capture",
                "/api/capture/screenshot",
                "/api/capture/delete",
            }:
                self._json({"error": "not found"}, status=404)
                return

            if self.path == "/api/capture":
                payload = _capture_payload(bridge)
                out_path = _write_capture_file(capture_root, payload)
                self._json(
                    {
                        "capture_file": str(out_path),
                        "capture_name": out_path.name,
                        "state": payload["state"],
                        "captured_at_utc": payload["captured_at_utc"],
                        "capture_digest": payload["capture_digest"],
                    },
                    status=200,
                )
                return

            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                self._json({"error": "empty payload"}, status=400)
                return

            raw = self.rfile.read(length)
            try:
                payload = json.loads(raw.decode("utf-8"))
            except json.JSONDecodeError:
                self._json({"error": "invalid json"}, status=400)
                return

            try:
                if self.path == "/api/capture/screenshot":
                    image_bytes = _decode_png_bytes_from_payload(payload)
                    capture_payload = _capture_payload(bridge)
                    image_path, bundle_path, bundle = _write_screenshot_bundle(
                        capture_root,
                        payload=capture_payload,
                        image_bytes=image_bytes,
                    )
                    self._json(
                        {
                            "capture_file": str(image_path),
                            "capture_name": bundle_path.name,
                            "image_file": str(image_path),
                            "bundle_file": str(bundle_path),
                            "state": capture_payload["state"],
                            "captured_at_utc": capture_payload["captured_at_utc"],
                            "capture_digest": capture_payload["capture_digest"],
                            "image_digest": bundle["image_digest"],
                            "bundle_digest": bundle["bundle_digest"],
                        },
                        status=200,
                    )
                    return
                if self.path == "/api/capture/delete":
                    name = payload.get("name")
                    if not isinstance(name, str):
                        self._json({"error": "name must be a string"}, status=400)
                        return
                    try:
                        target = _capture_path_from_name(capture_root, name)
                    except ValueError as exc:
                        self._json({"error": str(exc)}, status=400)
                        return
                    if not target.exists():
                        self._json({"error": f"capture not found: {name}"}, status=404)
                        return
                    try:
                        target_payload = json.loads(target.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        target_payload = {}
                    target.unlink()
                    image_file = target_payload.get("image_file")
                    if isinstance(image_file, str):
                        try:
                            image_path = Path(image_file).resolve()
                            if image_path.parent == capture_root.resolve() and image_path.exists():
                                image_path.unlink()
                        except OSError:
                            pass
                    self._json(
                        {
                            "deleted": name,
                            "captures": _list_capture_index(capture_root),
                        },
                        status=200,
                    )
                    return
                if self.path == "/api/scenario":
                    scenario_name = payload.get("scenario")
                    if not isinstance(scenario_name, str) or not scenario_name:
                        self._json({"error": "scenario must be a non-empty string"}, status=400)
                        return
                    bridge.switch_scenario(scenario_name)
                else:
                    bridge.apply_command(payload)
            except ValueError as exc:
                self._json({"error": str(exc)}, status=400)
                return
            self._json(bridge.state_payload(), status=200)

    return Handler


class WebShellServer:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        bridge: WebRuntimeBridge,
        capture_root: Path | None = None,
    ) -> None:
        self._bridge = bridge
        self._capture_root = capture_root or Path("captures")
        self._httpd = ThreadingHTTPServer(
            (host, port),
            _make_handler(bridge, capture_root=self._capture_root),
        )

    @property
    def port(self) -> int:
        return int(self._httpd.server_address[1])

    def start(self) -> None:
        self._bridge.start()

    def serve_forever(self) -> None:
        self._httpd.serve_forever(poll_interval=0.2)

    def shutdown(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        self._bridge.stop()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Launch the M1 web app shell.")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--scenario", type=str, default="ants_foraging", choices=list_scenarios())
    parser.add_argument("--agents", type=int, default=40)
    parser.add_argument("--width", type=int, default=30)
    parser.add_argument("--height", type=int, default=30)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--boundary-mode",
        type=str,
        choices=["clamp", "wrap"],
        default="clamp",
    )
    parser.add_argument(
        "--runtime-mode",
        type=str,
        choices=[mode.value for mode in RuntimeMode],
        default=RuntimeMode.INTERACTIVE.value,
    )
    parser.add_argument(
        "--step-interval-ms",
        type=int,
        default=50,
        help="Background simulation step interval in milliseconds.",
    )
    parser.add_argument(
        "--capture-root",
        type=Path,
        default=Path("captures"),
        help="Directory where /api/capture writes JSON snapshots.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.agents <= 0:
        parser.error("--agents must be > 0")
    if args.width <= 0 or args.height <= 0:
        parser.error("--width/--height must be > 0")
    if args.step_interval_ms <= 0:
        parser.error("--step-interval-ms must be > 0")

    bridge = WebRuntimeBridge(
        BridgeConfig(
            scenario_name=args.scenario,
            agents=args.agents,
            width=args.width,
            height=args.height,
            seed=args.seed,
            boundary_mode=args.boundary_mode,
            runtime_mode=RuntimeMode(args.runtime_mode),
            step_interval_s=args.step_interval_ms / 1000.0,
        )
    )
    server = WebShellServer(
        host=args.host,
        port=args.port,
        bridge=bridge,
        capture_root=args.capture_root,
    )
    server.start()

    print(
        json.dumps(
            {
                "mode": "m1-web-shell",
                "url": f"http://{args.host}:{server.port}/",
                "scenario": args.scenario,
                "agents": args.agents,
            },
            indent=2,
        )
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
