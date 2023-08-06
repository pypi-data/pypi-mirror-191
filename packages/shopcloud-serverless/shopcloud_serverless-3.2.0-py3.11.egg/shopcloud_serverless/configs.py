from pathlib import Path

import yaml

from . import exceptions


class Config:
    FILENAME = 'serverless.yaml'
    VERSION = 'V3'

    def __init__(self):
        self.version = None
        self.base_dir = None
        self.api_title = None
        self.api_description = None
        self.gcp_project = None
        self.gcp_region = None
        self.deploy_version = 0

    def load(self) -> bool:
        if not Path(Config.FILENAME).exists():
            return False
        with open(Config.FILENAME) as f:
            data = yaml.safe_load(f)
            self.version = data.get('version', '')
            self.base_dir = data.get('base_dir', '.')
            self.api_title = data.get('api_title', '')
            self.api_description = data.get('api_description', '')
            self.gcp_project = data.get('gcp_project')
            self.gcp_region = data.get('gcp_region')
            self.deploy_version = int(data.get('deploy_version', 0))

        if str(self.version).strip() != self.VERSION:
            raise exceptions.ConfigInvalidVersion()

        return True

    def save(self):
        with open(Config.FILENAME, 'w') as f:
            yaml.dump(self.dict(), f)

    def dict(self):
        return {
            'version': self.VERSION,
            'base_dir': self.base_dir or '.',
            'api_title': self.api_title,
            'api_description': self.api_description,
            'gcp_project': self.gcp_project,
            'gcp_region': self.gcp_region,
            'deploy_version': self.deploy_version,
        }
