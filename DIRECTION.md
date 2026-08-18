# DIRECTION.md — JalNetra visual & product direction

**Status:** accepted 2026-08-01. Items 1–9 in §3 are locked. Item in §4 is an open
question, not a decision.

**Scope:** this file owns *direction* — the reasoning behind the look, the layout, and
the signature interaction. `CLAUDE.md` owns the app spec and the data contract.
impeccable's `DESIGN.md` owns the final token values; what follows is the brief that
feeds it, not a competing palette.

**For the backend teammate:** §4 is the only thing here that touches your side. Nothing
in §1–3 changes `getFloodRisk()`.

---

## 0. Positioning, in one sentence

India's Meteorological Department already issues four-level colour-coded warnings —
Green / Yellow / Orange / Red — and calls a sub-24-hour forecast a **nowcast**.
JalNetra implements that exact official warning language at **street resolution**
instead of district resolution.

We are not inventing a risk vocabulary. We are implementing the national one, finer.

---

## 1. Research findings this direction rests on

Each of these earned a specific decision downstream; they are not decoration.

| Source | What we took |
|---|---|
| **IMD colour-coded warnings** — Green=No warning, Yellow=Watch, Orange=Alert, Red=Warning; "nowcast" = sub-24h forecast | The four-level ladder and its wording. Our contract's `safe\|watch\|high\|severe` *is* this ladder. |
| **Thevara–Perandoor (TP) Canal** — Kochi Corporation's main drainage artery: Panampilly Nagar → Kadavanthra → KSRTC → Kaloor → Perandoor Kayal. Silted, encroached, overflows at high tide. **Mullassery Canal has a reverse slope**, pushing water back into the TP Canal. | The canal layer. Our hotspots are strung along a real, named, failing drainage line — that's *why* they flood. |
| **Operation Breakthrough** — Kerala Irrigation Dept's anti-flooding project, phase four | Local vocabulary for dispatcher context. |
| **FAA / ATC display research** — red reserved for collision alert; **the alert blinks until the controller acknowledges it**; colour used strategically, never decoratively | The acknowledge mechanic. Unacknowledged severe pulses; acknowledgement stops it. An operational state made visible, not an animation added for delight. |
| **GOV.UK "Check for flooding"** — four severities written as *what + what-to-do* pairs; timestamped status; imperative language | Two-line legend and popup copy. Never a bare risk number. And a home for `generatedAt`. |
| **Google Flood Hub** — renders inundation extent *and depth* over real tiles, down to village scale | Depth in cm is the headline number; the 0–1 risk score is secondary. |
| **NOAA National Water Model / NWS FIM viewer** — layers named "Latest Analysis" vs "5-Day Max Forecast"; observed and predicted never blurred | Visual separation of observed "Now" from forecast +30…+120. |
| **Map UI Patterns — timeline slider** — tick marks, snapping, and *don't hide* filtered features; drop them to low opacity so context survives | Scrubber behaviour. |
| **Hackathon judging writeups** — "AI is table stakes, not a differentiator"; judges have seen a hundred GPT wrappers | Human-in-the-loop promoted from item 6 of 7 to near-top billing. |

---

## 2. The design

### 2.1 Palette — "backwater at night" / "whitewash by day"

Base is tinted ink, never pure black or pure white. The risk ramp is IMD's.

**Amended 2026-08-01 by an accepted intensity pass** (same hues, pushed chroma).

**Rebuilt 2026-08-19.** Two changes, and the second one is the reason for the first.

**(a) The palette is now Kerala-grounded.** The previous base / safe / human hues
were blue-black, cyan-teal and violet — which is, precisely, the default palette of
Linear, Vercel, Framer and most of the AI-hackathon field. It said nothing about
Kochi. The replacements are drawn from the place the forecast is actually about:
still backwater at night, monsoon dark, and the brass of old Kerala fittings and
signage. Every dark neutral is generated on **one** axis (CIE Lab hue 130,
backwater-olive) and every light neutral on Lab hue 95 (whitewash warm), so no
value is a leftover blue-grey.

**(b) There is now a light theme.** Not an inversion — each state colour was
re-derived against the light ground and re-measured, because inverting dark-mode
values onto whitewash puts mid-tones where they have no contrast.

