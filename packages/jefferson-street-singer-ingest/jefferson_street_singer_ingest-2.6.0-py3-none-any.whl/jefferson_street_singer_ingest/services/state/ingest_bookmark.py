from typing import Dict
from datetime import datetime
import json


class IngestBookmark:
    def __init__(
        self,
        pipeline_name: str = "",
        stream_name: str = "",
        timestamp: str = datetime.strftime(datetime.now(), "%Y%m%d%H%M"),
        additional_data: Dict[str, str] = None,
    ):
        self.pipeline_name = pipeline_name
        self.stream_name = stream_name
        self.timestamp = timestamp
        self.additional_data = additional_data if additional_data else {}

    def to_dict(self):
        return {
            self.pipeline_name: {
                self.stream_name: {
                    "timestamp": self.timestamp,
                    "additional_data": self.additional_data,
                }
            }
        }

    def to_json(self) -> str:
        dict_ = self.to_dict()
        return json.dumps(dict_)
