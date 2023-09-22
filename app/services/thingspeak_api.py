from dataclasses import dataclass
from json import loads, dumps

from app.clients.base_api import BaseApiClient
from app.dtos.thingspeak import ThingspeakResponse


@dataclass
class ThingspeakApiClient(BaseApiClient):
    def get_data(self, size: int = 10000) -> ThingspeakResponse:
        response = self.get(
            "/channels/1293177/feeds.json",
            params={"results": {size}},
        )
        if response.get("error"):
            raise response.get("error")

        json_body = loads(response.get("body"))
        for feed in json_body.get("feeds", []):
            for key, value in feed.items():
                if key.startswith("field") and value.lower() in ["nan"]:
                    feed[key] = 0.0

        cleaned_response = dumps(json_body)

        return ThingspeakResponse.schema().loads(cleaned_response)
