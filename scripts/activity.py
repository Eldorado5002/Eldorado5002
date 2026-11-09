#!/usr/bin/env python3
"""Draws dist/activity.svg and dist/streak.svg from your GitHub contribution data."""
import json
import math
import os
import pathlib
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

TOKEN = os.environ["GITHUB_TOKEN"]
USER = os.environ["GH_USER"]
OUT = pathlib.Path("dist")
OUT.mkdir(exist_ok=True)

SANS = "'Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
CAL = "contributionCalendar{totalContributions weeks{contributionDays{date contributionCount weekday}}}"
Q_YEAR = "query($login:String!){user(login:$login){createdAt contributionsCollection{" + CAL + "}}}"
Q_RANGE = ("query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login)"
           "{contributionsCollection(from:$from,to:$to){" + CAL + "}}}")


def gql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "activity-cards"},
    )
    with urllib.request.urlopen(req) as resp:
        out = json.load(resp)
    if out.get("errors"):
        raise SystemExit(f"GitHub API error: {out['errors']}")
    return out["data"]["user"]


def md(d):
    return f"{d:%b} {d.day}"


def mdy(d):
    return f"{md(d)}, {d.year}"


def text(x, y, value, size=11, fill="#8B949E", weight=400, anchor="start", mono=False, spacing=0):
    family = f"font-family:{MONO};" if mono else ""
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" style="{family}font-size:{size}px;'
            f'font-weight:{weight};letter-spacing:{spacing}px;fill:{fill}">{value}</text>')


def panel(h):
    return (f'<rect width="680" height="{h}" rx="14" fill="#111418"/>'
            f'<rect x=".5" y=".5" width="679" height="{h - 1}" rx="14" fill="none" stroke="#262C34"/>')


# ---------- Data ----------

# Last 12 months, the same window as your profile calendar
me = gql(Q_YEAR, {"login": USER})
cal = me["contributionsCollection"]["contributionCalendar"]
cells = [(w, d["weekday"], d["contributionCount"], date.fromisoformat(d["date"]))
         for w, wk in enumerate(cal["weeks"]) for d in wk["contributionDays"]]

# Every day since the account was created, for totals, streaks and best month
now = datetime.now(timezone.utc)
today = now.date()
created = datetime.fromisoformat(me["createdAt"].replace("Z", "+00:00"))
days = {}
for year in range(created.year, now.year + 1):
    start = datetime(year, 1, 1, tzinfo=timezone.utc)
    end = min(datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc), now)
    c = gql(Q_RANGE, {"login": USER, "from": start.isoformat(), "to": end.isoformat()})
    for wk in c["contributionsCollection"]["contributionCalendar"]["weeks"]:
        for d in wk["contributionDays"]:
            days[date.fromisoformat(d["date"])] = d["contributionCount"]

total = sum(days.values())
active = sorted(d for d, n in days.items() if n > 0)
first = active[0] if active else today

best_len, best_start, best_end = 0, None, None
run, run_start, prev = 0, None, None
for d in sorted(days):
    if days[d] > 0:
        if prev is not None and run > 0 and d - prev == timedelta(days=1):
            run += 1
        else:
            run, run_start = 1, d
        if run > best_len:
            best_len, best_start, best_end = run, run_start, d
    else:
        run = 0
    prev = d

if not best_len:
    streak_span = "No streak yet"
elif best_end >= today - timedelta(days=1):
    streak_span = f"{md(best_start) if best_start.year == today.year else mdy(best_start)} – Present"
elif best_start.year == best_end.year:
    streak_span = f"{md(best_start)} – {mdy(best_end)}"
else:
    streak_span = f"{mdy(best_start)} – {mdy(best_end)}"

months = defaultdict(int)
for d, n in days.items():
    months[(d.year, d.month)] += n
(by, bm), best_month = max(months.items(), key=lambda kv: kv[1]) if months else ((today.year, today.month), 0)
best_month_label = f"{date(by, bm, 1):%B %Y}"

