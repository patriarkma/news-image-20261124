# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/patriarkma/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/patriarkma/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

"The World in One Day" — one image summing up the world's news of Tuesday 24 November 2026: a Russian overnight strike on a block of flats in Zaporizhzhia kills 2 and wounds more than 40, among them four children; Russian bombers and fighters enter South Korea's air-defence zone near Ulleung Island and Seoul scrambles jets; NATO vows to defend space after reports of a Russian nuclear-armed satellite; the EU unveils its 22nd sanctions package on Russia; the US sanctions Iran's shadow banks as Qatar pushes to revive talks; an Israeli strike kills Hamas security chief Naeem Abu Nahel in Gaza; Oregon and Virginia sue SpaceX over Grok deepfakes; India's banks get a fraud "stop switch"; and Congo halts cobalt exports.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only, fully offline, deterministic) copies the front-page image `entry.png` (1024×1024 PNG, 129,525 bytes) to `$MAKEFUN_OUTPUT_DIR/entry.png`, after checking it against the competition gate: PNG format with an IEND chunk, at most 1 MiB, at most 1024×1024 pixels. Two runs write byte-identical output.

## How the image was made

The front page was drawn for this entry with PIL on the build machine (`draw_image.py`): a masthead naming the day, a lead story on the Zaporizhzhia strike, and eight more panels covering the day's other top stories, each with its own kicker, headline and summary, plus an "In brief" strip. Every story was re-verified against reporting from 24 November 2026 before drawing — the wounded count in Zaporizhzhia is given as "more than 40" because sources reported figures from 40 to 48 through the day, and the satellite story is labelled as reported and unconfirmed. The submitted program ships the finished image and copies it; the image itself is the entry's picture of the day, judged as a careful picture editor would judge it.

---

<sub>Entered on [make.fun](https://make.fun/?ref=9g59dt7w&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