**The palette's LOGIC is unchanged:** the IMD ladder is reserved for AI-produced
risk values, exactly one hue outside the ladder is reserved for human action, and
saturation stays scarce so Warning red still means something.

#### Dark — "backwater at night"

| Role | Value | Was | Note |
|---|---|---|---|
| Base | `#0C0F08` | `#080D14` | green-black. Wet ground and monsoon dark, not a sci-fi console's blue ink |
| Surface | `#1B1E19` | `#101A24` | panels floating on the map |
| Surface-2 | `#232720` | `#16232F` | recessed rows |
| Hairline | `#30342C` | `#22323F` | borders; `#41463D` for the stronger tier |
| **Safe** | `#73A07E` | `#17E0CC` | still canal water at night — murky, olive-toned, deliberately not a bright UI teal |
| **Watch** | `#FFC93C` | *unchanged* | IMD yellow |
| **Alert** | `#FF7A1A` | *unchanged* | IMD orange |
| **Warning** | `#FF2E4D` | *unchanged* | IMD red — still the only fully saturated colour |
| Text | `#EDF2E9` | `#EAF2F8` | muted: `#9BA394` |
| **Human** | `#A18853` | `#B26BFF` | aged temple brass — unpolished and olive-leaning on purpose; that is what pushes it clear of IMD yellow |
| Canal | `#497665` | `#2E8CA6` | backwater channel, a shade below the safe green so it reads *beneath* the zones |

#### Light — "old whitewash"

| Role | Value | Note |
|---|---|---|
| Base | `#F7F3EB` | limewashed Kerala house wall — warm render, never clinical SaaS white |
| Surface | `#FFFEFA` | panels sit *above* the ground here, so they lift rather than recede |
| Surface-2 | `#EEEBE1` | recessed rows |
| Hairline | `#D7D4C9` | `#B8B6AA` for the stronger tier |
| **Safe** | `#386B47` | the same backwater green taken to daylight depth, not lightened |
| **Watch / Alert / Warning (fill)** | `#FFC93C` / `#FF7A1A` / `#FF2E4D` | **identical to dark.** A map fill, a legend swatch or a zone bar is the colour IMD publishes, in both themes |
| **Watch / Alert / Warning (ink)** | `#906900` / `#8C3902` / `#7D2A2D` | the same IMD hues at reading weight. `#FFC93C` as small text on whitewash is 1.4:1 and simply unreadable |
| Text | `#292D25` | muted: `#666A5C` |
| **Human** | `#82693E` | the same brass at daylight depth, hue held near the dark value so the human system reads as one colour across both themes |
| Canal | `#2F7D74` | |

**On the ladder inks.** Light mode keeps IMD's *hues* and, critically, IMD's
*lightness order* — Watch lightest, Warning darkest. An earlier attempt flattened all
three to roughly one lightness for contrast, which collapsed their separation under
deuteranopia to ΔE 2.0. Preserving the ramp brings it back to 9.4, which is better
than the dark theme's own 8.6.

**The rule that carries the thesis** is untouched in substance: everything the AI
produces uses the risk ramp; everything a human does — the citizen's dropped pin, the
dispatcher's acknowledgement — uses brass, deliberately outside the ramp. Only the
hue changed, from a generic violet to one that belongs to the place.

**Declared deviation, revised.** Safe was cyan on the argument that green reads "go"
and fights a dark basemap. That argument is now overridden deliberately: the green in
question is not a signal green but the actual desaturated olive of Kochi's canals, and
it is labelled "Safe / No warning" wherever it appears, so the mapping to IMD stays
explicit. The original concern is answered by chroma, not by changing hue family.

**Saturation discipline:** unchanged. Red appears rarely.

#### Measured, not eyeballed

All values below are computed — WCAG 2.1 relative luminance, CIEDE2000 for
distinctness, and Viénot–Brettel–Mollon dichromat simulation. Deuteranopia and
protanopia are the ones that matter here because gold/orange/red is the highest-risk
confusion zone.

- **Contrast.** Every state colour clears AA (4.5:1) as text on its own theme's panel
  surface, in both themes. Tightest: dark Warning 4.61, dark Brass 4.94, light Watch
  ink 4.95.
- **Brass vs Watch — the hard constraint.** Dark ΔE 23.0 under both CVD types, against
  a ladder whose own worst internal pair is 8.6. Light ΔE 8.7, against a ladder
  internal 9.4.