year_total = cal["totalContributions"]
year_days = len(cells)
year_active = sum(1 for c in cells if c[2] > 0)
busy = max(cells, key=lambda c: c[2])
range_label = f"{cells[0][3]:%b %Y} – {cells[-1][3]:%b %Y}"

# ---------- Activity card: 3D calendar that grows in once ----------

S, C, OX, OY = 8, 0.866, 160, 96
TOPS = ["#1E242C", "#5A4419", "#8A6820", "#C0912A", "#E9B949"]
LEFTS = ["#181D24", "#46350F", "#6C5118", "#977121", "#B88F35"]
RIGHTS = ["#14181E", "#3A2C0C", "#5A4314", "#7E5E1B", "#9A772B"]


def level(n):
    return 0 if n == 0 else 1 if n <= 2 else 2 if n <= 6 else 3 if n <= 14 else 4


def pts(a):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in a)


bars = []
for w, d, n, _ in sorted(cells, key=lambda c: (c[0] + c[1], c[0])):
    lv = level(n)
    h = 1.5 if n == 0 else min(4 + math.sqrt(n) * 4.2, 56)
    x, y = OX + (w - d) * S * C, OY + (w + d) * S * 0.5
    top = [(x, y - h), (x + S * C, y + S * .5 - h), (x, y + S - h), (x - S * C, y + S * .5 - h)]
    left = [(x - S * C, y + S * .5 - h), (x, y + S - h), (x, y + S), (x - S * C, y + S * .5)]
    right = [(x, y + S - h), (x + S * C, y + S * .5 - h), (x + S * C, y + S * .5), (x, y + S)]
    bars.append(f'<g class="b" style="animation-delay:{w * 0.05:.2f}s">'
                f'<polygon points="{pts(left)}" fill="{LEFTS[lv]}"/>'
                f'<polygon points="{pts(right)}" fill="{RIGHTS[lv]}"/>'
                f'<polygon points="{pts(top)}" fill="{TOPS[lv]}"/></g>')

max_sum = max(c[0] + c[1] for c in cells)
H = max(372, round(OY + max_sum * S * 0.5 + S + 36))
legend = "".join(f'<rect x="{54 + i * 14}" y="{H - 59}" width="10" height="10" rx="2" fill="{col}"/>'
                 for i, col in enumerate(TOPS))

ACTIVITY_CSS = (
    "<style>"
    ".b{transform-box:fill-box;transform-origin:50% 100%;"
    "animation:grow 1s cubic-bezier(.2,.7,.2,1) both}"
    "@keyframes grow{from{transform:scaleY(.05);opacity:0}to{transform:scaleY(1);opacity:1}}"
    ".f1{animation:up .8s ease-out .2s both}.f2{animation:up .8s ease-out .5s both}"
    "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
    "</style>"
)

activity = "".join([
    f'<svg xmlns="http://www.w3.org/2000/svg" width="680" height="{H}" viewBox="0 0 680 {H}" '
    f'role="img" style="font-family:{SANS}">',
    "<title>Contribution activity</title>",
    ACTIVITY_CSS,
    panel(H),
    text(24, 34, "ACTIVITY", fill="#E9B949", weight=600, mono=True, spacing=2),
    text(104, 34, "a year of commits, public + private"),
    '<g class="f1">',
    text(656, 86, f"{year_total:,}", size=28, fill="#E6EDF3", weight=700, anchor="end"),
    text(656, 106, "contributions in the last year", anchor="end"),
    text(656, 122, range_label, fill="#6E7681", anchor="end"),
    "</g>",
    "".join(bars),
    '<g class="f2">',
    text(24, H - 112, f"{year_active}", size=20, fill="#E6EDF3", weight=700),
    text(64, H - 112, f"active days of {year_days}"),
    text(24, H - 86, f"{busy[2]}", size=20, fill="#E6EDF3", weight=700),
    text(64, H - 86, f"busiest day · {md(busy[3])}"),
    text(24, H - 50, "less", fill="#6E7681"),
    legend,
    text(126, H - 50, "more", fill="#6E7681"),
    text(24, H - 24, "updated daily from GitHub", fill="#6E7681"),
    "</g>",
    "</svg>",
])

