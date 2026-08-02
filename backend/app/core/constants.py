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
# instant". 0.75 h of antecedent rainfall is what puts standing water on the
# map at the resting position. It scales with rainfall, so 0 mm/hr still
# reads 0 cm — dry is dry.
ANTECEDENT_HOURS = 0.75

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
DEPTH_GAIN = 1.43

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