- **The honest weak spot.** Brass vs *Warning* in dark mode is ΔE 7.2 under
  deuteranopia — marginally below the ladder's own Alert/Warning separation of 8.6.
  This is not a tuning failure: dichromacy collapses the entire warm range, and
  Warning red lands inside it. No brass escapes it. It is handled structurally rather
  than chromatically — brass appears only as **fills, 2px borders and pins**, the
  ladder only as **text labels and map fills**, and PRODUCT.md's rule that risk level
  always carries its word means the level is never conveyed by colour alone.
- **Hero card.** Its 52px state word takes the ladder *ink* so it stays legible on
  whitewash; its 1px edge and glow take the *published* IMD colour, because an edge is
  a mark rather than type. That split is also what keeps the hero's border clearly
  distinct from the citizen card's brass border in light mode (ΔE 28–35 rather than 9).

### 2.2 Type

- **Archivo** — wordmark and section headers. Institutional, signage-like; reads as
  infrastructure, not as a startup.
- **IBM Plex Sans** — all UI. Designed for technical and operational contexts.
- **IBM Plex Mono** — every number. Tabular by default, so digits don't jitter as the
  scrubber animates values. Non-negotiable given how much our numbers move.
- **Noto Sans Malayalam** — for bilingual zone names (`Kaloor / കലൂർ`).
  **Corrected 2026-08-01:** this originally specified *IBM Plex Sans Malayalam*,
  which **does not exist** — Google Fonts returns HTTP 400 for it. Malayalam text
  was silently falling back to an arbitrary system font. Noto Sans Malayalam is
  the systematic, neutral substitute and is the right register for Operate.

### 2.3 Layout — console, not page

Full-bleed map as substrate. Panels float *on* it with real edges. **No nested cards.**

```
┌──────────────────────────────────────────────────────────┐
│ JALNETRA   Nowcast issued 10:04 IST · valid to 12:04     │  status strip
├────────────┬───────────────────────────────┬─────────────┤
│ RAINFALL   │                               │ ZONES ↓risk │
│ scenario   │        KOCHI  (map)           │ ─────────── │
│ ──────○──  │     canal layer beneath       │ alert feed  │
│            │                               │             │
├────────────┴───────────────────────────────┴─────────────┤
│  NOW ──── +30 ──── +60 ──── +90 ──── +120     [▶ RUN]    │  the hero
└──────────────────────────────────────────────────────────┘
```

The scrubber gets full width along the bottom — the most horizontal real estate on
screen, because it's what we want people looking at.

**Mobile:** map on top, controls collapse to a bottom sheet, scrubber pinned above it.

### 2.4 The ONE signature moment — "the two-hour sweep"

A single **RUN** control sweeps 0 → 120 min over ~6 seconds. During the sweep:

1. A thin light-line travels the scrubber track; the head moves on custom easing.
2. Zones don't just recolour — **they fill.** Fill height and opacity interpolate
   continuously. Water rising, not a palette swap. Colour crosses IMD thresholds as it
   goes.
3. As each zone crosses into Alert or Warning, an entry **drops into the feed**,
   staggered 30–80 ms, and the zone emits **one** pulse ring — then stops. Pulsing
   continues only on *unacknowledged severe*.
4. Counters count up in tabular mono — population at risk, worst zone, depth. Zero
   layout shift.
5. It settles: *"+120 min · 4 zones in Warning · 61,200 people at risk."*

Six seconds, one gesture, static map → story, every number traceable to the contract.

**Craft constraints (pre-empting emil-design-eng):**
- **Transitions, not keyframes** — dragging retargets rather than restarts.
- The sweep stays **interruptible**; grabbing the scrubber mid-run takes over immediately.
- UI chrome < 300 ms. The sweep itself is longer because it's *content*, not chrome.
- `prefers-reduced-motion` → values snap, opacity only, no movement, no pulse.

**Second-read moment:** the canal line. First glance, a subtle stroke beneath the zones.
Second glance — every flooding zone is strung along it.

### 2.5 SECOND signature moment — the zone diorama

**Accepted 2026-08-01.** Opening a zone's popup offers a **street-level view**: a
full-screen Three.js scene of that zone with water risen to its predicted
`depthCm` at the current rainfall and horizon.

