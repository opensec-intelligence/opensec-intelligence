"""Generate the OpenSec profile README SVGs. Text is embedded as paths so it
renders the same for every viewer (GitHub serves SVGs as images, no web fonts).

Usage: python scripts/gen.py [output-dir]   (default: assets/)"""

import math
import re
import sys
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "assets"
FONTS = HERE / "fonts"

GROTESK = TTFont(FONTS / "space-grotesk-latin-500-normal.woff")
GROTESK_400 = TTFont(FONTS / "space-grotesk-latin-400-normal.woff")
PIXEL = TTFont(FONTS / "DepartureMono-Regular.woff2")
MONO = TTFont(FONTS / "ibm-plex-mono-latin-500-normal.woff")


def text_path(font, text, size, x, y, tracking=0.0):
    """Return (svg path data, advance width) for text set at baseline (x, y).
    tracking is in em, like CSS letter-spacing."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    s = size / upem
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            name = cmap[ord("?")]
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[name].draw(tp)
        cx += gs[name].width * s + tracking * size
    width = cx - x - tracking * size
    return pen.getCommands(), width


def text_width(font, text, size, tracking=0.0):
    return text_path(font, text, size, 0, 0, tracking)[1]


def fmt(d):
    # Trim float noise to keep files small.
    return re.sub(r"(\d+\.\d)\d+", r"\1", d)


WORDMARK = (HERE / "opensec-wordmark.svg").read_text()
WM_GROUPS = re.findall(r'<g id="(opensec-[a-z0-9]+)"><path d="([^"]+)"', WORDMARK)
ACCENT_LETTERS = {"opensec-o", "opensec-s", "opensec-e2", "opensec-c"}

THEMES = {
    "dark": dict(
        bg="#050505",
        border="#ffffff1c",
        grid="#deebe0",
        grid_opacity="0.09",
        ink="#f1f3ef",
        muted="#969c97",
        faint="#ffffff26",
        accent="#bafc6b",
        accent_fill="#bafc6b",
        cell="#f1f3ef",
        cell_opacity=".34",
        trail="#bafc6b",
        glow=".45",
        gradient=False,
    ),
    "light": dict(
        bg="#f5f6f1",
        border="#0000001a",
        grid="#0b0c0b",
        grid_opacity="0.07",
        ink="#0b0c0b",
        muted="#5f655f",
        faint="#0b0c0b26",
        accent="#0a8f4a",
        accent_fill="url(#green)",
        cell="#0b0c0b",
        cell_opacity=".26",
        trail="#0ec75b",
        glow=".3",
        gradient=True,
    ),
}

GREEN_DEFS = """<linearGradient id="green" x1="0" y1="0" x2="1" y2="1" gradientUnits="objectBoundingBox">
<stop stop-color="#018b48"/><stop offset=".55" stop-color="#0ec75b"/><stop offset="1" stop-color="#00b956"/></linearGradient>"""

LAP = 9  # seconds per sweep lap, as on opensec.in/login
BUCKETS = 72

MOTION_CSS = f"""<style>
.orbit{{transform-origin:1010px 210px;animation:turn 16s linear infinite}}
.s{{opacity:0;animation:trail {LAP}s linear infinite}}
.k{{opacity:0;animation:lit {LAP}s linear infinite}}
.head{{transform-origin:1010px 210px;animation:turn {LAP}s linear infinite}}
@keyframes turn{{to{{transform:rotate(360deg)}}}}
@keyframes trail{{0%{{opacity:1}}6%{{opacity:.8}}15%{{opacity:.5}}28%{{opacity:.25}}45%{{opacity:.08}}62%,100%{{opacity:0}}}}
@keyframes lit{{0%,5.9%{{opacity:.8}}6%,100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.orbit,.head,.s,.k{{animation-play-state:paused}}}}
</style>"""


def coverage(x, y):
    # The official O on a 100-unit plate, as the login matrix rebuilds it:
    # four quarters (r 26-42), two of them split into an outer (35-42) and an
    # inner (26-32.5) band, each 1.5 units clear of the centre lines.
    if abs(x) < 1.5 or abs(y) < 1.5:
        return 0
    r = math.hypot(x, y)
    if r < 26 or r > 42:
        return 0
    split = (x > 0 and y > 0) or (x < 0 and y < 0)
    if not split:
        return 1
    return 1 if r >= 35 or r <= 32.5 else 0


def pixel_cells(pitch):
    cells = []
    span = math.ceil(43 / pitch)
    for j in range(-span, span + 1):
        for i in range(-span, span + 1):
            hit = sum(
                coverage((i - 0.5 + (sx + 0.5) / 4) * pitch, (j - 0.5 + (sy + 0.5) / 4) * pitch)
                for sy in range(4)
                for sx in range(4)
            )
            if hit < 3:
                continue
            hx, hy = i * pitch, j * pitch
            turn = (math.atan2(hx, -hy) / (2 * math.pi) + 1) % 1
            cells.append((hx, hy, hit / 16, turn))
    return cells


def pixel_mark(t, cx, cy, radius):
    """The login page's matrix O: dim cells with a clockwise trail of colour
    sweeping round once every LAP seconds, and a ticked bezel whose tick
    under the sweep head lights."""
    unit = radius / 42
    pitch = 2.2
    base = ""
    lit = [""] * BUCKETS
    for hx, hy, c, turn in pixel_cells(pitch):
        side = pitch * unit * 0.66 * math.sqrt(c)
        x, y = cx + hx * unit - side / 2, cy + hy * unit - side / 2
        rect = f"M{x:.1f} {y:.1f}h{side:.1f}v{side:.1f}h-{side:.1f}z"
        base += rect
        lit[min(BUCKETS - 1, int(turn * BUCKETS))] += rect
    # A soft glow that rides with the sweep head, under the cells.
    gr = 22 * unit
    out = [
        f'<radialGradient id="glow"><stop stop-color="{t["trail"]}" stop-opacity="{t["glow"]}"/>'
        f'<stop offset="1" stop-color="{t["trail"]}" stop-opacity="0"/></radialGradient>',
        f'<g class="head"><circle cx="{cx}" cy="{cy - 34 * unit:.1f}" r="{gr:.1f}" fill="url(#glow)"/></g>',
        f'<path d="{base}" fill="{t["cell"]}" opacity="{t["cell_opacity"]}"/>',
    ]
    r0 = 47 * unit
    quiet = ""
    ticks = []
    for i in range(BUCKETS):
        a = i / BUCKETS * 2 * math.pi - math.pi / 2
        r1 = r0 + (7 if i % 9 == 0 else 3.5) * unit * 0.6
        seg = (
            f"M{cx + math.cos(a) * r0:.1f} {cy + math.sin(a) * r0:.1f}"
            f"L{cx + math.cos(a) * r1:.1f} {cy + math.sin(a) * r1:.1f}"
        )
        quiet += seg
        ticks.append(seg)
    out.append(f'<path d="{quiet}" stroke="{t["cell"]}" stroke-opacity=".16"/>')
    for i in range(BUCKETS):
        # Bucket i lights when the head reaches its turn: delay = -(1 - turn) laps.
        delay = -(1 - (i + 0.5) / BUCKETS) * LAP
        style = f'style="animation-delay:{delay:.3f}s"'
        if lit[i]:
            out.append(f'<path class="s" {style} d="{lit[i]}" fill="{t["trail"]}"/>')
        out.append(f'<path class="k" {style} d="{ticks[i]}" stroke="{t["trail"]}"/>')
    return "\n".join(out)


def wordmark(t, x, y, height):
    s = height / 326
    parts = []
    for gid, d in WM_GROUPS:
        fill = t["accent_fill"] if gid in ACCENT_LETTERS else t["ink"]
        parts.append(f'<path d="{d}" fill="{fill}" fill-rule="evenodd"/>')
    return f'<g transform="translate({x} {y}) scale({s:.5f})">{"".join(parts)}</g>'


def banner(theme):
    t = THEMES[theme]
    W, H = 1280, 420
    cx, cy = 1010, 210
    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-labelledby="t">'
    )
    out.append("<title id=\"t\">OpenSec. From vulnerability to visibility.</title>")
    out.append("<defs>")
    if t["gradient"]:
        out.append(GREEN_DEFS)
    out.append(
        f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="{t["grid"]}" stroke-width="1"/></pattern>'
    )
    out.append(
        f'<radialGradient id="fade" cx="{cx}" cy="{cy}" r="560" gradientUnits="userSpaceOnUse">'
        '<stop stop-color="#fff"/><stop offset=".55" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    )
    out.append('<mask id="gridmask"><rect width="100%" height="100%" fill="url(#fade)"/></mask>')
    out.append(f'<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    out.append("</defs>")
    out.append(MOTION_CSS)
    out.append('<g clip-path="url(#card)">')
    out.append(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    out.append(
        f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="{t["grid_opacity"]}" mask="url(#gridmask)"/>'
    )

    # Instrument rings around the mark.
    out.append(f'<circle cx="{cx}" cy="{cy}" r="176" stroke="{t["faint"]}" stroke-width="1"/>')
    ticks = []
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        x1, y1 = cx + dx * 166, cy + dy * 166
        x2, y2 = cx + dx * 186, cy + dy * 186
        ticks.append(f"M{x1} {y1}L{x2} {y2}")
    out.append(f'<path d="{"".join(ticks)}" stroke="{t["accent"]}" stroke-width="2"/>')
    out.append(
        f'<g class="orbit"><circle cx="{cx}" cy="{cy - 176}" r="4" fill="{t["accent"]}"/></g>'
    )
    out.append(pixel_mark(t, cx, cy, 120))

    # Left column.
    x0 = 72
    out.append(wordmark(t, x0, 52, 38))

    size = 70
    track = -0.05
    d, _ = text_path(GROTESK, "From vulnerability", size, x0 - 3, 198, track)
    out.append(f'<path d="{fmt(d)}" fill="{t["ink"]}"/>')
    d, w = text_path(GROTESK, "to ", size, x0 - 3, 274, track)
    out.append(f'<path d="{fmt(d)}" fill="{t["ink"]}"/>')
    d, _ = text_path(PIXEL, "visibility.", size * 1.1, x0 - 3 + w + size * 0.02, 274, -0.02)
    out.append(f'<path d="{fmt(d)}" fill="{t["accent_fill"]}"/>')

    d, _ = text_path(GROTESK, "AI-native vulnerability management.", 19, x0, 320, -0.01)
    out.append(f'<path d="{fmt(d)}" fill="{t["accent"]}"/>')
    d, _ = text_path(
        GROTESK_400, "Security research, open-source tooling and Pi-Bolt.", 19, x0, 348, -0.01
    )
    out.append(f'<path d="{fmt(d)}" fill="{t["muted"]}"/>')

    cap = "// 150+ CVES DISCOVERED   // 100+ OPEN-SOURCE REPOSITORIES"
    d, _ = text_path(MONO, cap, 14, x0, 390, 0.04)
    out.append(f'<path d="{fmt(d)}" fill="{t["muted"]}"/>')

    out.append("</g>")
    out.append(
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" stroke="{t["border"]}"/>'
    )
    out.append("</svg>")
    return "\n".join(out)


BOLT_LOGO = (
    '<polygon fill="#F7C04A" points="540,100 220,460 390,460"/>'
    '<polygon fill="#E9A42C" points="540,100 390,460 430,320"/>'
    '<polygon fill="#4C96EA" points="430,320 390,460 300,700"/>'
    '<polygon fill="#2A78D6" points="430,320 300,700 600,320"/>'
)


def pibolt_card(theme):
    t = THEMES[theme]
    W, H = 1280, 350
    panel = "#0c0c0c" if theme == "dark" else "#ffffff"
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none" role="img" aria-labelledby="t">',
        '<title id="t">Pi-Bolt: Pi, the coding agent, compiled ahead of time to one native executable. '
        "10x sooner ready to type, 120x faster writing a 400 KB file, 4.5x less memory than Pi on Node 24.</title>",
        "<defs>",
    ]
    if t["gradient"]:
        out.append(GREEN_DEFS)
    out.append(
        f'<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" stroke="{t["grid"]}" stroke-width="1"/></pattern>'
        '<linearGradient id="fade" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>'
        '<mask id="gridmask"><rect width="100%" height="100%" fill="url(#fade)"/></mask>'
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>'
        "</defs>"
    )
    out.append('<g clip-path="url(#card)">')
    out.append(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    out.append(
        f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity="{t["grid_opacity"]}" mask="url(#gridmask)"/>'
    )

    x0 = 72
    d, _ = text_path(MONO, "// FLAGSHIP   OPEN SOURCE   MIT", 14, x0, 78, 0.04)
    out.append(f'<path d="{fmt(d)}" fill="{t["muted"]}"/>')
    out.append(f'<g transform="translate({x0 - 10} 98) scale(0.085)">{BOLT_LOGO}</g>')
    d, _ = text_path(GROTESK, "Pi-Bolt", 60, x0 + 62, 152, -0.05)
    out.append(f'<path d="{fmt(d)}" fill="{t["ink"]}"/>')
    for i, line in enumerate(
        ("Pi, the coding agent, compiled ahead of time", "to one native executable. No Node.js, no JIT.")
    ):
        d, _ = text_path(GROTESK_400, line, 21, x0, 200 + i * 30, -0.01)
        out.append(f'<path d="{fmt(d)}" fill="{t["muted"]}"/>')

    # Install command.
    out.append(
        f'<rect x="{x0}" y="262" width="508" height="52" rx="10" fill="{panel}" stroke="{t["faint"]}"/>'
    )
    d, w = text_path(MONO, "$ ", 16, x0 + 20, 294, 0)
    out.append(f'<path d="{fmt(d)}" fill="{t["accent"]}"/>')
    d, _ = text_path(MONO, "curl -fsSL pi-bolt.opensec.in/install.sh | sh", 16, x0 + 20 + w, 294, -0.01)
    out.append(f'<path d="{fmt(d)}" fill="{t["ink"]}"/>')

    # Benchmarks.
    stats = (
        ("10×", "sooner ready", "to type"),
        ("120×", "faster writing", "a 400 KB file"),
        ("4.5×", "less memory", "after 40 prompts"),
    )
    sx, col = 690, 186
    for i, (num, l1, l2) in enumerate(stats):
        x = sx + i * col
        if i:
            out.append(f'<path d="M{x - 24} 96V262" stroke="{t["faint"]}"/>')
        d, _ = text_path(MONO, f"// 0{i + 1}", 13, x, 110, 0.04)
        out.append(f'<path d="{fmt(d)}" fill="{t["muted"]}"/>')
        d, _ = text_path(PIXEL, num, 58, x - 2, 190, -0.03)
        out.append(f'<path d="{fmt(d)}" fill="{t["accent_fill"]}"/>')
        for j, line in enumerate((l1, l2)):
            d, _ = text_path(GROTESK_400, line, 17, x, 228 + j * 24, -0.01)
            out.append(f'<path d="{fmt(d)}" fill="{t["ink"] if j == 0 else t["muted"]}"/>')
    d, _ = text_path(MONO, "PI-BOLT 1.0.0 VS PI 1.4.0 ON NODE 24, LINUX X86-64", 12, sx, 300, 0.04)
    out.append(f'<path d="{fmt(d)}" fill="{t["muted"]}"/>')

    out.append("</g>")
    out.append(
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="17.5" stroke="{t["border"]}"/>'
    )
    out.append("</svg>")
    return "\n".join(out)


for theme in THEMES:
    (OUT / f"banner-{theme}.svg").write_text(banner(theme))
    (OUT / f"pi-bolt-{theme}.svg").write_text(pibolt_card(theme))
print("ok")
