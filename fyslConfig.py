from pathlib import Path
import json
import inspect

class fyslConfig:

    def __init__(self) -> None:

        config_folder = Path(inspect.getmodule(type(self)).__file__).parent
        self.URL_CONFIG = config_folder.joinpath(r'config/url.json')
        self.url_config = self._load_json(self.URL_CONFIG)

    def _load_json(self, config_path: Path):
        with config_path.open(mode = 'r') as f:
            return json.load(f)