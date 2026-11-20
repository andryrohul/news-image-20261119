# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/andryrohul/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/andryrohul/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page that sums up Thursday 19 November 2026 in 25 stories from 6 regions: the first-ever Trump–Xi–Putin trilateral in Shenzhen, the World Court's 9–6 genocide ruling on Myanmar, GTA VI's release after 13 years, and Anthropic's record $81.3bn IPO, plus a day-by-hours strip, a world map, a verdict box and a date check that keeps pre-Thursday stories off the page. Every figure was checked against reporting from Reuters, AP, CNN, Yonhap, the ABS and the ICJ.

## Run it

```sh
python3 main.py
```

That regenerates `entry.png` (1024×1024, under 1 MB) with Pillow, deterministically — two runs produce the same file.

## What is on the page

- **Masthead** — "Thursday 19 November 2026" with the day's three biggest stories as the red subhead.
- **Stats row** — 3 presidents, $81.3bn, 13 years, 730,000+ Rohingya, 204,070 listed to evacuate in Odisha, 551,864 exam candidates, 4.9% Australian jobless, 48 hours left at COP31.
- **The day by hours** — Auckland 00:00 to New York 09:30, local time.
- **3 lead stories** with drawn illustrations: the Shenzhen summit table, Vice City at dusk, and Anthropic's Nasdaq candlesticks.
- **12 mini-cards (4–15)** — Myanmar, COP31, Cyclone Akvan, the Crimean Bridge, Gaza, Riyadh, Florida, Suneung, Paris, Jakarta, Bogotá and Canberra, each tagged REPORTED, CLAIM or FORECAST.
- **Bottom band** — a "Where it happened" map, "Also on this page" briefs, the ICJ verdict, a "How sure are we?" legend and markets.
- **Date check** — stories in the headlines that day but not Thursday's news, excluded on purpose (Anthropic's $83 pricing was Wednesday, for example).

## Notes

- The program draws everything with Pillow shapes and DejaVu fonts; no network and no external images.
- `main.py` must be run from this directory; it writes `entry.png` next to itself.

---

<sub>Entered on [make.fun](https://make.fun/?ref=w6sgzd0k&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
