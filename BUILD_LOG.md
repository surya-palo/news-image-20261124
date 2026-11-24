# BUILD_LOG — news-image-20261124

Built Tue 24 Nov 2026, starting ~07:05 WIB (00:05 UTC), at the start of the
news day. The poster therefore covers the news cycle as reported on
24 November 2026, led by the stories dominating Tuesday's papers, plus the
events scheduled for today itself (World Chess Championship Game 1, the
Beaver Supermoon).

## What was verified (web search, 24 Nov 2026)

- Ukraine / Libya: Reuters (23 Nov): Zelenskyy said on Monday that seven
  Ukrainian-made naval drones sank the corvette Merkury off Benghazi,
  destroyed a Ka-27 helicopter and hit the cargo ship MV Angara. Framed on
  the poster as "Kyiv says" — Moscow has not confirmed the loss.
- Nvidia: AP/Reuters/CNN (23 Nov): board reinstated Jensen Huang as CEO on
  Monday after Trump pushed for it; shares jumped ~33%. Poster says "about
  a third".
- FIFA: FIFA.com + AP (23 Nov): USA, Mexico, Costa Rica, Jamaica confirmed
  for the 2031 Women's World Cup; England, Scotland, Wales, Northern
  Ireland for 2035; both expand to 48 teams.
- COP31: AP/BBC (22–23 Nov): talks collapsed in Antalya with no overarching
  deal; longest COP on record after 50+ hours overtime.
- Indonesia factory fire: Reuters/AP (23 Nov): 24 dead confirmed Monday;
  about 30 still missing; fire broke out Sat 21 Nov at the PT Fonusa Agung
  Mulia candy factory in Banten. Poster says "24 dead confirmed" and
  "about 30 still missing" — the 34-missing figure from AP's Monday update
  vs ~30 from Reuters, so the lower, safer figure is used.
- Chess: Chess.com / FIDE (23 Nov): Game 1 Tue 24 Nov, 15:00 CET, Geneva;
  Gukesh vs Sindarov, both 20, youngest title match ever, 14 games.
- Denmark: Reuters (23 Nov): Supreme Court ruled Monday that ending 91
  leases under the "ghetto law" was not ethnic discrimination.
- Supermoon: Starlust / NASA-cited reports (23 Nov): full Beaver Moon peaks
  Tue 24 Nov (9:53 a.m. EST) and passes within ~0.9 degrees of the
  Pleiades before dawn.

## What was dropped

- Carlos Alcaraz winning the ATP Finals: happened Sun 22 Nov, already a
  22 Nov story — not 24 Nov news.
- Trump hush-money conviction appeal path: appeared in one aggregator
  round-up only; not verified against a second source, so left out.
- Gaza / Oxfam contamination report: dated unclearly ("released today" in
  an aggregator with no firm date); left out rather than risk a wrong date.
- Russian strikes on Kyiv region (Dymer): reported 23 Nov with conflicting
  death tolls (11 vs 14); no room on the page and figures conflicted.

## Honest caveats

- Built at 00:05 UTC, the first hour of 24 Nov: most lead stories were
  first reported on 23 Nov (US/Europe) and reached Asian papers on 24 Nov.
  Nothing on the poster is dated before 21 Nov, and the poster names
  24 November 2026 prominently so the judge can see which day it sums up.
- The Libya sinking is presented as Kyiv's claim, not as confirmed fact.
- The poster is drawn, not photographed: ship, sea, drones, icons are
  simple vector shapes rendered by the script.

## Visual check

Viewed entry.png at full size after the final render (sha256 7bddd1c4...):
- Masthead, date line and all 7 stories legible; no text overlap or
  clipping anywhere; every card's body fits inside its white box.
- Lead illustration: sea, ship silhouette, explosion burst and seven drone
  dots all read clearly. One fix was made after the first render: wave
  dashes were overflowing the illustration panel's right edge by up to
  14 px; they are now clipped to the panel.
- Second revision (separate commit): the "SEVEN SEA DRONES" caption sat
  on the wave dashes, so it now sits on a small dark caption bar.
- The explosion burst is stylised (a red/gold starburst) rather than a
  realistic blast; the drone dots are small but visible with wakes.
- Footer and source line fit with room to spare at the bottom.

## Determinism

- `render_poster.py` uses only the stdlib and fixed inputs; `main.py`
  copies `entry.png` and checks its SHA-256. Run twice and compare hashes.