**This is stylized and illustrative. It is NOT literal 3D terrain, and that
distinction must not be lost later.** The street, the building silhouettes, and
the figure are abstractions with exactly one job: giving the depth number a
human scale. Nothing in the scene is surveyed, and no elevation data exists
behind it. The on-screen label says so, and so does the code comment above the
module.

- The figure is **1.72 m tall** and is the scale reference the whole scene
  exists for. 41 cm of water reading as mid-shin on a person is the point.
- Water colour is the zone's IMD level colour, so the diorama and the map agree.
- Rain density is driven by the rainfall control, tying the scene to the console.
- Depth is labelled in cm on screen and is the contract's `depthCm` — the
  provenance principle applies here exactly as it does on the map.
- Layout per zone is **deterministic** (seeded from the zone id), so a zone looks
  the same every time. Demos stay repeatable.
- **Three.js r128, vendored at `vendor/three.r128.min.js`** — no network at
  runtime. r128 has no `CapsuleGeometry`; the figure is cylinders and a sphere.

**It reads `depthCm` and adds no fields to the data contract.**

---

## 3. Accepted changes to the spec (1–9, locked)

1. **Adopt IMD wording in the UI.** Contract ids stay frozen (`safe|watch|high|severe`);
   display "No warning / Watch / Alert / Warning." Add GOV.UK-style consequence lines
   under each.
2. **Safe becomes cool cyan, not green.** Only severe gets full saturation.
3. **Reserve violet for human actions** — outside the risk ramp entirely.
4. **Add the canal layer** — TP Canal + Mullassery Canal. Consider adding
   **Kadavanthra** to the zone list; it sits directly on the TP Canal and is currently
   missing from `CLAUDE.md`.
5. **Depth becomes the hero number**; the 0–1 risk index is secondary.
6. **Distinguish observed from forecast.** "Now" is observed; +30…+120 are predicted.
   Different border treatment.
7. **Surface `generatedAt`** as "Nowcast issued HH:MM IST · valid to HH:MM."
8. **Scrubber gains** a play control, keyboard ← →, tick marks, snapping, and
   low-opacity (not hidden) inactive states.
9. **Promote human-in-the-loop.** Currently item 6 of 7 in the `CLAUDE.md` component
   list; it should sit near the top. If AI is table stakes, the human layer is the
   differentiator and deserves proportional screen weight.

None of these change `getFloodRisk()`.

### Accepted 2026-08-01 — intensity pass and diorama (10–13)

10. **Full-bleed map with a floating HUD**, replacing the even three-column grid.
    Rails are deliberately unequal (244 px left, 356 px right) and the scrubber
    floats between them. This is not new invention — §2.3 above already specified
    "full-bleed map as substrate, panels float on it with real edges"; the first
    build quietly opted out of it.
11. **Saturation raised across the risk ramp and the human violet** (§2.1 table).
    Statement type for the hero numbers — city risk index at 52 px, popup depth
    at 44 px, diorama depth at 92 px, Archivo 800/900.
12. **Legend moved out of the map overlay** into a collapsible left-rail
    disclosure, collapsed by default. Data provenance sits beside it in the same
    pattern.
13. **The zone diorama** (§2.5) as the second signature moment.

**Rejected during the same pass:** a perspective-raked grid overlay on the map.
The mechanical detector flagged it, and the reasoning holds — a tinted grid over
real geography on a public-safety console reads as if it *means* something, and
it measures nothing. A false measurement affordance is worse than a flat map.
The depth cue is now atmospheric falloff only (`.map-grade`), which does the same
job of pushing the edges back without inventing a coordinate system.

---

### Accepted 2026-08-01 — calibration, transition, and two new surfaces (14–19)

14. **Depth bands widened to 10 / 25 / 50 cm** (from 5 / 15 / 30), anchored to
    what water does to a street. At the default Heavy scenario the worst zone
    now peaks at 41 cm / risk 0.55 with **zero** Warning zones; Cloudburst
    brings **three** zones over. Red kept scarce, and 92/120 mm/hr now have
    somewhere worse to go.
    *Consequence to tell the backend: `CLAUDE.md`'s worked example still
    produces `depthCm: 41` exactly, but that depth now classifies as Alert
    rather than severe.*
