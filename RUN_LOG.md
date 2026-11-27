# RUN_LOG — news-image-20261127 v2 push (target 99.30%)

## Goal
- User order 27 Nov 07:49 WIB: "tembusin top 3 semua wallet". Parent update 07:55: target **99.30%**, not just beating #3 (98.39%).
- v1 "THE WORLD TODAY" (sub 01a21a65): dev 97.5354% (11W-1D-0L), implied rank ~#66/518. Cutoff #20 97.8638%, #3 98.5809%, #1 98.8562% (live LB fetch 27 Nov ~07:52 WIB).
- Competition: news-image-20261127, $100, top 50 paid, closes 29 Nov 07:00 WIB. Quota can_submit TRUE (day left 4, hard left 38).

## Hypothesis (BOUNTY_MASTER_SKILL §3)
- Judge (z-ai/glm-5.3-flash, pairwise) rewards: explicit date, breadth across
  regions/beats, internal consistency, legibility, sourcing. Punishes: undated
  stories, speculative/old stories, inconsistency. Evidence: judge reasons in
  v1's matches + top-3 images inspected 27 Nov ~07:52 WIB.
- v1 gaps vs top: no drawn scenes, no numbers strip, no UTC timeline, no
  status tags, no per-story sources, no DATE CHECK, 33 stories vs 36-40 top.
- v2 beats top1 on every dimension at once: 42 stories, 14 drawn scenes,
  8-number strip, UTC timeline, status tag + source + WHY IT MATTERS per lead,
  numbered briefs with sources, numbered map, DATE CHECK box — plus better
  accuracy (top1 wrongly schedules Gukesh Game 4 "today"; Game 4 is Sat 28 Nov,
  today is a rest day — verified via Chess.com/ChessBase).

## Facts verified via web search (27 Nov ~07:52-07:55 WIB)
- Kuwait: 2 Italian Rheinmetall Italia technicians (Antonio Saccoccio 65,
  Emanuele Lo Russo 36) killed Thu 26 Nov by Iranian drones at air-defence
  station; Iran denies; 4 wounded initially. Reuters/CNN/WSJ.
- Jazan: Houthi projectile hit Aramco Jazan refinery Thu 26 Nov, Nepalese
  worker killed, several hurt, some ops halted; day after Ras Tanura claim;
  coalition destroyed Hodeidah launch platform; Brent ~$95-96.57. Reuters/CNN.
- Gaza: Israeli strikes killed 10 Thu 26 Nov incl. Khaled Abu Nada (Hamas
  deputy education minister) + wife in Deir al-Balah; Hamas chief al-Hayya
  weighing response; 3rd straight night of strikes despite year-old ceasefire.
- Bangkok: Bangchak Phra Khanong refinery blast Thu 26 Nov ~14:45 local,
  9 hurt (3-4 critical), all units shut, 120,000 bpd. CNN/Reuters/AP.
- NZ: final official count due TODAY 27 Nov (noon AEDT); preliminary coalition
  67/131 seats, ~400,000 special votes uncounted; opposition 57. CNN.
- UK: ONS 26 Nov — net migration 77,000 yr to Jun 2026 (from 204,000),
  lowest since 1997 ex-pandemic. Reuters/Times.
- Storm: Thanksgiving storm, 900,000+ without power (Times); 100th Macy's
  parade postponed to Sat 28 Nov 08:30 ET — decision announced Wed 25 Nov;
  1,700+ flights delayed, 417 cancelled. Reuters/WSJ.
- Black Friday: Adobe FORECAST $12.9B online (+9.2%); NRF 126M shoppers.
- Bears-Lions 39-35: Williams to Odunze 6-yd TD with 3 seconds left; Bears
  9-2, six straight wins; Gibbs 205 yds, 3 TDs. Reuters/AP.
- Gukesh-Sindarov Game 3: 60-move draw, 1.5-1.5; Rio de Janeiro Variation;
  Sindarov made move 40 with 6 seconds to spare; TODAY is rest day, Game 4
  Sat 28 Nov. Chess.com/ChessBase.
- Depardieu: Paris appeals court Thu 26 Nov — trial for alleged rape of
  Charlotte Arnould (7 Aug 2018); 2nd charge dismissed; faces 15-20 yrs.
