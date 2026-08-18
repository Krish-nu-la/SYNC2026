# JalNetra — street-level flood nowcasting for Kochi

**JalNetra** ("water-eye") forecasts *street-level* flood risk across Kochi, Kerala for
the next two hours, from rainfall + terrain + drainage. It renders the forecast on a live
map and — the part that matters — lets a human act on it.

Built for **SYNC 2026 — Human × AI Hackathon**.

---

## The thesis: the forecast is AI, the action is human

India's Meteorological Department issues flood warnings **by district**. That is the
right resolution for a state government and the wrong one for a person deciding whether
to move their family upstairs. JalNetra issues warnings **by zone, for the next 120
minutes**, and then puts a person in the loop before anything happens:

- **AI flags the risk** — a physics-led hydrology model, corrected by a trained
  gradient-boosted regressor, predicts standing-water depth per zone per horizon.
- **A citizen reports ground truth** — "Report waterlogging here" drops a pin and nudges
  nearby zone risk. The model is not the only witness.
- **A human acts** — every alert carries a "Seen — I'm acting on this" control. The
  forecast's job is to end in an instruction; a number without one is an unfinished
  thought.

Every screen states its own provenance. What is real is labelled real, what is estimated
is labelled `est.`, and what is simulated says **Simulated** in the status strip.

---

## Running it

Two processes: a Python backend and any static file server for the frontend.

### 1. Backend (FastAPI + the trained model)

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn app.main:app --port 8000
```

Must be run **from `backend/`** — model, zone and log paths are relative to it.
On Apple Silicon, `xgboost` needs OpenMP: `brew install libomp`.

Check it: <http://127.0.0.1:8000/health> · interactive docs at `/docs`.

### 2. Frontend (no build step)

```bash
python3 -m http.server 8080
```

Open <http://127.0.0.1:8080/login.html>.

**The frontend does not require the backend.** If the API is unreachable, times out, or
errors, the console falls back to a deterministic in-browser simulation and says so in
the status strip. A backend that dies mid-demo degrades to a working console, never a
blank one.

---

## The seam

One function connects the two halves. It is the only point of contact:

```js
async function getFloodRisk(rainfallMmHr, timeOffsetMin)  // index.html
```

It reads `GET /forecast?rain=` — which returns **all five offsets in one response**, with
a 300 s server-side cache — and serves the requested frame from it. Full contract,
field by field, in [`docs/BACKEND_HANDOFF.md`](docs/BACKEND_HANDOFF.md).

### Endpoints

| Route | Returns |
|---|---|
| `GET /forecast?rain=` | all 5 offsets — what the console uses |
| `GET /nowcast?rain=&offset=` | one horizon, contract shape |
| `GET /dashboard?rain=` | deepest zone, risk index, population affected |
| `GET /alerts?rain=` | ranked alerts above the safe threshold |
| `GET /analytics?rain=` | depth distribution and zone counts |
| `GET /explain?zone=&rain=&offset=` | why this zone, in words |
| `GET`/`POST /reports` | citizen reports (SQLite) |
| `GET /health` | liveness + model state |

---

## How depth is computed

**Physics-led, ML-corrected.** `hydrology_service` runs a water balance per zone per
horizon — rainfall accumulates, a runoff coefficient decides what becomes surface water,
soil saturation removes the ground's absorption, drainage carries some away at an
efficiency degraded by canal backup, and what remains ponds, deeper on low ground. The
trained model then runs on the same time-evolved state and applies a bounded correction
(±25%, mean realised influence **9.9%**).

**Why not the model alone, stated plainly:** `flood_model.pkl` was trained on
district-level all-India flood data. Measured against Kochi's zone table it separates all
16 zones by **0.4 cm** end to end, is **flat in `elevation_m`**, reports **6.8 cm of
standing water in zero rain**, and **tops out near 46 cm against a 50 cm Warning
threshold**. It cannot resolve street-level variation within one city, and it cannot
issue a Warning at any input. What it genuinely knows is how sharply a catchment
escalates as rain accumulates — so that is the job it is given.

The physics decides *which zone floods first*; the model decides *how hard the city
escalates*. Full measurements in [`DIRECTION.md`](DIRECTION.md) §4b.

Warning bands follow IMD's four-level scale and are anchored to what water does to a
street: **10 cm** Watch, **25 cm** Alert (most cars stall near 30), **50 cm** Warning
(genuinely impassable).

---

## Tech

**Frontend** — single-file `index.html`, vanilla JS/CSS, no build step, everything
vendored. Chosen for stage reliability: no CDN in the critical path. Leaflet + CartoDB
dark tiles for the map, three.js for the street-level diorama. Archivo + IBM Plex
Sans/Mono + Noto Sans Malayalam, self-hosted.

**Backend** — FastAPI, XGBoost + scikit-learn, pandas, SQLAlchemy over SQLite.

**Quality floor** — responsive to mobile, visible keyboard focus, `prefers-reduced-motion`
respected, deterministic fallback so demos never surprise us, and every number on screen
traceable to the contract.

---

## Credits

| | |
|---|---|
| **Frontend, UI/UX, design system, integration** | [Ravishankar Varier](https://github.com/raaaviiiii) |
| **Backend, hydrology services, ML model** | [Krishnu](https://github.com/Krish-nu-la) — [SYNC---JALNETRA-](https://github.com/Krish-nu-la/SYNC---JALNETRA-) |

Zone list, coordinates and the TP/Mullassery canal failure modes come from reporting on
actual Kochi waterlogging and Kerala Irrigation Department material. Population figures
are estimates, labelled `est.` wherever they appear. There is no live rainfall feed —
rainfall is a scenario slider, and the console says so.

Sources in [`docs/REFERENCES.md`](docs/REFERENCES.md).