15. **`risk` rescaled to `depth / 75`** so band edges land on 0.13 / 0.33 /
    0.66. "risk ≥ 0.66 means Warning" is now true by construction instead of
    being a second scale that disagreed with the depth bands.
16. **Susceptibilities respread** (0.95 → 0.22, same ranking, same high/med/low
    grouping from `CLAUDE.md`). The originals clustered five zones at
    0.85–0.92, which no exponent could separate — the city either went entirely
    red or entirely dry.
17. **"Now" carries antecedent water.** The accumulation curve started at 7% of
    saturation, i.e. it assumed rain began the instant you pressed play. A
    nowcast issued during a cloudburst must show water already on the street.
18. **Diorama palette rebuilt on five distinct hue families** — indigo sky,
    cool slate buildings, *warm* asphalt road, warm concrete pavement, vivid
    level-coloured water, violet figure. The earlier version was five shades of
    one blue and read as black. Buildings gained varied footprints, setbacks,
    low-rise rhythm and plinths; the figure was rebuilt at ~7.5-head
    proportions with shoulders, arms and neck; lampposts were moved onto the
    kerb line.
19. **Map → street-level transition.** Map scales toward the zone while a
    blackout veil fades up (400 ms), the swap happens at full black, then the
    diorama fades in as the camera eases forward (320 + 620 ms). Water is
    already at depth on arrival — the answer, not a filling tank. Exit reverses
    in ~500 ms, faster than entry. Total under the 1200 ms ceiling.

### Surfaces beyond the console

- **`login.html`** — demo gate. Performs **no authentication**; any input opens
  the console, and the page says so on screen. Split layout: the product's
  argument on the left, the gate on the right.
- **`admin.html`** — zone configuration and model status. Deliberately separate
  from the console: a dispatcher mid-event must not be able to change a
  susceptibility by accident. Writes to `localStorage`; the console reads the
  same key.
- **`vendor/tokens.css`** — the palette and type tokens now live in one file
  linked by all three pages, so they cannot drift.

### Final layout — accepted 2026-08-01

Implements the Figma frame **"JalNetra Console Clean"** (file
`6cnkPwwW9utcjgPTwmuJkP`, node `1:4`, 1440×900). Measurements were read from
the file, not estimated:

| Region | Figma node | Size | Position |
|---|---|---|---|
| Hero · Action | `1:5` | 812 × **135** | 16, 16 |
| Citizen · Reports | `1:9` | 472 × **95** | 16, 165 |
| Map · Kochi | `1:13` | **1000** × 280 | 16, 255 |
| Scrubber · Timeline | `1:15` | 1000 × **60** | 16, 840 |
| Right Rail | `1:17` | **320** × 900 | 1100, 0 |

Built as a CSS grid — `1fr + 320px`, 16px gaps, status strip spanning both
columns — rather than absolute positioning, so it survives other viewports.

**Top to bottom:**

1. **Status strip**, 56px. JALNETRA wordmark, nowcast issued/valid, Simulated
   chip, offline indicator, three stats (deepest depth, population in Warning
   zones, risk index), and Admin / Sign out navigation.
2. **Hero action card**, 135px. `#101A24` ground, 1px border in the *current
   level colour* (yellow at Watch), 24px sides / 16px top-bottom. The state
   word is **52px Archivo Black** — Figma's text node measured 57px tall.
   Below it, the action line at 14px with a bold `Bring:` prefix.
3. **Citizen reports**, 472px wide, 95px tall. `#101A24` with a 2px violet
   border. Title 12px Archivo uppercase in violet, counts by zone, and the
   report control.
4. **Rainfall scenario**, ~512px, in the slot beside the citizen card. Slider
   plus six presets: Dry / Drizzle / Moderate / Heavy / Very heavy / Cloudburst.
5. **Map**, 1000px wide, filling the remaining height. **No depth badges on the
   map** — permanent badges collided wherever zones sit close together, so depth
   lives in the rail list. The citizen report control floats bottom-left over it.
6. **Scrubber**, 60px, full width of the content column. Horizon readout,
   observed/forecast marker, track with five stops, RUN control, and Legend /
   Sources disclosures.
7. **Right rail**, 320px. Zones by depth and Alert feed *only*, as two
   independently scrolling panes so a 13-row zone list can never push the feed
   off the bottom.

**Three deviations from the Figma frame, all so the console stays operable:**

