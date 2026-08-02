import pandas as pd

from app.ml.model_loader import model_loader
from app.services.zone_service import ZoneService
from app.services.weather_service import weather_service
from app.services.hydrology_service import hydrology_service


class FeatureBuilder:
    """
    Builds the 19-column feature frame flood_model.pkl was trained on.

    `offset` reaches the model THROUGH the hydrology. Every rainfall-derived
    feature below is computed from the time-evolved state at that horizon
    (cumulative rainfall, saturated soil, a canal that has had time to back
    up) rather than from the instantaneous rate. That is what makes the model
    return a different number per horizon instead of five identical frames.
    """

    def __init__(self):

        self.zone_service = ZoneService()

        model_loader.load()

    def build(self, rainfall, offset):

        weather = weather_service.get_weather(rainfall)

        zones = self.zone_service.get_all_zones()

        rows = []

        for zone in zones:

            hydrology = hydrology_service.calculate(
                rainfall,
                zone,
                weather,
                offset,
            )

            land = model_loader.encoders[
                "land_cover"
            ].transform(
                [zone["land_cover"]]
            )[0]

            soil = model_loader.encoders[
                "soil_type"
            ].transform(
                [zone["soil_type"]]
            )[0]

            # Accumulated depth of rain at this horizon, not the hourly rate.
            # This is the feature the model is most responsive to.
            cumulative_rainfall = hydrology["cumulative_rainfall"]

            # Local water level rises with what the drains failed to clear and
            # with canal backup — so it is both time- and zone-dependent.
            water_level_m = (
                hydrology["canal_overflow"] / 100.0
            ) * (
                1.0 + hydrology["soil_saturation"]
            )

            river_discharge = cumulative_rainfall * 2

            rainfall_discharge = cumulative_rainfall * river_discharge

            rainfall_waterlevel = cumulative_rainfall * water_level_m

            terrain_risk = hydrology["runoff"]

            population_density = (

                zone["population"] / 10

            )

            population_risk = (

                population_density

                *

                weather["historical_floods"]

            )

            weather_severity = (

                cumulative_rainfall

                +

                weather["temperature_c"]

                +

                weather["humidity_percent"]

            ) / 3

            infra_risk = (

                10

                -

                weather["infrastructure"]

            )

            rows.append({

                "latitude": zone["lat"],

                "longitude": zone["lng"],

                "rainfall_mm": cumulative_rainfall,

                "temperature_c": weather["temperature_c"],

                "humidity_percent": weather["humidity_percent"],

                "river_discharge_m³_s": river_discharge,

                "water_level_m": water_level_m,

                "elevation_m": zone["elevation"],

                "land_cover": land,

                "soil_type": soil,

                "population_density": population_density,

                "infrastructure": weather["infrastructure"],

                "historical_floods": weather["historical_floods"],

                "rainfall_discharge": rainfall_discharge,

                "rainfall_waterlevel": rainfall_waterlevel,

                "terrain_risk": terrain_risk,

                "population_risk": population_risk,

                "weather_severity": weather_severity,

                "infra_risk": infra_risk,

                # Carried through for the predictor; dropped before predict().
                "zone": zone,

                "physics_depth_cm": hydrology["depth_cm"],

            })

        return pd.DataFrame(rows)


feature_builder = FeatureBuilder()
