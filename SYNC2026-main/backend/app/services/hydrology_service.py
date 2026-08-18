import math

from app.core.constants import (
    ANTECEDENT_HOURS,
    SOIL_CAPACITY_MM,
    LAND_COVER_RUNOFF,
    DEPTH_GAIN,
)


class HydrologyService:
    """
    Physics-based hydrology. This is where depthCm comes from.

    A water balance, in four moves: rain falls, some of it runs off instead of
    soaking in, the drains carry some away, and whatever is left ponds — deeper
    on low ground. Every term is driven by a real column in zones.csv, so two
    zones under identical rainfall genuinely diverge.

    `offset` is the forecast horizon in minutes and it drives ACCUMULATION.
    Rain does not stop at +0; it keeps falling across the two-hour window while
    the soil saturates and the drains lose efficiency. That compounding is why
    the sweep moves, and why zones cross their thresholds at different times
    rather than all at once.
    """

    def calculate(self, rainfall, zone, weather, offset=0):

        hours = offset / 60.0

        # A nowcast is issued into weather already in progress. "+0 min" is
        # "what is on the ground right now", not "rain starts this instant" —
        # so the map shows standing water at the resting position. Scales with
        # rainfall, so dry conditions still read 0 cm.
        effective_hours = ANTECEDENT_HOURS + hours

        cumulative_rainfall = rainfall * effective_hours          # mm

        # ------------------------------------------------------------------
        # Runoff coefficient — what share of rain becomes surface water.
        # Susceptibility dominates (it encodes reported waterlogging history,
        # drainage encroachment, silting); terrain and land cover modulate.
        # ------------------------------------------------------------------
        land_factor = LAND_COVER_RUNOFF.get(zone["land_cover"], 1.0)

        runoff_coefficient = min(
            0.98,
            zone["terrain_factor"]
            * (0.25 + 0.75 * zone["susceptibility"])
            * land_factor,
        )

        runoff = (cumulative_rainfall / 10.0) * runoff_coefficient   # cm

        # ------------------------------------------------------------------
        # Soil saturation — the reason depth accelerates rather than tracking
        # rainfall linearly. Early rain infiltrates; once the column is full
        # it stops absorbing and effectively all subsequent rain runs off.
        # ------------------------------------------------------------------
        capacity = SOIL_CAPACITY_MM.get(zone["soil_type"], 60.0)

        soil_saturation = 1.0 - math.exp(-cumulative_rainfall / capacity)

        infiltration_relief = 0.45 + 0.55 * soil_saturation

        inflow_cm = runoff * infiltration_relief

        # ------------------------------------------------------------------
        # Drainage — drain_capacity is the mm/hr the network clears when
        # healthy, and it does not stay healthy. Sitting near the Thevara-
        # Perandoor canal means backflow once the canal is high, and a
        # saturated catchment means the drains are already running full.
        # ------------------------------------------------------------------
        canal_backup = 1.0 / (1.0 + zone["canal_distance_km"])

        drainage_efficiency = max(
            0.05,
            (1.0 - 0.55 * canal_backup) * (1.0 - 0.40 * soil_saturation),
        )

        outflow_cm = (
            zone["drain_capacity"] * effective_hours / 10.0
        ) * drainage_efficiency

        # ------------------------------------------------------------------
        # Ponding — low ground concentrates what the drains could not take.
        # ------------------------------------------------------------------
        net_cm = max(0.0, inflow_cm - outflow_cm)

        pooling = 1.0 + 1.6 / (1.0 + zone["elevation"])

        depth_cm = net_cm * pooling * DEPTH_GAIN

        # Diagnostics — surfaced by /explain and fed to the model as features.
        storage_capacity = zone["drain_capacity"] * (1.0 - soil_saturation)

        canal_overflow = (
            cumulative_rainfall / (zone["canal_distance_km"] + 1.0)
        )

        flow_velocity = runoff / (zone["elevation"] + 1.0)

        flood_potential = (
            runoff * soil_saturation * (1.0 - drainage_efficiency)
        )

        return {

            "depth_cm": depth_cm,

            "runoff": runoff,

            "inflow_cm": inflow_cm,

            "outflow_cm": outflow_cm,

            "soil_saturation": soil_saturation,

            "drainage_efficiency": drainage_efficiency,

            "canal_overflow": canal_overflow,

            "flow_velocity": flow_velocity,

            "storage_capacity": storage_capacity,

            "cumulative_rainfall": cumulative_rainfall,

            "flood_potential": flood_potential,

            "effective_hours": effective_hours,

        }


hydrology_service = HydrologyService()
