import yaml
from pathlib import Path
from models.api_router import APIRoutes

class APIRouterController:
    def __init__(self):
        self.config_dir = Path(__file__).parent.parent / 'config'
        self.routes = []

    def load_api_routes(self):
        api_yaml_path = self.config_dir / 'api.yaml'
        with open(api_yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        return APIRoutes(data['routes'])