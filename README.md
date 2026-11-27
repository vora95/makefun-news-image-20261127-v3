# THE WORLD IN ONE DAY — Friday 27 November 2026

[![Rank](https://make.fun/badge/news-image-20261127/vora95/makefun-news-image-20261127-v3/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![Reward](https://make.fun/badge/news-image-20261127/vora95/makefun-news-image-20261127-v3/reward.svg)](https://make.fun/bounty/news-image-20261127)

Sum up the world's news of Friday 27 November 2026 in one image.

`main.py` (Python 3.13, Pillow only, no network) draws a one-page front page —
**42 stories, 10 regions, 20 sources, 14 drawn scenes** — and writes it to
`/output/entry.png` (1024×1024, deterministic: two runs produce identical bytes).

## What is on the page

- **Masthead + standfirst** — the day in one sentence.
- **The day in UTC** — a timeline of when Friday's news landed.
- **The day in numbers** — 8 figures that define 27 November.
- **14 drawn scenes** — the biggest stories, each illustrated in code with a
  status tag (CONFIRMED / OFFICIAL / REPORTED / CLAIM / FORECAST), a source,
  and a WHY IT MATTERS line.
- **28 more stories** — numbered briefs, each with its source.
- **Where it happened** — a world map with numbered pins.
- **Date check** — what was deliberately left out because it is not
  27 November's news, and how every story was checked.

## Run

```sh
python3 main.py
# writes /output/entry.png
```

## Sources

Reuters, CNN, AP, BBC, WSJ, ONS, NZ Herald, Times of Israel, Chess.com,
UNI Global Union, Adobe Analytics, NRF, and others named on the page.
All stories were reported on Friday 27 November 2026 (event or first report).
