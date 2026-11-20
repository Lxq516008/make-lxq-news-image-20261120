# make-lxq-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Lxq516008/make-lxq-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Lxq516008/make-lxq-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One image summing up the world's news of Friday 20 November 2026: a newspaper
front page, drawn by a program, with seven stories from that day — Kyiv's
bridges hit in an overnight missile barrage, Houthi claims against Saudi
targets, a UK–EU youth mobility deal, US sanctions on two crime networks,
a Tokyo protest, California's Nvidia probe, and the COP31 fossil-fuel row.

`generate_image.py` (Python + Pillow, DejaVu fonts) draws the page with flat
shapes and text — no photographs, no borrowed artwork. `main.ts` copies the
finished `entry.png` to the output directory. See `NEWS.md` for every story
and its sources.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=a0pz932n&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
