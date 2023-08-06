from pathlib import Path

from . import endpoints, file_contents, gateways, helpers, jobs
from .configs import Config


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
        print(helpers.bcolors.OKGREEN + 'Init config success' + helpers.bcolors.ENDC)
        return 0
    elif args.which == 'jobs':
        return jobs.cli_main(args, config)
    elif args.which == 'gateway':
        return gateways.cli_main(args, config)
    elif args.which == 'endpoints':
        return endpoints.cli_main(args, config)
