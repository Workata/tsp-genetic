import json

# TODO if there will be enough time then rewrite this
# TODO for pydantic BaseSettings (class) with config validation


class ConfigLoader:

    @classmethod
    def load(cls, file_path: str) -> dict:
        with open(file_path) as f:
            data = json.load(f)
            return data
