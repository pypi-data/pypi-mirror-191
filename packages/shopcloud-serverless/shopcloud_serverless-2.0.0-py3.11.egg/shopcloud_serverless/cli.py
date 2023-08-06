from pathlib import Path

from . import endpoints, file_contents, gateways, helpers, jobs
from .configs import Config


def init_file_structure(config: Config):
    base_dir = config.base_dir
    if base_dir != '.':
        if not Path(base_dir).exists():
            Path(base_dir).mkdir()
    if not Path(base_dir, 'endpoints').exists():
        Path(base_dir, 'endpoints').mkdir()
    if not Path(base_dir, 'endpoints', 'src').exists():
        Path(base_dir, 'endpoints', 'src').mkdir()
        Path(base_dir, 'endpoints', 'src', '__init__.py').touch()
        Path(base_dir, 'endpoints', 'src', 'services').mkdir()
        Path(base_dir, 'endpoints', 'src', 'services', '__init__.py').touch()
        endpoints.endpoint_create(base_dir, 'hello_world')
        endpoints.endpoint_create(base_dir, 'docs')

    if not Path(base_dir, 'api.yaml').exists():
        with open(f"{base_dir}/api.yaml", "w") as file:
            file.write(file_contents.api(
                title=config.api_title,
                description=config.api_description,
                project=config.gcp_project,
                region=config.gcp_region,
            ))
    if not Path(base_dir, 'requirements.txt').exists():
        with open(f"{base_dir}/requirements.txt", "w") as file:
            file.write(file_contents.requirements())


def main(args) -> int:
    if not hasattr(args, 'which'):
        print(
            helpers.bcolors.FAIL
            + 'Can not parse action use --help'
            + helpers.bcolors.ENDC
        )
        return 1

    if hasattr(args, 'debug') and args.debug:
        print(args)

    config = Config()

    if args.which == 'init':
        config.base_dir = args.base_dir or helpers.ask_for('Base directory', '.')
        config.api_title = args.api_title or helpers.ask_for('API title', 'My API')
        config.api_description = args.api_description or helpers.ask_for('API description', 'My API description')
        config.gcp_project = args.gcp_project or helpers.ask_for('GCP project')
        config.gcp_region = args.gcp_region or helpers.ask_for('GCP region', 'europe-west1')
        config.save()
        init_file_structure(config)
        print(helpers.bcolors.OKGREEN + 'Init API-Gateway Config success' + helpers.bcolors.ENDC)
        return 0
    elif args.which == 'jobs':
        return jobs.cli_main(args, config)
    elif args.which == 'gateway':
        return gateways.cli_main(args, config)
    elif args.which == 'endpoints':
        return endpoints.cli_main(args, config)
