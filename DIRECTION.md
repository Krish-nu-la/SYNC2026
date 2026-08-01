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

### 2.1 Palette — "wet asphalt at night"

Base is tinted ink, never pure black. The risk ramp is IMD's, adjusted for legibility
on dark.

| Role | Value | Note |
|---|---|---|
| Base | `#0A0F16` | blue-tinted ink, not `#000` |
| Surface | `#121B24` | panels floating on the map |
| Hairline | `#1E2A36` | borders, grid |
| **Safe** | `#3FB6AD` | cyan-teal — water-calm |
| **Watch** | `#E5B23C` | IMD yellow, warmed |
| **Alert** | `#EF7A29` | IMD orange |
| **Warning** | `#E03A38` | IMD red — **the only fully saturated colour in the app** |
| Text | `#E4EDF4` | muted: `#7A8B99` |
| **Human** | `#A78BFA` | violet — see below |

**The rule that carries the thesis:** everything the AI produces uses the risk ramp.
Everything a human does — the citizen's dropped pin, the dispatcher's acknowledgement —
uses violet, deliberately *outside* the ramp. Two visual systems coexisting on one
screen. The Human × AI argument becomes legible before anyone reads a word of it.

**Declared deviation:** safe is cyan, not IMD's literal green. Green on a dark map reads
"go" and fights the basemap. Label it "Safe / No warning" so the mapping to IMD stays
explicit and honest.

**Saturation discipline:** red appears rarely. Most zones sit quiet most of the time.
When red arrives it has to mean something.

### 2.2 Type

- **Archivo** — wordmark and section headers. Institutional, signage-like; reads as
  infrastructure, not as a startup.
- **IBM Plex Sans** — all UI. Designed for technical and operational contexts.
- **IBM Plex Mono** — every number. Tabular by default, so digits don't jitter as the
  scrubber animates values. Non-negotiable given how much our numbers move.
- **IBM Plex Sans Malayalam** — same superfamily, so zone names can render bilingually
  (`Kaloor / കലൂർ`) in matching type.

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

---

## 4. OPEN QUESTION — not decided, do not implement

**Tide state.** Kochi's canals back up **at high tide** — a real, cited driver of
waterlogging, and the TP Canal's documented overflow behaviour depends on it. Modelling
it would be physically honest and is something no competing team is likely to have.

**Why it's parked:** it would change the shared data contract, and the contract is the
seam between frontend and backend. Sent to the backend teammate for a decision first.

Until that comes back: **`getFloodRisk()` is unchanged.** No tide field, no tide UI, no
speculative stubs.

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
