from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
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
      --bg: #f7f4ee;
      --panel: #fffdf9;
      --ink: #242424;
      --muted: #6a6a6a;
      --accent: #0f766e;
      --accent-2: #b45309;
      --line: #d4d0c8;
    }
    body {
      margin: 0;
      font-family: "Avenir Next", "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #fffaf0, var(--bg));
      color: var(--ink);
    }
    .wrap {
      max-width: 1100px;
      margin: 0 auto;
      padding: 20px;
      display: grid;
      grid-template-columns: 1fr 300px;
      gap: 16px;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .controls {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }
    button {
      border: 1px solid var(--line);
      background: #fff;
      color: var(--ink);
      border-radius: 8px;
      padding: 8px 12px;
      cursor: pointer;
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
      border-radius: 10px;
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #eef7f7, #e6f1e8);
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
      padding: 6px 8px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: #fff;
    }
    input[type=checkbox] {
      width: auto;
    }
    #scenario-select {
      width: 170px;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="panel">
      <div class="controls">
        <select id="scenario-select"></select>
        <button id="switch-scenario">Switch Scenario</button>
        <button id="play" class="primary">Play</button>
        <button id="pause">Pause</button>
        <button id="step">Step</button>
        <button id="reset" class="secondary">Reset</button>
      </div>
      <canvas id="sim-canvas" width="900" height="600"></canvas>
    </section>
    <aside class="panel">
      <h3 style="margin: 6px 0 10px 0;">M1 Live State</h3>
      <div class="stat">Scenario: <strong id="scenario">-</strong></div>
      <div class="stat">Tick: <strong id="tick">0</strong></div>
      <div class="stat">Paused: <strong id="paused">true</strong></div>
      <div class="stat">Agents: <strong id="agents">0</strong></div>
      <div class="stat">Carrying: <strong id="carrying">0</strong></div>
      <div class="stat">Signal total: <strong id="signal">0.00</strong></div>
      <div class="row">
        <label for="speed">Speed</label>
        <input id="speed" type="number" min="0.1" step="0.1" value="1.0" />
        <button id="set-speed">Apply</button>
      </div>
      <div class="row">
        <label for="seek-tick">Seek tick</label>
        <input id="seek-tick" type="number" min="0" step="1" value="0" />
        <button id="seek-btn">Seek</button>
        <button id="rewind-10">Rewind 10</button>
      </div>
      <div class="row">
        <label for="show-signal">Signal overlay</label>
        <input id="show-signal" type="checkbox" />
      </div>
    </aside>
  </div>
<script>
const canvas = document.getElementById("sim-canvas");
const ctx = canvas.getContext("2d");
const scenarioSelect = document.getElementById("scenario-select");
const seekTickInput = document.getElementById("seek-tick");
const showSignalToggle = document.getElementById("show-signal");
let latest = null;
let meta = null;

async function postJson(url, payload) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
  });
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

  for (let y = 0; y < state.signal.data.length; y++) {
    const row = state.signal.data[y];
    for (let x = 0; x < row.length; x++) {
      const value = row[x];
      if (value <= 0) continue;
      const alpha = Math.min(0.45, (value / maxSignal) * 0.45);
      ctx.fillStyle = `rgba(180, 83, 9, ${alpha.toFixed(3)})`;
      ctx.fillRect(x * sx, y * sy, Math.ceil(sx), Math.ceil(sy));
    }
  }
}

function drawState(state) {
  const width = canvas.width;
  const height = canvas.height;
  ctx.clearRect(0, 0, width, height);
  if (!state) return;

  const worldW = state.world.width;
  const worldH = state.world.height;
  const sx = width / worldW;
  const sy = height / worldH;

  drawSignalOverlay(state, sx, sy);

  ctx.fillStyle = "#1f2937";
  ctx.beginPath();
  ctx.arc(state.colony.x * sx, state.colony.y * sy, 7, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#16a34a";
  for (const food of state.food_sources) {
    ctx.beginPath();
    ctx.rect(food.x * sx - 4, food.y * sy - 4, 8, 8);
    ctx.fill();
  }

  for (const agent of state.agents) {
    ctx.fillStyle = agent.carrying > 0 ? "#dc2626" : "#0f766e";
    ctx.beginPath();
    ctx.arc(agent.x * sx, agent.y * sy, 4, 0, Math.PI * 2);
    ctx.fill();
  }
}

function render() {
  if (!latest) return;
  document.getElementById("scenario").textContent = latest.scenario;
  document.getElementById("tick").textContent = String(latest.tick);
  document.getElementById("paused").textContent = String(latest.paused);
  document.getElementById("agents").textContent = String(latest.metrics.agent_count);
  document.getElementById("carrying").textContent = String(latest.metrics.carrying_agents);
  document.getElementById("signal").textContent = latest.metrics.signal_total.toFixed(2);
  seekTickInput.max = String(Math.max(0, latest.tick));
  if (scenarioSelect.value !== latest.scenario) {
    scenarioSelect.value = latest.scenario;
  }
  drawState(latest);
}

async function refresh() {
  try {
    const res = await fetch("/api/state");
    latest = await res.json();
    render();
  } catch (_err) {
    // Keep UI resilient while server is restarting.
  }
}

async function loadMeta() {
  const res = await fetch("/api/meta");
  meta = await res.json();
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
document.getElementById("switch-scenario").onclick = () => {
  switchScenario(scenarioSelect.value);
};
showSignalToggle.onchange = () => render();

loadMeta().then(refresh);
setInterval(refresh, 120);
</script>
</body>
</html>
"""


def _make_handler(bridge: WebRuntimeBridge):
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

            if self.path == "/health":
                self._json({"ok": True})
                return

            self._json({"error": "not found"}, status=404)

        def do_POST(self) -> None:  # noqa: N802 - stdlib hook name
            if self.path not in {"/api/command", "/api/scenario"}:
                self._json({"error": "not found"}, status=404)
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
    def __init__(self, *, host: str, port: int, bridge: WebRuntimeBridge) -> None:
        self._bridge = bridge
        self._httpd = ThreadingHTTPServer((host, port), _make_handler(bridge))

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
    server = WebShellServer(host=args.host, port=args.port, bridge=bridge)
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
