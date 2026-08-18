import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.services.prediction_service import prediction_service


class SyncService:

    OFFSETS = [0, 30, 60, 90, 120]

    SYNC_INTERVAL_MINUTES = 30
    SYNC_TIMEOUT_SECONDS = 60

    SNAPSHOT_PATH = Path("data/latest_snapshot.json")

    def __init__(self):
        self.SNAPSHOT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def build_snapshot(self, rainfall=None):
        """
        Build a complete 2-hour forecast package.

        Each frame is generated independently so one failed
        frame does not destroy the previous cached snapshot.
        """

        started = time.perf_counter()

        forecasts = []

        for offset in self.OFFSETS:

            # IMPORTANT:
            # rainfall override is only used for current frame.
            current_rainfall = (
                rainfall
                if offset == 0
                else None
            )

            result = prediction_service.predict(
                rainfall=current_rainfall or 0,
                offset=offset,
                db=None
            )

            forecasts.append({
                "offsetMin": offset,
                "data": result
            })

        now = datetime.now(timezone.utc)

        snapshot = {
            "status": "live",

            "syncType": "scheduled",

            "generatedAt": now.isoformat(),

            "nextSyncAt": (
                now + timedelta(
                    minutes=self.SYNC_INTERVAL_MINUTES
                )
            ).isoformat(),

            "expiresAt": (
                now + timedelta(hours=2)
            ).isoformat(),

            "processingTimeMs": round(
                (time.perf_counter() - started) * 1000,
                2
            ),

            "forecasts": forecasts
        }

        self._save_snapshot(snapshot)

        return snapshot

    def _save_snapshot(self, snapshot):

        temp_path = self.SNAPSHOT_PATH.with_suffix(
            ".tmp"
        )

        with open(
            temp_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                snapshot,
                file,
                indent=2
            )

        # Atomic replacement.
        temp_path.replace(
            self.SNAPSHOT_PATH
        )

    def get_latest(self):

        if not self.SNAPSHOT_PATH.exists():

            return {
                "status": "unavailable",
                "message": "No forecast snapshot available."
            }

        try:

            with open(
                self.SNAPSHOT_PATH,
                "r",
                encoding="utf-8"
            ) as file:

                snapshot = json.load(file)

            generated = datetime.fromisoformat(
                snapshot["generatedAt"]
            )

            now = datetime.now(timezone.utc)

            age_seconds = (
                now - generated
            ).total_seconds()

            snapshot["dataAgeSeconds"] = round(
                age_seconds,
                2
            )

            snapshot["status"] = (
                "stale"
                if age_seconds > 7200
                else "offline"
            )

            return snapshot

        except (
            OSError,
            ValueError,
            KeyError,
            json.JSONDecodeError
        ):

            return {
                "status": "unavailable",
                "message": "Forecast snapshot is invalid."
            }


sync_service = SyncService()