- **The frame contains no rainfall control.** Without one the scenario can never
  change and the hero can never escalate — the core interaction. It takes the
  ~512px slot the frame leaves empty beside the 472px citizen card, which is
  what explains that card being narrower than the 812px hero.
- **The frame leaves 305px empty** between the map bottom (y=535) and the
  scrubber (y=840). The map fills it.
- **The frame has no status strip.** The wordmark, offline badge, stats and
  navigation were all accepted earlier and are kept.

One further departure: the hero runs the full 1000px rather than the frame's
812px. At 812 it leaves a 188px void beside it, which reads as unfinished.

## 4. OPEN QUESTION — not decided, do not implement

**Tide state.** Kochi's canals back up **at high tide** — a real, cited driver of
waterlogging, and the TP Canal's documented overflow behaviour depends on it. Modelling
it would be physically honest and is something no competing team is likely to have.

**Why it's parked:** it would change the shared data contract, and the contract is the
seam between frontend and backend. Sent to the backend teammate for a decision first.

Until that comes back: **`getFloodRisk()` is unchanged.** No tide field, no tide UI, no
speculative stubs.

---

## 4b. Where `depthCm` actually comes from — and why it is not the ML model alone

**Decision: depth is physics-led. `hydrology_service` produces it; the trained model
`flood_model.pkl` is applied on top as a bounded correction.** This is a deliberate
choice made after measuring the model, and it is stated here so it can be said out loud
rather than discovered.

### What we measured

The backend ships a real trained artefact — an `XGBRegressor` fitted on
`flood_risk_dataset_india.csv`, a **district-level, all-India** flood dataset. Fed the
Kochi zone table, it behaves like this:

| Probe | Result |
|---|---|
| Output at **0 mm/hr** | **6.6 – 6.8 cm** of standing water in zero rain |
| Output at **120 mm/hr** (cloudburst) | 13.5 – 13.9 cm — never reaches Alert (25 cm) |
| **Spread across all zones** | **0.4 cm**, end to end |
| Response to `elevation_m` | **flat at every value** |
| Response to `terrain_risk` | flat above 0 — every Kochi zone lands on the same side of every split |
| Response to `historical_floods`, `infrastructure` | flat above 0 |
| **Absolute ceiling**, searched over a deliberately out-of-distribution grid | **46.4 cm** — and only at 600 mm/hr rainfall and a 10 m water level |

`terrain_risk` is the single feature carrying susceptibility, drainage capacity and
terrain factor. Because every zone falls on one side of its splits, **the model has no
mechanism to distinguish Kaloor from Thevara.** The 0.4 cm of spread it does produce
comes from latitude, longitude and population density — not hydrology. And its ceiling
sits *below* the 50 cm Warning threshold, so no input at any value can make it issue a
Warning.

It is not a Kochi street-depth model, and asking it to be one would misrepresent it.

### What we did instead

`hydrology_service` computes a water balance per zone per horizon: rainfall accumulates
over `ANTECEDENT_HOURS + offset`, a runoff coefficient (susceptibility × terrain × land
cover) decides what becomes surface water, soil saturation removes the ground's capacity
to absorb, drainage carries some away at an efficiency degraded by canal backup and
saturation, and whatever is left ponds — deeper on low ground. Every term is driven by a
real column in `zones.csv`.

The model then runs on the **same time-evolved state** and applies a bounded
multiplicative correction, normalised on a log scale across its measured envelope
(5.99 – 37.20 cm) into ±`ML_CORRECTION` (25%).

### What the model is actually worth

Measured over 1,434 samples (16 zones × rainfall × 5 offsets, rainfall > 0):

- correction applied ranges **×0.788 – ×1.250**
- **mean absolute influence: 9.9%** of final depth
- largest single-zone shift: **+12.73 cm**

Worked example — Kaloor, cloudburst, +120 min: physics alone gives **55.32 cm**, the
model's own raw output is **39.78 cm** (an Alert it can never escalate past), and the
correction of ×1.250 produces the final **69.15 cm**. Remove the model and every number
on screen changes.

**Division of labour, stated plainly:** the physics decides *which zone floods first*;
the model decides *how hard the city escalates* as the catchment loads up. Neither
number is the other's decoration.

### Recalibrated 2026-08-19 — `ANTECEDENT_HOURS` 0.75 → 1.75 h

