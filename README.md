# The World in One Day — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/surya-palo/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/surya-palo/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper-style poster that sums up the world news of **Tuesday 24 November 2026**
in one 1024x1024 image: one lead story plus six news cards and an "also today" strip.

## The day's news

- **Lead — War at sea:** Kyiv says seven sea drones sank the Russian corvette
  *Merkury* off Libya, destroying a Ka-27 helicopter and hitting the cargo ship
  *MV Angara*.
- **Tech:** Nvidia's board reinstates Jensen Huang as CEO after President Trump
  pushed for his return; shares jumped about a third.
- **Sport:** FIFA confirms the USA, Mexico, Costa Rica and Jamaica as 2031
  Women's World Cup hosts, and the four UK nations for 2035.
- **Climate:** COP31 ends in Antalya with no deal — the longest COP on record.
- **Asia:** 24 dead confirmed after the candy factory fire near Jakarta; about
  30 workers still missing.
- **Sport:** World Chess Championship Game 1 in Geneva — Gukesh vs Sindarov,
  the youngest title match ever.
- **Europe:** Denmark's top court backs the "ghetto law" evictions.
- **Also today:** the Beaver Supermoon peaks and passes the Pleiades.

Every fact was checked against reporting from Reuters, AP, BBC, FIFA and
FIDE before it went on the page; see `BUILD_LOG.md` for what was verified
and what was dropped.

## How it is built

`render_poster.py` draws the poster with the Python standard library only:
a hand-built 5x7 bitmap font, a pixel buffer, and a minimal PNG encoder
(`zlib` + `struct`). No network, no system fonts, no third-party packages,
so the render is byte-for-byte deterministic.

`main.py` (stdlib only) copies `entry.png` to `/output/entry.png` and
verifies its SHA-256.

```sh
python3 render_poster.py   # rebuild entry.png
python3 main.py            # copy to /output/entry.png, verify hash
```

## Files

- `entry.png` — the poster (1024x1024, under 1 MiB)
- `render_poster.py` — the renderer
- `main.py` — the entry point
- `BUILD_LOG.md` — honest build notes
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
