"""Generates assets/terminal.svg — an animated "about me" terminal.

Commands are typed out character by character (SMIL clip animation),
outputs fade in right after. Edit LINES and re-run:  python3 scripts/build_terminal.py
"""
from html import escape
from pathlib import Path

W = 900
FONT = 16
CHAR_W = FONT * 0.602  # monospace advance
LINE_H = 27
TOP = 70
LEFT = 28
TYPE_SPEED = 0.045  # seconds per char
PAUSE = 0.35

PROMPT = [("alx", "#22d3ee"), ("@", "#8b93b8"), ("lab", "#f472b6"), (":", "#8b93b8"), ("~", "#8b7cff"), ("$ ", "#8b93b8")]

# ("cmd", text) or ("out", [(text, color), ...])
LINES = [
    ("cmd", "whoami"),
    ("out", [("→ ", "#8b7cff"), ("Software engineer who ships products end-to-end with AI agents", "#e2e6ff")]),
    ("gap", None),
    ("cmd", "cat now.md"),
    ("out", [("  ▸ ", "#22d3ee"), ("Fitness SaaS in production ", "#e2e6ff"), ("— .NET API, mobile apps, payments", "#8b93b8")]),
    ("out", [("  ▸ ", "#22d3ee"), ("Маяк ", "#e2e6ff"), ("— local-first Wi-Fi trust center on Rust + Tauri", "#8b93b8")]),
    ("out", [("  ▸ ", "#22d3ee"), ("Go ", "#e2e6ff"), ("— digging into game-server internals", "#8b93b8")]),
    ("out", [("  ▸ ", "#22d3ee"), ("Godot ", "#e2e6ff"), ("— an indie game for desktop & mobile", "#8b93b8")]),
    ("gap", None),
    ("cmd", "cat workflow.yml"),
    ("out", [("  pair_programmer: ", "#f472b6"), ("Claude Code + Codex", "#e2e6ff")]),
    ("out", [("  toolbox:         ", "#f472b6"), ("agents · MCP · skills · hooks", "#e2e6ff")]),
    ("out", [("  motto:           ", "#f472b6"), ('"ship it, measure it, make it better"', "#a3e635")]),
    ("gap", None),
    ("prompt", None),
]

H = TOP + LINE_H * len(LINES) + 26


def prompt_tspans():
    return "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in PROMPT)


prompt_len = sum(len(t) for t, _ in PROMPT)
body = []
defs = []
t = 0.6
y = TOP
for i, (kind, payload) in enumerate(LINES):
    if kind == "gap":
        y += LINE_H
        continue
    if kind == "cmd":
        cmd_x = LEFT + prompt_len * CHAR_W
        dur = max(len(payload) * TYPE_SPEED, 0.2)
        cid = f"c{i}"
        defs.append(
            f'<clipPath id="{cid}"><rect x="{cmd_x:.1f}" y="{y - FONT - 4}" height="{LINE_H}" width="0">'
            f'<animate attributeName="width" from="0" to="{len(payload) * CHAR_W + 2:.1f}" begin="{t + 0.25:.2f}s" dur="{dur:.2f}s" '
            f'calcMode="discrete" values="{";".join(f"{k * CHAR_W:.1f}" for k in range(len(payload) + 1))}" fill="freeze"/>'
            f"</rect></clipPath>"
        )
        body.append(
            f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur="0.01s" fill="freeze"/>'
            f'<text x="{LEFT}" y="{y}">{prompt_tspans()}</text>'
            f'<text x="{cmd_x:.1f}" y="{y}" fill="#ffffff" clip-path="url(#{cid})">{escape(payload)}</text></g>'
        )
        t += 0.25 + dur + PAUSE
    elif kind == "out":
        spans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in payload)
        body.append(
            f'<text x="{LEFT}" y="{y}" opacity="0" xml:space="preserve">{spans}'
            f'<animate attributeName="opacity" to="1" begin="{t:.2f}s" dur="0.25s" fill="freeze"/></text>'
        )
        t += 0.12
    elif kind == "prompt":
        body.append(
            f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{t:.2f}s" dur="0.01s" fill="freeze"/>'
            f'<text x="{LEFT}" y="{y}">{prompt_tspans()}</text>'
            f'<rect class="cursor" x="{LEFT + prompt_len * CHAR_W:.1f}" y="{y - FONT + 2}" width="{CHAR_W:.1f}" height="{FONT + 2}" fill="#22d3ee"/></g>'
        )
    y += LINE_H

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="whoami — about alxshmrv">
  <title>whoami — about alxshmrv</title>
  <defs>
    <linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0d1124"/>
      <stop offset="1" stop-color="#070a14"/>
    </linearGradient>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8b7cff"/>
      <stop offset="0.5" stop-color="#22d3ee"/>
      <stop offset="1" stop-color="#f472b6"/>
    </linearGradient>
    <filter id="shade" x="-10%" y="-10%" width="120%" height="130%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    {"".join(defs)}
    <style>
      text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: {FONT}px; white-space: pre; }}
      .cursor {{ animation: blink 1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0 }} }}
      .glow {{ animation: glow 6s ease-in-out infinite alternate; }}
      @keyframes glow {{ from {{ opacity: .25 }} to {{ opacity: .6 }} }}
    </style>
  </defs>
  <rect class="glow" x="30" y="24" width="{W - 60}" height="{H - 40}" rx="20" fill="url(#border)" filter="url(#shade)"/>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="url(#tbg)" stroke="url(#border)" stroke-opacity="0.6"/>
  <rect x="1" y="1" width="{W - 2}" height="38" rx="16" fill="#ffffff" fill-opacity="0.04"/>
  <circle cx="26" cy="20" r="6" fill="#ff5f57"/>
  <circle cx="46" cy="20" r="6" fill="#febc2e"/>
  <circle cx="66" cy="20" r="6" fill="#28c840"/>
  <text x="{W / 2}" y="25" text-anchor="middle" fill="#8b93b8" style="font-size:13px">alx@lab — zsh — {W // 10}×{len(LINES)}</text>
  {chr(10).join("  " + b for b in body)}
</svg>
"""

out = Path(__file__).resolve().parent.parent / "assets" / "terminal.svg"
out.write_text(svg, encoding="utf-8")
print(f"wrote {out} ({len(svg)} bytes, {t:.1f}s animation)")