- China tariffs: USTR proposed Wed 25 Nov Section 301 duties on 14 economies
  (China +20%, total 45% some goods); China replied Thu 26 Nov via He Yadong:
  "reserves the right to take necessary measures". EU 15%, Indonesia 18%.
- Ibiza: Malta-flagged tanker Med Emre capsized ~25-30 nm off Ibiza early
  Thu, up to 7,000t diesel, 17 crew rescued, 1 died in hospital, no
  pollution so far. Reuters.
- Trump GDP: BEA revised Q3 growth 3.4% -> 4.3% Wed 25 Nov; Trump Thu 26 Nov
  demanded probe, called pre-election numbers "fake". Reuters/AP.
- Sinner: AO officials confirmed Thu 26 Nov — out of AO 2027 (Jan 17) after
  right-knee surgery; hasn't played since Wimbledon July; lost No.1 to Zverev.
- Mecca alliance: Pakistan, Saudi, Turkey FMs meet Islamabad Fri-Sat 27-28
  Nov on mutual defence pact signed in Mecca in August. Reuters.
- Musk: two SpaceX shares for every US child (~$18B), announced Wed 25 Nov
  (one from SpaceX, one from Musk personally; via Trump Accounts). Reuters.
- Karachi: six-storey under-construction building collapsed Wed 25 Nov,
  3 killed, 14 injured, Baloch Colony. Dawn/Rescue 1122.
- N. Korea: GUR (Ukraine intel) Thu 26 Nov — Pyongyang temporarily halted
  KN-23 missile + artillery shipments to Russia after spat over Seoul.
  Reuters notes it could not independently verify.
- Amazon: Make Amazon Pay strikes/protests in 20+ countries Fri 27 Nov;
  ver.di strikes at 11 German sites. UNI Global/Engadget.

## Design (v2, "THE WORLD IN ONE DAY")
- 1024x1024, cream paper, Liberation Serif/Sans bundled in fonts/ (OFL,
  deterministic across environments).
- Sections: kicker / masthead / standfirst / UTC timeline / numbers strip /
  3 lead scenes / 5 scene cards / 6 scene cards (= 14 scenes) / 28 numbered
  briefs (2 cols) / map + DATE CHECK / footer with sources + method legend.
- Status tags: CONFIRMED (2+ outlets) / OFFICIAL (on the record) /
  REPORTED (one outlet) / CLAIM (one side says) / FORECAST (scheduled today).
- Total: 14 scene stories + 28 briefs = 42 stories, 10 regions, 20 sources.

## Build log
- 27 Nov ~07:56 WIB: repo vora95/makefun-news-image-20261127-v3 created
  (id 1473825938); homepage = bounty URL; topics makefun/ai-agents/bounties;
  bootstrapped via Contents API.
- 27 Nov ~07:56 WIB: local git init (vora95 <vior24942@gmail.com>); fonts
  bundled; LICENSE (MIT + SPDX), owner.json (wallet 5goa...), README, .gitignore.
- main.py v1 (own message): full program; render FAILED with TypeError
  (float x in range() inside scene_gaza) + layout budget over by ~25px.
- main.py v2 (separate message): int() casts in card functions; all 14
  scenes rewritten h-aware (lead 52px, row2 44px, row3 38px); bodies
  shortened to guarantee 2 lines; timeline labels shortened; advances
  184/132/140. Render OK: 2 runs byte-identical, 233,460 B.
- main.py v3 (separate message): visual polish after viewing renders —
  Kuwait skyline + 2nd burst; Jazan bigger flames + glow; Ibiza bigger hull
  + waves; map PIN_OFFSETS to declutter Middle East/South Asia pins.
  Render OK: 2 runs byte-identical, sha256
  a4e41c0166d61af1599d8f967243b59970aa073587c6807167077a8214a43ff1,
  234,286 B, 1024x1024.
- Verified by viewing the render (full + 3 zoom crops): all 42 stories,
  timeline, numbers, tags, sources, map pins, DATE CHECK, footer legible;
  glyphs -> (arrow) and 1/2 render correctly in Liberation fonts.
- [commit sha + badge checks to be added after git push]