# ---------- Streak card: ring, glow and flame play once ----------

STREAK_CSS = (
    "<style>"
    ".c1{animation:up .8s ease-out both}.c2{animation:up .8s ease-out .3s both}"
    ".c3{animation:up .8s ease-out .6s both}"
    "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
    "#rg{stroke-dasharray:214;animation:ring 1.6s ease-out .4s both}"
    "@keyframes ring{from{stroke-dashoffset:214}to{stroke-dashoffset:0}}"
    "#gl{animation:gl 1.2s ease-out 1.9s both}"
    "@keyframes gl{0%{opacity:0}40%{opacity:.22}100%{opacity:0}}"
    "#fm{transform-box:fill-box;transform-origin:50% 100%;animation:fm 1.2s ease-out 1.9s both}"
    "@keyframes fm{0%{transform:scale(0);opacity:0}45%{transform:scale(1.25,1.35);opacity:1}"
    "70%{transform:scale(.95);opacity:1}100%{transform:scale(1);opacity:1}}"
    "</style>"
)

streak = "".join([
    f'<svg xmlns="http://www.w3.org/2000/svg" width="680" height="180" viewBox="0 0 680 180" '
    f'role="img" style="font-family:{SANS}">',
    "<title>Contribution streak</title>",
    STREAK_CSS,
    panel(180),
    text(24, 30, "STREAK", fill="#E9B949", weight=600, mono=True, spacing=2),
    '<path d="M230 56V156M450 56V156" stroke="#262C34"/>',
    '<g class="c1">',
    text(120, 100, f"{total:,}", size=24, fill="#E6EDF3", weight=700, anchor="middle"),
    text(120, 122, "Total contributions", size=12, fill="#C9D1D9", anchor="middle"),
    text(120, 140, f"{mdy(first)} – Present", fill="#6E7681", anchor="middle"),
    "</g>",
    '<circle cx="340" cy="94" r="34" fill="none" stroke="#2A3038" stroke-width="4"/>',
    '<circle id="gl" cx="340" cy="94" r="34" fill="none" stroke="#E9B949" stroke-width="12"/>',
    '<circle id="rg" cx="340" cy="94" r="34" fill="none" stroke="#E9B949" stroke-width="4" '
    'stroke-linecap="round" transform="rotate(-90 340 94)"/>',
    '<path id="fm" d="M340 52c4 5 7 8 7 12a7 7 0 0 1-14 0c0-3 2-5 3-7c1 3 2 4 4 4c0-3-1-6 0-9z" '
    'fill="#E8743B" stroke="#111418" stroke-width="2"/>',
    '<g class="c2">',
    text(340, 103, f"{best_len}", size=26, fill="#E9B949", weight=700, anchor="middle"),
    text(340, 146, "Longest streak · days", size=12, fill="#E9B949", weight=600, anchor="middle"),
    text(340, 164, streak_span, fill="#6E7681", anchor="middle"),
    "</g>",
    '<g class="c3">',
    text(560, 100, f"{best_month:,}", size=24, fill="#E6EDF3", weight=700, anchor="middle"),
    text(560, 122, "Best month", size=12, fill="#C9D1D9", anchor="middle"),
    text(560, 140, best_month_label, fill="#6E7681", anchor="middle"),
    "</g>",
    "</svg>",
])

(OUT / "activity.svg").write_text(activity, encoding="utf-8")
(OUT / "streak.svg").write_text(streak, encoding="utf-8")
print(f"Last year: {year_total} contributions, {year_active}/{year_days} active days")
print(f"All time: {total} contributions, longest streak {best_len} days, best month {best_month_label}")
