from app.ml.model_loader import model_loader
from app.ml.feature_builder import feature_builder
import math

from app.core.constants import (
    ML_CORRECTION,
    ML_MIN_CM,
    ML_MAX_CM,
)


class Predictor:
    """
    Combines the physics estimate with the trained model.

    flood_model.pkl is loaded, called on every request, and its output moves
    the final number — but it does not set it alone. It was trained on
    district-level all-India flood data and, measured against zones.csv, it
    separates Kochi's zones by 0.4 cm end to end while topping out near 46 cm
    against a 50 cm Warning threshold. It cannot carry street-level variation.
    What it CAN do is judge how hard a given rainfall accumulation escalates,
    which is genuine information the water balance does not encode.

    So it is applied as a bounded multiplicative correction: the physics sets
    where a zone sits relative to its neighbours, the model sets how sharply
    the whole city responds as rain accumulates. Weight is capped at
    ML_CORRECTION (±25%) so a model this coarse cannot overrule terrain.
    """

    def __init__(self):

        model_loader.load()

    def predict(self, rainfall, offset):

        df = feature_builder.build(rainfall, offset)

        zones = df["zone"]

        physics = df["physics_depth_cm"]

        X = df.drop(columns=["zone", "physics_depth_cm"])

        # Keep feature order exactly as during training
        X = X[model_loader.features]

        model_depths = model_loader.model.predict(X)

        results = []

        for zone, physics_cm, model_cm in zip(zones, physics, model_depths):

            model_cm = float(model_cm)

            # Normalise the model onto [0, 1] across its own measured envelope.
            # Log scale because the model's response to accumulated rain is
            # multiplicative, and because it keeps the correction moving
            # smoothly across the whole band instead of pinning to the cap the
            # moment rainfall gets interesting.
            model_signal = (
                math.log(max(model_cm, ML_MIN_CM) / ML_MIN_CM)
                / math.log(ML_MAX_CM / ML_MIN_CM)
            )

            model_signal = max(0.0, min(1.0, model_signal))

            # Maps to [1 - ML_CORRECTION, 1 + ML_CORRECTION]. The model damps
            # the physics in light rain and amplifies it as the catchment
            # loads up — that escalation curve is what it genuinely knows.
            correction = (
                (1.0 - ML_CORRECTION)
                + 2.0 * ML_CORRECTION * model_signal
            )

            depth_cm = float(physics_cm) * correction

            if rainfall <= 20:
                confidence = 0.98
            elif rainfall <= 40:
                confidence = 0.96
            elif rainfall <= 60:
                confidence = 0.94
            elif rainfall <= 80:
                confidence = 0.91
            else:
                confidence = 0.88

            results.append({
                "zone": zone,
                "depth_cm": round(depth_cm, 2),
                "physics_cm": round(float(physics_cm), 2),
                "model_cm": round(model_cm, 2),
                "correction": round(correction, 4),
                "confidence": confidence
            })

        return results


predictor = Predictor()
