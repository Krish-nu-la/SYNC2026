from datetime import datetime
import time

from app.ml.predictor import predictor
from app.services.risk_service import risk_service
from app.services.trend_service import trend_service


class PredictionService:

    def predict(
        self,
        rainfall,
        offset
    ):

        # Start timer
        start = time.perf_counter()

        # Physics + AI prediction at this horizon
        predictions = predictor.predict(
            rainfall,
            offset
        )

        # Trend is a DIRECTION, so it needs two points. Re-run the previous
        # 30-minute step and compare — the contract defines trend as change
        # against that step specifically. At +0 there is no earlier step, so
        # compare against the antecedent state by stepping back anyway; the
        # hydrology is continuous below zero offset and returns less water.
        previous = predictor.predict(
            rainfall,
            max(0, offset - 30)
        )

        previous_depth = {
            p["zone"]["id"]: p["depth_cm"]
            for p in previous
        }

        zones = []

        for p in predictions:

            zone = p["zone"]

            result = risk_service.calculate(
                p["depth_cm"]
            )

            if offset == 0:
                # Nothing before "now" to compare against.
                trend = "steady"
            else:
                trend = trend_service.calculate(
                    previous_depth.get(
                        zone["id"],
                        p["depth_cm"]
                    ),
                    p["depth_cm"]
                )

            zones.append({

                "id": zone["id"],

                "name": zone["name"],

                "lat": zone["lat"],

                "lng": zone["lng"],

                "depthCm": result["depthCm"],

                "risk": result["risk"],

                "level": result["level"],

                "population": zone["population"],

                "trend": trend,

                # AI Confidence
                "confidence": p["confidence"]

            })

        # Stop timer
        processing_time = (
            time.perf_counter() - start
        ) * 1000

        return {

            "generatedAt": datetime.utcnow().isoformat() + "Z",

            "processingTimeMs": round(
                processing_time,
                2
            ),

            "rainfallMmHr": rainfall,

            "timeOffsetMin": offset,

            "zones": zones

        }


prediction_service = PredictionService()