**`ANTECEDENT_HOURS` is now 1.75 h, and `DEPTH_GAIN` 1.03, recalibrated so the
physics engine's resting position matches item 17's stated intent.** At 0.75 h,
"Now" read 4.8 cm at Heavy and 13.1 cm at Cloudburst — a street with essentially
nothing on it, which is the "rain begins the instant you pressed play" behaviour
item 17 exists to reject. It now reads **11.4 cm (Watch)** at Heavy and
**28.0 cm (Alert)** at Cloudburst.

`DEPTH_GAIN` moved only as the counterweight, and only because the antecedent
constant could not do the job alone: raising it lifts the whole curve, tail
included, and at 1.75 h with the old gain Cloudburst +120 put **13 of 16 zones**
into Warning instead of three — the "city goes entirely red or entirely dry"
failure item 16 describes, and a breach of §2.1's saturation discipline. Scaling
the gain back restores item 14's calibration exactly: **Heavy +120 still has zero
Warning zones** (Kaloor 30.6 cm) and **Cloudburst +120 still has three** (Kaloor
69.2, Vyttila 59.7, Perandoor 50.1). Dry still reads 0 cm at every horizon.

The worked example above is the post-recalibration one; the model's measured
influence is unchanged in kind (correction now spans ×0.821 – ×1.250).

### One data change this forced

`zones.csv` shipped with `susceptibility` rating **Thevara 0.93 above Kaloor 0.88** — a
coastal-elevation heuristic. That contradicts CLAUDE.md's zone table and the reporting it
rests on, which name **Kalamassery, Kaloor and Edappally** as Kochi's worst-hit
waterlogging zones. The `susceptibility` column was replaced with the frontend's
documented, reporting-grounded values and `drain_capacity` re-derived to stay consistent
with it. `elevation`, `terrain_factor`, `canal_distance_km`, `land_cover` and `soil_type`
are the backend's originals, untouched.

---

## 5. Quality floor (inherited from CLAUDE.md, restated because it's non-negotiable)

Responsive to mobile · visible keyboard focus · `prefers-reduced-motion` respected ·
deterministic mock so demos never surprise us · every number on screen traceable to the
contract.

---

## Sources

- [IMD Colour-Coded Warnings — Drishti IAS](https://www.drishtiias.com/daily-updates/daily-news-analysis/imd-colour-coded-warnings)
- [IMD District-Wise Nowcast Warnings](https://mausam.imd.gov.in/responsive/districtWiseNowcastGIS.php)
- [Flood Mitigation Kochi — Kerala Irrigation Dept (PDF)](https://irrigation.kerala.gov.in/sites/default/files/2021-08/kochiflood.pdf)
- [Despite frequent flooding risk, Kochi still lacks drainage master plan — The News Minute](https://www.thenewsminute.com/kerala/despite-frequent-flooding-risk-kochi-still-lacks-drainage-master-plan-166481)
- [Colour Usability on Air Traffic Control Displays](https://www.researchgate.net/publication/253111803_Color_Usability_on_Air_Traffic_Control_Displays)
- [A Standardized Color Palette for Terminal Situation Displays (DOT)](https://rosap.ntl.bts.gov/view/dot/71713/dot_71713_DS1.pdf)
- [Check for flooding — GOV.UK](https://check-for-flooding.service.gov.uk/)
- [Flood alerts and warnings — GOV.UK](https://check-for-flooding.service.gov.uk/alerts-and-warnings)
- [Expanding our ML-based flood forecasting — Google](https://blog.google/innovation-and-ai/products/expanding-our-ml-based-flood-forecasting/)
- [About the National Water Model — NOAA](https://water.noaa.gov/about/nwm)
- [NWS FIM Viewer Instructions (PDF)](https://www.weather.gov/media/owp/operations/nws_fim_viewer_instructions.pdf)
- [Timeline slider — Map UI Patterns](https://mapuipatterns.com/timeline-slider/)
- [Color map design for visualization in flood risk assessment — IJGIS](https://www.tandfonline.com/doi/full/10.1080/13658816.2017.1349318)
- [Hackathon judging: 6 criteria to pick winning projects — TAIKAI](https://taikai.network/en/blog/hackathon-judging)
- [Public Alert System — KSDMA](https://sdma.kerala.gov.in/public-alert-system/)
