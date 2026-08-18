SAFE = "safe"
WATCH = "watch"
HIGH = "high"
SEVERE = "severe"

LEVELS = [
    SAFE,
    WATCH,
    HIGH,
    SEVERE
]

SAFE_LIMIT = 10
WATCH_LIMIT = 25
HIGH_LIMIT = 50

MAX_RISK = 1.0
MAX_DEPTH = 100

# ----------------------------------------------------------------------
# HYDROLOGY CONSTANTS
#
# Depth is produced by hydrology_service, not by flood_model.pkl. The
# reason is documented in DIRECTION.md §4: the trained model was fitted on
# district-level all-India data and does not resolve street-level variation
# inside Kochi. It still runs, as a bounded correction — see ML_CORRECTION.
# ----------------------------------------------------------------------

# A nowcast is issued into weather that is ALREADY HAPPENING. "+0 min" must
# therefore mean "this is what is on the ground now", not "rain begins this
# instant". It scales with rainfall, so 0 mm/hr still reads 0 cm — dry is dry.
#
# Recalibrated 0.75 -> 1.75 h. At 0.75 h, "Now" read 4.8 cm at Heavy and
# 13.1 cm at Cloudburst — a street with essentially nothing on it, which
# contradicts DIRECTION.md item 17 ("a nowcast issued during a cloudburst
# must show water already on the street"). At 1.75 h, Now reads 11.4 cm
# (Watch) at Heavy and 28.0 cm (Alert) at Cloudburst: rain that has plainly
# been falling for a while, which is what item 17 asks for.
ANTECEDENT_HOURS = 1.75

# mm of rain a soil column absorbs before it stops absorbing. Clay saturates
# fastest and so floods soonest; sand keeps taking water for longer.
SOIL_CAPACITY_MM = {
    "Clay": 45.0,
    "Silt": 60.0,
    "Loam": 75.0,
    "Peat": 90.0,
    "Sandy": 110.0,
}

# Share of rainfall that becomes surface runoff rather than soaking away.
# Sealed surfaces shed almost everything; vegetation absorbs.
LAND_COVER_RUNOFF = {
    "Urban": 1.00,
    "Water Body": 0.95,
    "Desert": 0.85,
    "Agricultural": 0.80,
    "Forest": 0.60,
}

# Single calibration constant converting net ponded volume to street depth.
# Tuned so that Heavy (62 mm/hr) leaves headroom and Cloudburst (120 mm/hr)
# drives the worst zones past the 50 cm Warning threshold.
#
# Retuned 1.43 -> 1.03 as the counterweight to ANTECEDENT_HOURS above, and
# for no other reason. Raising the antecedent lifts the WHOLE curve, tail
# included: at 1.75 h with the old gain, Cloudburst +120 put 13 of 16 zones
# into Warning instead of three — the "city either goes entirely red or
# entirely dry" failure item 16 describes, and a direct breach of §2.1's
# saturation discipline. Scaling the gain back restores item 14's
# calibration exactly (Heavy +120: zero Warning zones; Cloudburst +120:
# three) while keeping the higher resting level. This constant's stated job
# is precisely this trade, so retuning it here is its purpose, not a
# workaround.
DEPTH_GAIN = 1.03

# How far the trained model is allowed to move the physics estimate, as a
# fraction. The model carries real weight — it is what makes the rainfall
# response non-linear — but it cannot invent zone variation it never learned.
ML_CORRECTION = 0.25

# The model's output envelope across the whole scenario space, once it is fed
# time-evolved features. Measured from flood_model.pkl by sweeping rainfall
# 0-120 across all five offsets — not guessed. Used to normalise its response
# onto a log scale so the correction spans its band smoothly instead of
# saturating against the cap the moment rainfall gets interesting.
ML_MIN_CM = 5.99
ML_MAX_CM = 37.20