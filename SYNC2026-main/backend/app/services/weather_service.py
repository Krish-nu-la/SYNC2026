import requests

from app.core.config import settings


class WeatherService:
    """
    Weather input service for JalNetra.

    Weather observations/forecasts come from Open-Meteo.
    River discharge and water level remain explicitly marked as
    proxy-derived until real gauge data is integrated.
    """

    def __init__(self):
        self.provider = getattr(
            settings,
            "WEATHER_PROVIDER",
            "open-meteo",
        )

    def get_weather(self, rainfall_override=None, offset=0):
        """
        Return weather inputs for the requested forecast offset.

        offset:
            Forecast offset in minutes.
        """

        if self.provider == "slider":
            return self._slider_weather(rainfall_override)

        try:
            return self.get_openmeteo(
                offset=offset,
                rainfall_override=rainfall_override,
            )

        except (
            requests.RequestException,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            # Keep the prediction API operational if the
            # external weather provider is unavailable.
            return self._slider_weather(rainfall_override)

    @staticmethod
    def _slider_weather(rainfall):
        """
        Scenario/slider mode.

        Hydrology values are explicitly marked as proxy values.
        """

        rainfall = float(rainfall or 0)

        return {
            "rainfall_mm": rainfall,
            "temperature_c": 29.0,
            "humidity_percent": 85.0,

            # Proxy values — NOT observed gauge measurements.
            "river_discharge_m³_s": rainfall * 2.0,
            "water_level_m": rainfall / 100.0,

            "historical_floods": 4,
            "infrastructure": 7,

            "source": "scenario",
            "rainfall_source": "scenario",
            "hydrology_source": "proxy",
            "hydrology_observed": False,
        }

    def get_openmeteo(
        self,
        offset=0,
        rainfall_override=None,
    ):
        """
        Retrieve hourly forecast data from Open-Meteo.

        Open-Meteo provides hourly forecast weather.
        The requested minute offset is mapped to the nearest
        hourly forecast frame.
        """

        url = getattr(
            settings,
            "OPENMETEO_URL",
            "https://api.open-meteo.com/v1/forecast",
        )

        # We need enough forecast hours to cover the requested offset.
        forecast_hours = max(
            3,
            int(offset // 60) + 2,
        )

        params = {
            "latitude": getattr(
                settings,
                "WEATHER_LATITUDE",
                9.98,
            ),
            "longitude": getattr(
                settings,
                "WEATHER_LONGITUDE",
                76.28,
            ),
            "hourly": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation"
            ),
            "forecast_hours": forecast_hours,
            "timezone": "UTC",
        }

        response = requests.get(
            url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()
        hourly = data["hourly"]

        temperatures = hourly["temperature_2m"]
        humidities = hourly["relative_humidity_2m"]
        precipitation = hourly["precipitation"]

        if not temperatures:
            raise ValueError(
                "Open-Meteo returned no hourly forecast data"
            )

        # Open-Meteo provides hourly values.
        # Map 0–120 minute offsets to the nearest hourly frame.
        index = int(round(offset / 60))

        index = min(
            max(index, 0),
            len(temperatures) - 1,
        )

        forecast_rainfall = float(
            precipitation[index] or 0
        )

        temperature = float(
            temperatures[index]
        )

        humidity = float(
            humidities[index]
        )

        # Preserve the user/API rainfall override for the
        # immediate scenario while future offsets use forecast rainfall.
        if (
            offset == 0
            and rainfall_override is not None
        ):
            rainfall = float(rainfall_override)
            rainfall_source = "scenario"
        else:
            rainfall = forecast_rainfall
            rainfall_source = "open-meteo"

        return {
            "rainfall_mm": rainfall,
            "temperature_c": temperature,
            "humidity_percent": humidity,

            # These remain proxy values until real river/gauge
            # integrations are added.
            "river_discharge_m³_s": rainfall * 2.0,
            "water_level_m": rainfall / 100.0,

            "historical_floods": 4,
            "infrastructure": 7,

            "source": "open-meteo",
            "rainfall_source": rainfall_source,
            "hydrology_source": "proxy",
            "hydrology_observed": False,
        }


weather_service = WeatherService()